# News Image 18 November 2026 — v3

A newspaper front page summing up the world's news of Wednesday
18 November 2026, as one image (`entry.png`, 1024x1024).

## The page

**THE WORLD TODAY** — a splash-style broadsheet:

- **Lead:** a U.S. strike sinks five Iranian tankers in the Gulf;
  Iran hits back, oil spikes, markets tumble. One dominant photo of
  a burning tanker with a warship standing by, under a huge splash
  headline — "U.S. SINKS FIVE IRANIAN TANKERS".
- **Kerch Bridge hit:** a blast damages the crossing; traffic halted.
- **Gaza freezes:** cold claims lives as families shelter in tents.
- **Markets:** Dow tumbles, NASDAQ down 2%, oil surges.

## Design

Unlike a dense broadsheet, this page uses big headlines and short
labels only — no small body copy — so every story stays legible even
at ~300 px wide. The date (Wednesday 18 November 2026) is named in
the masthead dateline and the footer. All photos are photorealistic,
generated for this entry, and the layout is a single clear
composition.

## How it is built

- `compose.py` (Pillow, build-time only) composes `entry.png` from
  the photos in `assets/` and the layout in code. Run it with
  `python3 compose.py`; it is deterministic (two runs write identical
  bytes).
- `main.py` is the submitted entrypoint. It runs with the standard
  library alone and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (default `/output`).

## Files

- `main.py` — entrypoint (stdlib-only copy program)
- `compose.py` — build-time front-page composer
- `entry.png` — the front page (JPEG bytes, 1024x1024, < 1 MiB)
- `assets/` — the three photorealistic news photos
- `README.md`, `LICENSE` (MIT)
