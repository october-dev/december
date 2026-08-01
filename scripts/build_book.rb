#!/usr/bin/env ruby
# frozen_string_literal: true

require "cgi"
require "digest"
require "open3"
require "pathname"
require "time"

ROOT = Pathname.new(__dir__).parent.expand_path
OUTPUT = ROOT.join("DECEMBER-BOOK.html")

PYTHON_MARKDOWN = <<~'PY'.freeze
  import sys
  from markdown_it import MarkdownIt

  renderer = MarkdownIt("commonmark", {"html": False})
  renderer.enable("table")
  renderer.enable("strikethrough")
  sys.stdout.write(renderer.render(sys.stdin.read()))
PY

PARTS = [
  ["I", "Enter the dream", "The promise, the public story, and the present state.", [
    ["OVERVIEW.md", "Readable introduction", "Orientation"],
    ["README.md", "Repository guide", "Current status"],
    ["LANDING-PAGE-BRIEF.md", "Public story and language", "Communication brief"]
  ]],
  ["II", "The world specification", "The complete product, world, agent, society, architecture, validation, and roadmap specification.",
   (0..12).map { |n| [Pathname.new(Dir[ROOT.join(format("wiki/%02d-*.md", n))].first).relative_path_from(ROOT).to_s, "Specification #{format('%02d', n)}", "Normative design"] }],
  ["III", "Evidence, integrity, and the lab", "Sources, determinism, parameters, costs, initial conditions, research charter, and R0 protocol.",
   (13..19).map { |n| [Pathname.new(Dir[ROOT.join(format("wiki/%02d-*.md", n))].first).relative_path_from(ROOT).to_s, "Research #{format('%02d', n)}", "Research and hardening"] }],
  ["IV", "Architecture decisions", "Accepted and proposed constraints, their consequences, and rejected alternatives.",
   Dir[ROOT.join("wiki/adr/*.md")].sort.map { |p| [Pathname.new(p).relative_path_from(ROOT).to_s, "ADR #{File.basename(p)[0, 3]}", "Decision record"] }],
  ["V", "Audits and challenge record", "The current verdict first, then the historical pass and reusable audit instrument.", [
    ["AUDIT-FINDINGS-PASS-2.md", "Independent audit, pass 2", "Current audit verdict"],
    ["AUDIT-FINDINGS.md", "Audit findings, pass 1", "Historical audit"],
    ["AUDIT-REPORT-TEMPLATE.md", "Independent audit template", "Review instrument"]
  ]]
].freeze

def esc(value)
  CGI.escapeHTML(value.to_s)
end

def text_only(value)
  CGI.unescapeHTML(value.gsub(/<[^>]+>/, "")).strip
end
def slug(value)
  value.downcase.encode("ASCII", invalid: :replace, undef: :replace, replace: "")
       .gsub(/[^a-z0-9]+/, "-").gsub(/\A-|\-\z/, "")
end

def render_markdown(markdown)
  html, error, status = Open3.capture3("python3", "-c", PYTHON_MARKDOWN, stdin_data: markdown)
  abort "Markdown rendering failed: #{error}" unless status.success?
  html
end

docs = []
PARTS.each do |part_no, part_title, _description, entries|
  entries.each do |path, label, kind|
    source = ROOT.join(path)
    abort "Missing source: #{path}" unless source.file?
    markdown = source.read
    docs << {
      path: path, label: label, kind: kind, part: part_no, part_title: part_title,
      id: "doc-#{slug(path.sub(/\.md\z/, ""))}",
      title: markdown.lines.find { |line| line.start_with?("# ") }&.sub(/^# /, "")&.strip || path,
      markdown: markdown,
      words: markdown.scan(/\b[\p{L}\p{N}][\p{L}\p{N}'’-]*\b/).length,
      hash: Digest::SHA256.hexdigest(markdown)
    }
  end
end

path_map = docs.to_h { |doc| [doc[:path], doc] }
path_map["wiki/"] = path_map["wiki/00-vision-and-north-star.md"]

docs.each do |doc|
  html = render_markdown(doc[:markdown])
  used_heading_ids = Hash.new(0)
  html = html.gsub(/<(h[1-6])>(.*?)<\/\1>/m) do
    tag, body = Regexp.last_match.captures
    base_id = slug(text_only(body))
    used_heading_ids[base_id] += 1
    id = used_heading_ids[base_id] == 1 ? base_id : "#{base_id}-#{used_heading_ids[base_id]}"
    full_id = "#{doc[:id]}-#{id}"
    %(<#{tag} id="#{full_id}">#{body}<a class="anchor" href="##{full_id}" aria-label="Link">#</a></#{tag}>)
  end
  html = html.gsub(/href="([^"]+)"/) do
    href = CGI.unescapeHTML(Regexp.last_match(1))
    if href.start_with?("#")
      same_document = href.start_with?("##{doc[:id]}-") ? href : "##{doc[:id]}-#{href.delete_prefix('#')}"
      next %(href="#{esc(same_document)}")
    end
    next %(href="#{esc(href)}") if href.match?(%r{\A(?:https?:|mailto:)})
    path, fragment = href.split("#", 2)
    resolved = Pathname.new(doc[:path]).dirname.join(path).cleanpath.to_s
    target = path_map[resolved] || path_map["#{resolved}/"]
    replacement = target ? "##{target[:id]}#{fragment && !fragment.empty? ? "-#{fragment}" : ""}" : href
    %(href="#{esc(replacement)}")
  end
  doc[:html] = html
  doc[:headings] = html.scan(/<h([23]) id="([^"]+)">(.*?)<a class="anchor"/m).map do |level, id, body|
    [level, id, text_only(body)]
  end
end

total_words = docs.sum { |doc| doc[:words] }
minutes = (total_words / 230.0).ceil
generated = Time.now.iso8601
revision = `git -C #{ROOT} rev-parse --short HEAD 2>/dev/null`.strip
corpus_hash = Digest::SHA256.hexdigest(docs.map { |doc| "#{doc[:path]}:#{doc[:hash]}" }.join("\n"))

sidebar = PARTS.map do |part_no, part_title, _description, _entries|
  links = docs.select { |doc| doc[:part] == part_no }.map do |doc|
    %(<a class="side-link" data-side="#{doc[:id]}" href="##{doc[:id]}"><b>#{esc(doc[:label])}</b><span>#{esc(doc[:title])}</span></a>)
  end.join
  %(<section class="side-part"><small>Part #{part_no}</small><h3>#{esc(part_title)}</h3>#{links}</section>)
end.join

body = PARTS.map do |part_no, part_title, description, _entries|
  chapters = docs.select { |doc| doc[:part] == part_no }.map do |doc|
    inside = doc[:headings].first(20).map do |level, id, heading|
      %(<a class="level-#{level}" href="##{id}">#{esc(heading)}</a>)
    end.join
    inside = inside.empty? ? "" : %(<details class="inside"><summary>Inside this chapter</summary><nav>#{inside}</nav></details>)
    <<~HTML
      <article class="chapter" id="#{doc[:id]}" data-title="#{esc(doc[:title])}" data-source="#{esc(doc[:path])}">
        <header class="chapter-meta"><div><em>#{esc(doc[:kind])}</em><code>#{esc(doc[:path])}</code></div><div><span>#{doc[:words].to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse} words</span><label><input type="checkbox" class="read" data-read="#{doc[:id]}"> Read</label></div></header>
        #{inside}
        <div class="markdown">#{doc[:html]}</div>
        <footer class="chapter-foot"><details><summary>Write feedback on this chapter</summary><p>Saved only in this browser until exported.</p><textarea data-note="#{doc[:id]}" placeholder="Questions, disagreements, changes, decisions…"></textarea></details><a href="#desk">Reader’s desk ↑</a></footer>
      </article>
    HTML
  end.join
  %(<section class="part"><header class="part-head"><small>Part #{part_no}</small><h2>#{esc(part_title)}</h2><p>#{esc(description)}</p></header>#{chapters}</section>)
end.join

manifest = docs.map do |doc|
  %(<tr><td><a href="##{doc[:id]}">#{esc(doc[:path])}</a></td><td>#{doc[:words]}</td><td><code>#{doc[:hash][0, 12]}</code></td></tr>)
end.join

styles = <<~CSS
  :root{color-scheme:light;--paper:#f4efe4;--deep:#e8deca;--ink:#211e19;--muted:#756b5f;--line:#cfc3b1;--accent:#a8472a;--soft:#ead0c1;--green:#315b49;--panel:#fffaf0;--code:#292824;--codeink:#f6eddd;--serif:Iowan Old Style,Baskerville,Georgia,serif;--sans:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;--mono:"SFMono-Regular",Consolas,monospace}html[data-theme=dark]{color-scheme:dark;--paper:#171816;--deep:#22231f;--ink:#eee8dc;--muted:#aba297;--line:#46453f;--accent:#ef8a67;--soft:#4b3027;--green:#78aa92;--panel:#20211e;--code:#0c0e0d;--codeink:#f3eadb}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:25px}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans)}body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.2;background-image:radial-gradient(#795f3b 0.5px,transparent 0.5px);background-size:5px 5px}a{color:var(--accent);text-underline-offset:3px}button,input,textarea{font:inherit}.progress{position:fixed;z-index:100;top:0;left:0;height:3px;width:0;background:var(--accent)}.mobile{display:none}.sidebar{position:fixed;z-index:20;inset:0 auto 0 0;width:305px;overflow:auto;padding:26px 20px 70px;border-right:1px solid var(--line);background:var(--paper)}.brand{display:flex;align-items:center;gap:11px;margin-bottom:22px;color:var(--ink);text-decoration:none}.brand i{display:grid;place-items:center;width:39px;height:39px;border-radius:50%;color:var(--paper);background:var(--ink);font:23px var(--serif)}.brand b{display:block;font:21px var(--serif)}.brand span{color:var(--muted);font-size:11px}.search{position:sticky;top:0;z-index:2;padding:8px 0 14px;background:var(--paper)}.search input{width:100%;padding:11px;border:1px solid var(--line);border-radius:8px;color:var(--ink);background:var(--panel)}.search span{display:block;min-height:17px;margin-top:6px;color:var(--muted);font-size:11px}.side-part{padding:15px 0;border-top:1px solid var(--line)}.side-part small{color:var(--accent);font:700 10px var(--mono);text-transform:uppercase}.side-part h3{margin:3px 0 8px;font:600 15px var(--serif)}.side-link{display:block;margin:0 -7px;padding:6px 7px;border-radius:6px;color:var(--muted);text-decoration:none}.side-link:hover,.side-link.active{color:var(--ink);background:var(--panel)}.side-link b{display:block;font-size:11px}.side-link span{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:13px var(--serif)}.tools{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:15px}.tools button{padding:9px;border:1px solid var(--line);border-radius:7px;color:var(--ink);background:var(--panel);cursor:pointer;font-size:11px}.meter{color:var(--muted);font-size:11px}.shell{margin-left:305px}.cover{min-height:92vh;display:flex;align-items:end;padding:8vw 6vw;border-bottom:1px solid var(--line);background:radial-gradient(circle at 78% 18%,var(--soft),transparent 32%),linear-gradient(155deg,transparent 55%,var(--deep))}.cover>div{width:min(1060px,100%)}.kicker{color:var(--accent);font:700 11px var(--mono);letter-spacing:.16em;text-transform:uppercase}.cover h1{margin:20px 0;font:500 clamp(62px,10vw,140px)/.85 var(--serif);letter-spacing:-.06em}.cover .lede{max-width:780px;font:25px/1.45 var(--serif)}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:55px;border:1px solid var(--line);background:var(--line)}.stats div{min-height:95px;padding:17px;background:var(--paper)}.stats b{display:block;font:30px var(--serif)}.stats span{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.08em}.desk{padding:90px 6vw;border-bottom:1px solid var(--line)}.desk h2{margin:8px 0 25px;font:500 clamp(42px,6vw,70px)/1 var(--serif);letter-spacing:-.04em}.desk-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(280px,.8fr);gap:55px;max-width:1140px}.desk p,.desk li{line-height:1.65}.desk h3{margin:34px 0 10px;font:600 24px var(--serif)}.callout{padding:22px;border-left:4px solid var(--accent);background:var(--panel);box-shadow:0 20px 60px #32261418}.callout b{color:var(--accent)}.decisions{padding:0;list-style:none;counter-reset:n}.decisions li{position:relative;padding:11px 0 11px 43px;border-top:1px solid var(--line);counter-increment:n}.decisions li:before{content:counter(n,decimal-leading-zero);position:absolute;left:0;color:var(--accent);font:700 11px/2 var(--mono)}.machine{display:grid;gap:9px}.machine div{padding:13px 15px;border:1px solid var(--line);border-radius:7px;background:var(--panel)}.machine b{display:block;font-family:var(--serif)}.machine span{color:var(--muted);font-size:12px}.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}.action{padding:10px 15px;border:1px solid var(--ink);border-radius:999px;color:var(--paper);background:var(--ink);text-decoration:none;cursor:pointer}.action.alt{color:var(--ink);background:transparent}.part-head{padding:90px 6vw 50px;border-bottom:1px solid var(--line);background:var(--deep)}.part-head small{color:var(--accent);font:700 11px var(--mono);text-transform:uppercase}.part-head h2{margin:10px 0;font:500 clamp(42px,6vw,72px)/1 var(--serif);letter-spacing:-.04em}.part-head p{max-width:760px;color:var(--muted);font:20px/1.45 var(--serif)}.chapter{width:min(900px,calc(100% - 80px));margin:70px auto 110px;padding-bottom:50px;border-bottom:2px solid var(--ink)}.chapter[hidden],.side-link[hidden]{display:none}.chapter-meta{display:flex;justify-content:space-between;gap:15px;margin-bottom:32px;padding-bottom:12px;border-bottom:1px solid var(--line);color:var(--muted);font-size:11px}.chapter-meta>div{display:flex;align-items:center;gap:12px}.chapter-meta em{padding:5px 7px;border-radius:4px;color:var(--paper);background:var(--green);font-style:normal;font-weight:700;text-transform:uppercase}.chapter-meta code{font-family:var(--mono)}.inside{margin-bottom:28px;padding:13px 15px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}.inside summary{cursor:pointer;font-size:12px;font-weight:700}.inside nav{display:grid;grid-template-columns:1fr 1fr;gap:5px 16px;margin-top:11px}.inside a{color:var(--muted);font-size:12px;text-decoration:none}.inside .level-3{padding-left:12px}.markdown{font:18px/1.72 var(--serif)}.markdown>h1{margin:0 0 40px;font:500 clamp(43px,6vw,76px)/.98 var(--serif);letter-spacing:-.045em}.markdown h2{margin:68px 0 18px;padding-top:8px;font:600 34px/1.12 var(--serif);letter-spacing:-.025em}.markdown h3{margin:40px 0 13px;font:600 25px/1.2 var(--serif)}.markdown h4{margin:28px 0 9px;font:700 17px var(--sans)}.anchor{margin-left:7px;color:var(--line);font:400 .55em var(--sans);text-decoration:none;opacity:0}.markdown h1:hover .anchor,.markdown h2:hover .anchor,.markdown h3:hover .anchor{opacity:1}.markdown p{margin:0 0 1.25em}.markdown hr{margin:55px 0;border:0;border-top:1px solid var(--line)}.markdown blockquote{margin:26px 0;padding:2px 0 2px 22px;border-left:4px solid var(--accent)}.markdown li{margin:.4em 0}.markdown li::marker{color:var(--accent)}.markdown code{padding:.14em .34em;border-radius:4px;background:var(--deep);font:.82em/1.5 var(--mono);overflow-wrap:anywhere}.markdown pre{overflow:auto;margin:27px 0;padding:19px;border-radius:8px;color:var(--codeink);background:var(--code)}.markdown pre code{padding:0;color:inherit;background:transparent;white-space:pre}.markdown table{display:block;width:100%;overflow:auto;margin:28px 0;border-collapse:collapse;font:13px/1.45 var(--sans)}.markdown th,.markdown td{min-width:110px;padding:9px 11px;border:1px solid var(--line);text-align:left;vertical-align:top}.markdown th{background:var(--deep);font-size:10px;text-transform:uppercase}.chapter-foot{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-top:70px;padding-top:22px;border-top:1px solid var(--line);font-size:12px}.chapter-foot details{flex:1}.chapter-foot summary{color:var(--accent);cursor:pointer;font-weight:700}.chapter-foot textarea{width:100%;min-height:145px;resize:vertical;padding:12px;border:1px solid var(--line);border-radius:8px;color:var(--ink);background:var(--panel)}.manifest{width:min(1000px,calc(100% - 80px));margin:90px auto 140px}.manifest h2{font:500 48px var(--serif)}.manifest .meta{padding:14px;border:1px solid var(--line);background:var(--panel);overflow-wrap:anywhere}.manifest table{width:100%;border-collapse:collapse;font-size:12px}.manifest th,.manifest td{padding:8px;border-bottom:1px solid var(--line);text-align:left}.none{display:none;padding:80px;text-align:center;font:28px var(--serif)}
  @media(max-width:920px){.mobile{display:flex;position:sticky;top:0;z-index:30;justify-content:space-between;padding:10px 15px;border-bottom:1px solid var(--line);background:var(--paper)}.mobile button{padding:7px 10px;border:1px solid var(--line);border-radius:7px;color:var(--ink);background:var(--panel)}.sidebar{transform:translateX(-103%);transition:.2s;box-shadow:0 20px 70px #0005}body.nav-open .sidebar{transform:none}.shell{margin:0}.cover,.desk,.part-head{padding-left:24px;padding-right:24px}.desk-grid{grid-template-columns:1fr}.inside nav{grid-template-columns:1fr}}
  @media(max-width:560px){.cover h1{font-size:57px}.cover .lede{font-size:19px}.stats{grid-template-columns:1fr 1fr}.chapter{width:calc(100% - 38px)}.chapter-meta,.chapter-foot{align-items:flex-start;flex-direction:column}.markdown{font-size:17px}.markdown>h1{font-size:42px}.markdown h2{font-size:29px}}
  @media print{.sidebar,.mobile,.progress,.actions,.inside,.chapter-foot,.anchor{display:none!important}.shell{margin:0}.cover{page-break-after:always}.desk{page-break-after:always}.part-head,.chapter{page-break-before:always}.chapter{width:100%;margin:40px auto}a{color:inherit}}
CSS

scripts = <<~JS
  (function(){
    var R=document.documentElement,B=document.body,D=[].slice.call(document.querySelectorAll('.chapter')),S=[].slice.call(document.querySelectorAll('.side-link')),Q=document.getElementById('search'),O=document.getElementById('search-out'),N=document.getElementById('none'),P='december-book:';
    function get(k){try{return localStorage.getItem(P+k)}catch(e){return null}}function set(k,v){try{localStorage.setItem(P+k,v)}catch(e){}}
    if(get('theme')==='dark')R.dataset.theme='dark';function themeLabel(){document.getElementById('theme').textContent=R.dataset.theme==='dark'?'Light mode':'Dark mode'}themeLabel();
    document.getElementById('theme').onclick=function(){R.dataset.theme=R.dataset.theme==='dark'?'light':'dark';set('theme',R.dataset.theme);themeLabel()};
    document.getElementById('menu').onclick=function(){B.classList.toggle('nav-open')};S.forEach(function(a){a.onclick=function(){B.classList.remove('nav-open')}});document.getElementById('print').onclick=function(){print()};
    function search(){var q=Q.value.trim().toLowerCase(),v=0;D.forEach(function(c){var m=!q||c.textContent.toLowerCase().indexOf(q)>-1;c.hidden=!m;var a=document.querySelector('[data-side="'+c.id+'"]');if(a)a.hidden=!m;if(m)v++});N.style.display=v?'none':'block';O.textContent=q?v+' of '+D.length+' chapters':'Press / to search'}Q.oninput=search;
    document.onkeydown=function(e){if(e.key==='/'&&document.activeElement!==Q&&document.activeElement.tagName!=='TEXTAREA'){e.preventDefault();Q.focus()}if(e.key==='Escape'&&document.activeElement===Q){Q.value='';search();Q.blur()}};
    function meter(){document.getElementById('meter').textContent=document.querySelectorAll('.read:checked').length+' of '+D.length+' chapters marked read'}document.querySelectorAll('.read').forEach(function(c){c.checked=get('read:'+c.dataset.read)==='1';c.onchange=function(){set('read:'+c.dataset.read,c.checked?'1':'0');meter()}});meter();
    document.querySelectorAll('[data-note]').forEach(function(t){t.value=get('note:'+t.dataset.note)||'';t.oninput=function(){set('note:'+t.dataset.note,t.value)}});
    document.getElementById('export').onclick=function(){var l=['# December reading notes','','Exported: '+new Date().toISOString(),''],n=0;D.forEach(function(c){var t=c.querySelector('[data-note]'),x=t?t.value.trim():'',r=c.querySelector('.read').checked;if(!x&&!r)return;n++;l.push('## '+c.dataset.title,'','- Source: `'+c.dataset.source+'`','- Marked read: '+(r?'yes':'no'),'');if(x)l.push(x,'')});if(!n)l.push('_No notes or read markers yet._','');var b=new Blob([l.join('\\n')],{type:'text/markdown'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='december-reading-notes.md';a.click();setTimeout(function(){URL.revokeObjectURL(u)},1000)};
    function progress(){var h=document.documentElement.scrollHeight-innerHeight;document.getElementById('progress').style.width=(h?scrollY/h*100:0)+'%'}addEventListener('scroll',progress,{passive:true});progress();
    if('IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)S.forEach(function(a){a.classList.toggle('active',a.dataset.side===e.target.id)})})},{rootMargin:'-15% 0px -75% 0px'});D.forEach(function(c){io.observe(c)})}
  }());
JS

html = <<~HTML
  <!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="The complete December product, research, architecture, and audit corpus in one reviewable book."><title>December — The Complete Working Book</title><style>#{styles}</style></head><body>
  <div class="progress" id="progress"></div><div class="mobile"><b>December book</b><button id="menu">Contents</button></div>
  <aside class="sidebar"><a class="brand" href="#top"><i>D</i><div><b>December</b><span>The complete working book</span></div></a><div class="search"><input id="search" type="search" placeholder="Search the whole book…"><span id="search-out">Press / to search</span></div><nav>#{sidebar}</nav><div class="tools"><button id="theme">Dark mode</button><button id="export">Export notes</button></div><p class="meter" id="meter"></p></aside>
  <main class="shell" id="top"><section class="cover"><div><p class="kicker">Wega Labs · Review edition · #{esc(generated[0, 10])}</p><h1>December</h1><p class="lede">The complete working book for a little artificial world that keeps living: the dream, the causal machinery, the research contract, every open decision, and the audits that tried to break it.</p><div class="stats"><div><b>#{docs.length}</b><span>source documents</span></div><div><b>#{total_words.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse}</b><span>source words</span></div><div><b>≈ #{minutes / 60}h #{minutes % 60}m</b><span>complete read</span></div><div><b>Gate 0</b><span>still open</span></div></div></div></section>
  <section class="desk" id="desk"><p class="kicker">Before page one</p><h2>The reader’s desk</h2><div class="desk-grid"><div>
    <p>This is a faithful compilation, not a replacement specification. Every chapter names its source file and retains the source text. This desk exists to make the decisions and inconsistencies visible before more of the world is built.</p>
    <div class="callout"><b>The most important status collision.</b> The roadmap says implementation must remain unstarted until Gate 0 closes. The README says Phase 1 is underway, and the deterministic event/RNG/replay spine already exists. We should formally call that foundation a bounded pre-gate spike, or revise Gate 0 and the roadmap to match what has actually happened.</div>
    <h3>The seven decisions that need you</h3><ol class="decisions"><li><b>Budget:</b> maximum cash spend after existing credits, emergency cutoff behavior, and the canonical-world versus research-ensemble allocation.</li><li><b>Licensing:</b> permissive-only reuse or deliberate compatibility with reciprocal licenses.</li><li><b>Deployment:</b> canonical machine and OS, and whether cloud infrastructure is in scope.</li><li><b>Pace:</b> the initial relationship between real and simulated time.</li><li><b>Publication:</b> private/local history, public streaming, or a staged combination.</li><li><b>Research posture:</b> accept or revise the claims ladder, R0 protocol, and separation of canonical exhibit from registered cohorts.</li><li><b>Naming:</b> reserve December for this living world and distinctly rename or separate December Sato.</li></ol>
    <h3>Randomness and human messiness</h3><p>The design allows chance, uneven personalities, destructive motives, glory-seeking, revenge, altruism, martyrdom, irrationality, domination, risk, and mistakes. It forbids a <em>system-wide reward for viewer engagement</em> or a hidden storyteller creating war because war would be exciting. Individuals may want terrible or theatrical things; the world itself cannot secretly want a better episode.</p>
    <h3>Reading paths</h3><p><b>One-hour alignment:</b> Overview, pass-2 audit, risks/open questions, roadmap, and ADRs. <b>Full understanding:</b> Parts I–IV in order, then the audits. <b>Implementation:</b> focus on chapters 06, 09, 10, 11, 14, 15, 16, and the ADRs.</p><div class="actions"><a class="action" href="#doc-overview">Start reading ↓</a><a class="action alt" href="#doc-audit-findings-pass-2">Current audit</a><button class="action alt" id="print">Print / save PDF</button></div>
  </div><aside><h3>The machine in five moves</h3><div class="machine"><div><b>1 · Kernel owns truth</b><span>matter, time, bodies, permissions, outcomes</span></div><div><b>2 · Residents choose attempts</b><span>private knowledge, memory, motives, structured actions</span></div><div><b>3 · Events become history</b><span>causes, random draws, consequences, provenance</span></div><div><b>4 · Memory becomes identity</b><span>experience, testimony, belief, relationships, commitments</span></div><div><b>5 · The observer reads, never directs</b><span>since-you-left, why, replay, branches</span></div></div><h3>What exists today</h3><p>Integer-valued canonical state, deterministic named random streams, append-only hash-chained events, snapshots, and exact replay tests. No ecology, residents, cognition, institutions, or continuously living world exists yet.</p><h3>Giving feedback</h3><p>Every chapter ends with a notes field. Notes stay in this browser. <b>Export notes</b> downloads one Markdown feedback file organized by source.</p></aside></div></section>
  <div class="none" id="none">No chapter contains that phrase.</div>#{body}
  <section class="manifest"><p class="kicker">Reproducibility</p><h2>Corpus manifest</h2><p>Re-run <code>ruby scripts/build_book.rb</code> after changing a source document.</p><p class="meta"><b>Generated:</b> #{esc(generated)} · <b>Source revision:</b> #{esc(revision)} · <b>Corpus SHA-256:</b> <code>#{corpus_hash}</code></p><table><thead><tr><th>Source</th><th>Words</th><th>SHA-256</th></tr></thead><tbody>#{manifest}</tbody></table></section></main><script>#{scripts}</script></body></html>
HTML

OUTPUT.write(html)
puts "Wrote #{OUTPUT.relative_path_from(ROOT)}"
puts "#{docs.length} documents · #{total_words} source words · #{OUTPUT.size} bytes"
