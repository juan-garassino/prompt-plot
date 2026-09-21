# reconstructions — reference plates rebuilt as authored Scenes

Each folder is one reference image reconstructed with the engine
(`studio/AUTHORING.md` is the method). Oracle results, where they exist, are in
`gallery/references/oracles/` for comparison. **Nothing here is traced.**

## Built

| plate | vocabulary it exercises | build |
|---|---|---|
| `latent-topography/` | `radial_nest` masses · `contour_nest` funnels · `dissolve` forward row · `hourglass_ring` U-Net · `dot_cloud` · `ribbon` | `python studio/reconstructions/latent-topography/build.py [out.png]` |
| `gan-plate/` | `rounded_rect_ring` + `radial_burst` panels · `radial_nest` masses · `dot_cloud` latent · `ribbon` flows | `python studio/reconstructions/gan-plate/build.py [out.png]` |

These two share one vocabulary and differ only in composition — that is the
generality claim, and the reason the form layer exists.

## Briefed, not yet built

`cubist-repro/` · `engraving-repro/` · `acrylic-repro/` — the three oracle
targets, each with its reference at `<slug>/ref/reference.png`. Run either seat:

    promptplot studio design cubist-repro --mode scene --rounds 4 --provider <p>
    # or author the Scene in conversation and: promptplot scene render scene.json

The engraving is the deepest: four nibs, `surface_grid` skin, `flow_family` hair
with a travelling highlight, protected eyes and lips. Expect it to drive most of
the tuning in `engine/material.py`.
