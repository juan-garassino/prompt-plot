# Sending plot jobs from the gallery server

Status: **the single-layer path is built and tested; the job layer below is not.**

## What exists today

`scripts/gallery_serve.py --allow-plot` + `scripts/gallery_plotter.py`:

| | |
|---|---|
| `GET /plotter/state` | enabled · busy · paper · whether a frame has been traced · current job · log |
| `GET /plotter/layers?target=` | colour layers in that gcode with stroke and command counts |
| `POST /plotter/job` | `action: "frame"` or `action: "layer"` — **one** layer |
| `POST /plotter/stop` | request a stop |

Viewer **Plot** panel: layer chips, Trace frame, Send layer, Stop, live log.

Safety, all verified by request: off unless `--allow-plot`; `confirm: true` required;
target must resolve inside `gallery/` and end `.gcode`; bounds-checked before any
command goes out; **an ink job is refused until a frame has been traced in that same
process**. Loopback only.

**The gap:** a 4-pen plate is four separate clicks, with nothing tracking where you
are. That is fine for one layer and wrong for a real plate.

## The job layer

### 1. Job model

```python
Job = {
  "id": "j-20260921-143002",
  "target": "studio/convolutions/current/pp_convolutions_v1.gcode",
  "paper": "a5:landscape", "margin": 15.0,
  "layers": [0, 1, 2, 3],          # or a subset
  "batch_strokes": 400,            # 0 = whole layer in one go
  "state": "pending|framing|awaiting_swap|streaming|awaiting_rezero|paused|done|error",
  "cursor": {"layer": 1, "batch": 3, "stroke": 1200},
  "progress": {"layer": [1200, 1424], "overall": [3100, 5465]},
  "eta_min": 38,
  "log": [...]
}
```

Persist to `~/.promptplot/plot_jobs/<id>.json` after every batch. That file **is** the
resume point.

### 2. The sequence the server owns

```
frame (pen up)
  → for each layer:
       park (0,0) · WAIT for /plotter/continue   ← the human swaps the pen
       rapid pen-up to the layer's first drawn point
       for each batch of batch_strokes:
            stream
            if rezero_every hit: park (0,0) · WAIT for /plotter/continue
  → park (0,0), done
```

`awaiting_swap` and `awaiting_rezero` block the worker thread on a
`threading.Event`; `POST /plotter/continue` sets it. Nothing polls the machine while
waiting, and the serial port stays open.

### 3. Endpoints to add

| | |
|---|---|
| `POST /plotter/job` | gains `action: "plate"` — target, optional `layers`, `batch_strokes`, `rezero_every`, `confirm` |
| `POST /plotter/continue` | acknowledge a swap or re-zero and proceed |
| `POST /plotter/pause` | stop after the current batch, keep the job resumable |
| `POST /plotter/resume` | `{job_id}` — reopen the port and continue from `cursor` |
| `GET /plotter/jobs` | recent jobs with state, for the resume list |

`GET /plotter/state` grows `cursor`, `progress`, `eta_min` and `waiting_for`.

### 4. Why batching and re-zero

Leo loses position on long plots — it is in memory as an open issue and it is the
reason a 6-hour plate is currently not worth starting. Batching gives:

- a **clean stop point** — pause at a stroke boundary, never mid-stroke;
- a **drift check** — park at (0,0) every N strokes so the operator can see whether
  the head still agrees about the origin, and abort early if not;
- a **resume point** — `slice_stroke_range(bucket, s, e)` already exists and is what
  `plot layer --strokes S:E` uses, so resume is the same call with a different `s`.

### 5. ETA

Draw length ÷ ~1 m/min on Leo, plus a fixed cost per pen swap. `preview --stats`
already computes draw length; the gallery manifests already carry it (`d`), and
`gallery/PRINT.md` is sorted by it.

### 6. Finding the plate

Mostly done — the viewer filters "plottable only", and `PRINT.md` lists everything
plottable cheapest-first. Worth adding:

- sort the viewer by draw length / pen count, not just series;
- surface `~min on Leo` on the card (the manifest has it);
- a **Queue** button: add the plate on screen to an ordered list, then run the list.

Multi-plate queueing is the last thing to build, not the first — it only matters once
single-plate jobs run unattended, and they will not until batching and resume work.

## Order of work

1. `action: "plate"` + `awaiting_swap` + `/plotter/continue` — turns 4 clicks into 1.
2. Job persistence + `/plotter/resume`.
3. Batching + `rezero_every` + `awaiting_rezero`.
4. Progress + ETA in the panel.
5. Sort/filter by cost in the viewer.
6. Multi-plate queue.

## Constraints that carry over

- The frame gate stays. A job's first act is always the pen-up trace.
- One job at a time, one process owning the port. Never two readers on the serial
  port — that is how acks get stolen.
- Bounds-check every layer before streaming it, not just the first.
- `G0` = travel (pen up), `G1` = draw (pen down).
- Loopback only: this process moves a machine and writes files.
