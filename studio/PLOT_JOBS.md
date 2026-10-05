# Sending plot jobs from the gallery server

Status (2026-09-28): **steps 1–4 of the job layer are built and tested** — plate
jobs, pen-swap waits, persistence + resume, batching + re-zero checks, progress + ETA
in the panel. Steps 5–6 (sort by cost, multi-plate queue) are not. See "What is built"
right below; the design sections after it are kept as the spec they were built from.

## What is built (steps 1–4)

One engine, `promptplot/plotjob.py`, two seats:

- **Server** — `POST /plotter/job {action: "plate", target, layers?, batch_strokes?,
  rezero_every?, max_feed?, min_dwell?, confirm}` · `POST /plotter/continue {wait_seq}` ·
  `POST /plotter/pause` · `POST /plotter/resume {job_id, retrace?, confirm}` ·
  `GET /plotter/jobs`. `GET /plotter/state` carries `waiting_for`, `cursor`, `progress`,
  `eta_min`. Viewer Plot panel: **Plot plate** (batch / re-zero inputs), the wait
  message, **Continue / Pause / Stop**, a progress bar with layer · strokes · plate ·
  ETA, and a resumable-jobs list with **Resume**.
- **Terminal** — `promptplot plot plate FILE.gcode [--layers 0,2,3] [--batch-strokes 400]
  [--rezero-every 2000] [--max-feed 500] [--min-dwell 1.0] [--resume JOB_ID] [--retrace]
  [--jobs] [--port …] [--paper a5:landscape] [--margin 15] [--dry-run]`. Enter continues
  a wait, `p` pauses, `s` stops; Ctrl-C once = pause after this batch, twice = stop now.
  `--dry-run` rehearses the whole sequence on the simulator.

**The sequence** (both seats): refuse unless every selected layer fits the paper →
open the port → [resume: pen up, WAIT `awaiting_rezero` — reopening the port re-zeroes
Grbl where the head sits] → frame trace pen up (first act of a fresh job) → per layer:
[pen changes] `M5`, dwell, `G0 X0 Y0`, `G4 P0.5` (the ack means the head is home) →
WAIT `awaiting_swap` → pen-up `G0` to the batch's first drawn point → batches through
`stream_chunk(enforce_pen_state=True)` → job file saved → [pause asked] park, `paused`
→ [`rezero_every` reached] park, WAIT `awaiting_rezero`, pen-up approach → … → park
(0,0), `done`. Consecutive runs of the same colour do not wait for a swap. A swap wait
counts as a re-zero check.

**Not saturating Leo.** Nothing in the job layer writes to the port: every line goes
through `SerialPlotter.send_command` (`promptplot/plotter.py`), which holds `_io_lock`
across write + `readline` — send one line, wait for its `ok`. One line in flight means
Grbl's 128-byte RX buffer cannot overflow, and Grbl holds the `ok` until the line fits
its planner, so the controller sets the pace. The heartbeat is off, so the ack loop is
the only reader; HTTP threads only set `threading.Event`s; a `flock` on
`~/.promptplot/plot_jobs/plotter.lock` keeps a terminal job and a server job (or its
frame/layer jobs) off the port at the same time. Batches are the stop / drift-check /
resume granularity, not flow control, and always end on a stroke boundary. A failed or
timed-out ack **aborts** (pen up retried, park) rather than carrying on — a lost `ok`
shifts every later ack by one line.

**Leo-safe defaults** (memory: slow feeds, long dwells): every draw is capped at
F500 and carries an explicit `F` (a resumed batch cannot lean on a modal feed lost in
the reconnect reset); every `G4` is floored at 1.0 s. `--max-feed 0 --min-dwell 0`
streams the file as-is.

**ETA** = Σ draw length ÷ each draw's (capped) feed + travel ÷ 2000 mm/min + the file's
`G4` dwells (or 2.0 s per pen cycle when it has none) + 90 s per pen swap + 20 s per
re-zero check, × a measured pace (stream wall time ÷ modelled time, once a minute of
drawing has been streamed). The 600/2000/2.0 constants are `gallery_index.py`'s
(`PRINT.md`); 90 s and 20 s are guesses — correct them after the first real plate.

**Resume.** `stopped`, `paused` and `error` jobs are resumable; the file's sha256 must
still match. A stop mid-batch rewinds the cursor to the stroke that was being drawn
(redrawn once — better than a half-missing stroke). The server resumes only on the
paper it was started on, and only with a frame traced in this process or `retrace: true`;
the terminal resume relies on the job's own earlier trace unless `--retrace`. Both wait
for the origin check before anything moves. `continue` must name the wait on screen
(`wait_seq`), so a double click cannot acknowledge the next pen swap.

Tests: `tests/test_plotjob.py` (stub plotter, no hardware).

### Follow-ups the job layer could not do (files it must not touch)

- `GCodeCommand.from_string` parses `P` as `int`: `G4 P0.2` loads as `G4 P0`, so every
  gcode streamed through `FilePipeline` (`plot layer`, the server's layer job) loses its
  pen dwells. The plate job's dwell floor masks it; the loader should keep a float.
- `SerialPlotter.send_command` ack timeout is fixed per plotter (60 s here). Grbl acks a
  `G4` only after the planner drains, so a very long queued move before a dwell could
  still time out; an adaptive timeout (length ÷ feed × 2 + 2 s) belongs in `plotter.py`.
- Travel speed: `G0` runs at Grbl's `$110/$111` max rate. Slowing rapids for Leo is a
  firmware setting — do not turn travels into `G1` (the pen guardrail would ink them).
- `split_color_layers` returns contiguous runs; a colour that appears twice is two
  layers (two swaps) in file order. `--layers` groups a colour's runs together.
- `plot frame` / `plot layer` from the terminal do not take the plotter lock.


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

1. ~~`action: "plate"` + `awaiting_swap` + `/plotter/continue` — turns 4 clicks into 1.~~ built
2. ~~Job persistence + `/plotter/resume`.~~ built
3. ~~Batching + `rezero_every` + `awaiting_rezero`.~~ built
4. ~~Progress + ETA in the panel.~~ built
5. Sort/filter by cost in the viewer.
6. Multi-plate queue.

## Constraints that carry over

- The frame gate stays. A job's first act is always the pen-up trace.
- One job at a time, one process owning the port. Never two readers on the serial
  port — that is how acks get stolen.
- Bounds-check every layer before streaming it, not just the first.
- `G0` = travel (pen up), `G1` = draw (pen down).
- Loopback only: this process moves a machine and writes files.
