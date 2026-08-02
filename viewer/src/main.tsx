import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { Container, Graphics, Stage, Text, useApp } from '@pixi/react';
import * as PIXI from 'pixi.js';
import { Viewport } from 'pixi-viewport';

import * as map from './data/gentle.js';
import { characters } from './data/characters.ts';
import { Character } from './components/Character.tsx';
import { PixiStaticMap } from './components/PixiStaticMap.tsx';
import PixiViewport from './components/PixiViewport.tsx';
import type { WorldMap } from './world-map.ts';
import folkSpritesUrl from './assets/32x32folk.png?url';
import gentleTilesUrl from './assets/gentle-obj.png?url';
import './styles.css';

type Point = { x: number; y: number };
type SnapshotResident = {
  resident_id: string;
  name: string;
  role: string;
  x_millimetres: number;
  y_millimetres: number;
  activity: string;
};
type SnapshotContainer = { container_id: string; grain_grams: number };
type Snapshot = {
  contract_version: string;
  scenario_id: string;
  state_hash: string;
  through_sequence: number;
  coordinate_system: { millimetres_per_tile: number };
  state: {
    sim_time: number;
    containers: SnapshotContainer[];
    residents: SnapshotResident[];
    ledger: { live_grain_grams: number; spoiled_grain_grams: number };
  };
};
type ReplayEvent = {
  sequence: number;
  event_id: string;
  event_type: string;
  sim_time: number;
  event_hash: string;
  payload: Record<string, string | number>;
};
type Manifest = {
  contract_version: string;
  scenario_id: string;
  event_count: number;
  final_state_hash: string;
};
type Replay = { manifest: Manifest; snapshot: Snapshot; events: ReplayEvent[] };
type Resident = SnapshotResident & {
  color: string;
  character: (typeof characters)[number];
  point: Point;
  direction: Point;
};

const worldMap = {
  width: map.mapwidth,
  height: map.mapheight,
  tileSetUrl: gentleTilesUrl,
  tileSetDimX: map.tilesetpxw,
  tileSetDimY: map.tilesetpxh,
  tileDim: map.tiledim,
  bgTiles: map.bgtiles,
  objectTiles: map.objmap,
  animatedSprites: [],
} as WorldMap;

const colors = ['#7fb9b2', '#e3a866', '#d9806c', '#9caa6a'];

async function loadReplay(): Promise<Replay> {
  const base = `${import.meta.env.BASE_URL}data/`;
  const [manifestResponse, snapshotResponse, eventsResponse] = await Promise.all([
    fetch(`${base}manifest.json`),
    fetch(`${base}snapshot.json`),
    fetch(`${base}events.jsonl`),
  ]);
  if (!manifestResponse.ok || !snapshotResponse.ok || !eventsResponse.ok) {
    throw new Error('The kernel replay bundle could not be loaded.');
  }
  const manifest = await manifestResponse.json() as Manifest;
  const snapshot = await snapshotResponse.json() as Snapshot;
  const eventsText = await eventsResponse.text();
  const events = eventsText.trim().split('\n').filter(Boolean).map((line) => JSON.parse(line) as ReplayEvent);
  if (manifest.contract_version !== 'december.observer.v1' || snapshot.contract_version !== manifest.contract_version) {
    throw new Error(`Unsupported observer contract: ${manifest.contract_version}`);
  }
  if (events.length !== manifest.event_count) throw new Error('Replay manifest event count mismatch.');
  return { manifest, snapshot, events };
}

function effectiveEventTime(event: ReplayEvent) {
  return event.event_type === 'world.time_advanced.v1'
    ? Number(event.payload.sim_time)
    : event.sim_time;
}

function projectionAt(replay: Replay, simTime: number) {
  const millimetresPerTile = replay.snapshot.coordinate_system.millimetres_per_tile;
  const activeEvents = replay.events.filter((event) => effectiveEventTime(event) <= simTime);
  const containers = new Map(replay.snapshot.state.containers.map((item) => [item.container_id, item.grain_grams]));

  for (const event of activeEvents) {
    if (event.event_type === 'grain.transferred.v1') {
      const source = String(event.payload.from);
      const destination = String(event.payload.to);
      const grams = Number(event.payload.grams);
      containers.set(source, (containers.get(source) ?? 0) - grams);
      containers.set(destination, (containers.get(destination) ?? 0) + grams);
    }
  }

  const residents = replay.snapshot.state.residents.map((snapshotResident, index): Resident => {
    const movement = replay.events.filter((event) =>
      event.event_type === 'resident.moved.v1' && event.payload.resident_id === snapshotResident.resident_id
    );
    const keyframes = [
      { time: replay.snapshot.state.sim_time, x: snapshotResident.x_millimetres, y: snapshotResident.y_millimetres },
      ...movement.map((event) => ({
        time: effectiveEventTime(event),
        x: Number(event.payload.x_millimetres),
        y: Number(event.payload.y_millimetres),
      })),
    ];
    let previous = keyframes[0];
    let next = keyframes[0];
    for (const frame of keyframes) {
      if (frame.time <= simTime) previous = frame;
      if (frame.time > simTime) { next = frame; break; }
      next = frame;
    }
    const duration = Math.max(1, next.time - previous.time);
    const mix = next === previous ? 0 : Math.max(0, Math.min(1, (simTime - previous.time) / duration));
    const activityEvents = activeEvents.filter((event) =>
      event.event_type === 'resident.activity_changed.v1' && event.payload.resident_id === snapshotResident.resident_id
    );
    const activity = activityEvents.length
      ? String(activityEvents[activityEvents.length - 1].payload.activity)
      : snapshotResident.activity;
    return {
      ...snapshotResident,
      activity,
      color: colors[index % colors.length],
      character: characters[(index * 2) % characters.length],
      point: {
        x: (previous.x + (next.x - previous.x) * mix) / millimetresPerTile,
        y: (previous.y + (next.y - previous.y) * mix) / millimetresPerTile,
      },
      direction: { x: next.x - previous.x, y: next.y - previous.y },
    };
  });
  return { residents, containers, activeEvents };
}

function orientation(dx: number, dy: number) {
  if (Math.abs(dx) > Math.abs(dy)) return dx >= 0 ? 0 : 180;
  return dy >= 0 ? 90 : 270;
}

function formatClock(simTime: number) {
  const day = Math.floor(simTime / 86_400) + 1;
  const daySeconds = simTime % 86_400;
  const hour = Math.floor(daySeconds / 3_600);
  const minute = Math.floor((daySeconds % 3_600) / 60);
  return { day, time: `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}` };
}

function formatMass(grams: number) {
  return `${(grams / 1_000).toFixed(1)} kg`;
}

function eventPresentation(event: ReplayEvent, residents: SnapshotResident[]) {
  const resident = residents.find((item) => item.resident_id === event.payload.resident_id);
  if (event.event_type === 'resident.activity_changed.v1') {
    return { kind: 'ACTIVITY', text: `${resident?.name ?? 'A resident'} began: ${event.payload.activity}.` };
  }
  if (event.event_type === 'resident.moved.v1') {
    const x = Number(event.payload.x_millimetres) / 1_000;
    const y = Number(event.payload.y_millimetres) / 1_000;
    return { kind: 'MOVE', text: `${resident?.name ?? 'A resident'} reached tile ${x}, ${y}.` };
  }
  if (event.event_type === 'grain.transferred.v1') {
    return { kind: 'STOCK', text: `${formatMass(Number(event.payload.grams))} moved from ${event.payload.from} to ${event.payload.to}.` };
  }
  return null;
}

function ResourceMarker({ x, y, color }: { x: number; y: number; color: number }) {
  const draw = React.useCallback((graphics: PIXI.Graphics) => {
    graphics.clear();
    graphics.beginFill(color, 0.18);
    graphics.lineStyle(1, color, 0.85);
    graphics.drawCircle(0, 0, 14);
    graphics.drawCircle(0, 0, 4);
    graphics.endFill();
  }, [color]);
  return <Graphics x={x} y={y} draw={draw} />;
}

function World({ width, height, residents, selected, onSelect }: {
  width: number; height: number; residents: Resident[]; selected: string; onSelect: (id: string) => void;
}) {
  const app = useApp();
  const viewportRef = useRef<Viewport>();

  useEffect(() => {
    viewportRef.current?.moveCenter(24 * worldMap.tileDim, 16 * worldMap.tileDim);
    viewportRef.current?.setZoom(Math.max(0.8, Math.min(1.1, width / 1120)));
  }, [width, height]);

  return (
    <PixiViewport app={app} screenWidth={width} screenHeight={height} worldWidth={worldMap.width * worldMap.tileDim} worldHeight={worldMap.height * worldMap.tileDim} viewportRef={viewportRef}>
      <PixiStaticMap map={worldMap} />
      <Container>
        <ResourceMarker x={30 * 32} y={17 * 32} color={0xe3a866} />
        <ResourceMarker x={34 * 32} y={11 * 32} color={0xd9806c} />
      </Container>
      {residents.map((resident) => (
        <Container key={resident.resident_id}>
          <Character
            x={resident.point.x * 32}
            y={resident.point.y * 32}
            orientation={orientation(resident.direction.x, resident.direction.y)}
            isMoving={resident.direction.x !== 0 || resident.direction.y !== 0}
            isThinking={resident.resident_id === selected}
            isViewer={resident.resident_id === selected}
            textureUrl={folkSpritesUrl}
            spritesheetData={resident.character.spritesheetData}
            speed={resident.character.speed}
            onClick={() => onSelect(resident.resident_id)}
          />
          <Text x={resident.point.x * 32} y={resident.point.y * 32 - 29} text={resident.name} anchor={0.5} style={new PIXI.TextStyle({ fontFamily: 'monospace', fontSize: 10, fill: 0xf8f0db, stroke: 0x17170f, strokeThickness: 3 })} />
        </Container>
      ))}
    </PixiViewport>
  );
}

function DecemberPreview() {
  const stageRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 900, height: 650 });
  const [speed, setSpeed] = useState(4);
  const [elapsed, setElapsed] = useState(0);
  const [selected, setSelected] = useState('iven');
  const [replay, setReplay] = useState<Replay | null>(null);
  const [loadError, setLoadError] = useState('');

  useEffect(() => {
    loadReplay().then(setReplay).catch((error: Error) => setLoadError(error.message));
  }, []);

  useEffect(() => {
    const observer = new ResizeObserver(([entry]) => setSize({
      width: Math.max(320, Math.floor(entry.contentRect.width)),
      height: Math.max(420, Math.floor(entry.contentRect.height)),
    }));
    if (stageRef.current) observer.observe(stageRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let frame = 0;
    let previous = performance.now();
    const tick = (now: number) => {
      const delta = Math.min(100, now - previous) / 1_000;
      previous = now;
      setElapsed((value) => value + delta * speed);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [speed]);

  const timeline = useMemo(() => {
    if (!replay) return null;
    const start = replay.snapshot.state.sim_time;
    const end = Math.max(start + 1, ...replay.events.map(effectiveEventTime));
    const simTime = start + Math.floor((elapsed * 12) % (end - start + 1));
    return { simTime, ...projectionAt(replay, simTime) };
  }, [elapsed, replay]);

  if (loadError) return <main className="load-state"><b>Replay unavailable</b><p>{loadError}</p></main>;
  if (!replay || !timeline) return <main className="load-state"><b>Opening the event log…</b></main>;

  const clock = formatClock(timeline.simTime);
  const selectedResident = timeline.residents.find((resident) => resident.resident_id === selected) ?? timeline.residents[0];
  const visibleEvents = timeline.activeEvents
    .map((event) => ({ event, presentation: eventPresentation(event, replay.snapshot.state.residents) }))
    .filter((item) => item.presentation)
    .slice(-6)
    .reverse();
  const granary = timeline.containers.get('granary') ?? 0;
  const seedStore = timeline.containers.get('raised_seed_store') ?? 0;
  const resources = [
    { label: 'Granary', value: formatMass(granary), delta: 'canonical stock' },
    { label: 'Seed store', value: formatMass(seedStore), delta: 'canonical stock' },
    { label: 'Population', value: String(timeline.residents.length), delta: 'scripted bodies' },
    { label: 'Event chain', value: String(replay.manifest.event_count), delta: 'hash-linked events' },
  ];

  return (
    <main className="preview-shell">
      <header className="preview-header">
        <a className="preview-brand" href="/"><span className="preview-mark">D</span><div><b>DECEMBER</b><small>Wega Labs · Kernel-driven Day One</small></div></a>
        <div className="preview-clock"><span>DAY {clock.day}</span><strong>{clock.time}</strong><i>Early summer</i></div>
        <div className="header-actions">
          <a href="/book">Read the book ↗</a>
          <div className="speed-control" aria-label="Replay speed">
            {[1, 4, 12].map((value) => <button key={value} className={speed === value ? 'active' : ''} onClick={() => setSpeed(value)}>{value}×</button>)}
          </div>
        </div>
      </header>

      <section className="preview-grid">
        <div className="world-frame" ref={stageRef}>
          <Stage width={size.width} height={size.height} options={{ backgroundColor: 0x667a55, antialias: false }}>
            <World width={size.width} height={size.height} residents={timeline.residents} selected={selectedResident.resident_id} onSelect={setSelected} />
          </Stage>
          <div className="world-status"><span className="pulse" /> Kernel replay · {replay.manifest.contract_version}</div>
          <div className="world-help">Drag to pan · wheel to zoom · select a resident</div>
        </div>

        <aside className="observer-panel">
          <section className="fixture-note"><span>KERNEL-DRIVEN REPLAY</span><p>Every movement, task, stock, timestamp, and event below was exported by December’s deterministic Python kernel. Actions are scripted; cognition and ecology are not built yet.</p></section>
          <section>
            <div className="panel-heading"><span>Residents in view</span><b>{timeline.residents.length} / {timeline.residents.length}</b></div>
            <div className="resident-list">
              {timeline.residents.map((resident) => (
                <button key={resident.resident_id} className={selectedResident.resident_id === resident.resident_id ? 'selected' : ''} onClick={() => setSelected(resident.resident_id)}>
                  <i style={{ background: resident.color }} />
                  <span><b>{resident.name}</b><small>{resident.role}</small></span>
                  <em>→</em>
                </button>
              ))}
            </div>
            <div className="selected-task"><span>Canonical activity</span><b>{selectedResident.activity}</b><small>resident.activity_changed.v1</small></div>
          </section>
          <section>
            <div className="panel-heading"><span>World state</span><b>state {replay.snapshot.state_hash.slice(0, 8)}</b></div>
            <div className="resource-grid">{resources.map((item) => <div key={item.label}><span>{item.label}</span><b>{item.value}</b><small>{item.delta}</small></div>)}</div>
          </section>
          <section className="event-section">
            <div className="panel-heading"><span>Canonical event feed</span><b>{timeline.activeEvents.length} applied</b></div>
            <ol>{visibleEvents.map(({ event, presentation }) => {
              const eventClock = formatClock(effectiveEventTime(event));
              return <li key={event.event_id}><time>{eventClock.time}</time><div><span>{presentation!.kind}</span><p>{presentation!.text}</p><code>seq {event.sequence} · {event.event_id}</code></div></li>;
            })}</ol>
          </section>
        </aside>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(<DecemberPreview />);
