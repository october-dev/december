# December observer

The read-only browser adapter for December's canonical kernel. It displays the
`december.observer.v1` snapshot and JSONL event stream in `public/data/` and has
no write path back to the simulation.

```sh
npm install
npm run dev
npm run build
```

Regenerate the replay at the repository root, then refresh the viewer copy:

```sh
PYTHONPATH=src .venv/bin/python examples/founding_valley_day_one.py
cp artifacts/founding-valley-day-one/* viewer/public/data/
```

The first visual layer selectively ports MIT-licensed renderer code from
[a16z-infra/ai-town](https://github.com/a16z-infra/ai-town) commit `7b24233`.
It does not contain Convex, Clerk, AI Town's agent loop, model providers, memory
store, or backend. See `third_party/AI-TOWN-LICENSE` and `THIRD_PARTY.md`.
