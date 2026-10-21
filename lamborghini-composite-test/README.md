# Urus-inspired image-plate compositing test

**Two-second feasibility test, not an approved realistic Lamborghini transformation.**
New project; original MOV, prior Remotion project and previous preview are unchanged.
Source interval: original frames 75–134 (approximately 2.5–4.5 seconds).

## What is rendered

Generated empty luxury-SUV cabin plate, recurrent RVM subject alpha with local can-hole repairs and reduced neutral chair residue, original RGB person, foreground cabin armrest occlusion, hand restored over armrest, source audio. No generated face, facial motion, clothing or body; no subject geometry changes or frame interpolation. Only the hair boundary outside the protected face rectangle receives wall-color decontamination. H.264/AAC encoding introduces ordinary compression.

The source camera looks up from desk height with the subject lower in the frame. A parked passenger-seat view with neutral daylight was chosen to fit that angle and source illumination. A generated matching plate avoids scraping an unlicensed third-party photograph. Its cabin details are **Urus-inspired, not a verified accurate Lamborghini Urus interior**. The plate is a generated asset, not a claim of a real vehicle photograph or a third-party copyright license.

Remotion performs layered composition, background brightness/saturation adjustment, seat contact shadow, foreground occlusion, audio synchronization and final export. There is no fake driving movement or zoom. RGB for the protected face region is compared with the source before lossy encoding. The source VFR timestamps differ from the test's 30fps grid by at most about 1.67 ms; audio starts at original 2.5 seconds.

## Quality decision

Do not extend this version to the full clip yet. Rendered contact-sheet inspection reveals residual hair/shoulder halos, imperfect forearm/armrest contact, and a static plate whose cabin identity and seat/body geometry are not verified. Can matte repairs are heuristic and may include background around fingers. The test is an actual environment composite, unlike the earlier source/mask diagnostic, but it does not meet the original requirement of being indistinguishable from real phone footage.

## Run independently

```bash
cd lamborghini-composite-test
npm ci
npm run typecheck
npm run studio -- --port=3001
npm run render
```

All 60 processed subject PNGs, the generated cabin and extracted audio are included so rendering does not require the earlier research environment. On this cloud machine node_modules reuses the prior project's installed pinned dependencies; a fresh checkout should use npm ci. remotion.config.ts uses /usr/bin/chromium if present. Output is out/urus-composite-test.mp4. Browser copy with faststart is published separately as preview/lamborghini-composite-test-v1.mp4.

`scripts/refine_masks.py` documents mask changes and needs the earlier local research outputs plus that project's Python venv to regenerate the PNGs. It is not needed to render the committed assets. `mask-refinement.json` records processing counts. Facial RGB checks and timestamp checks are in validation.json; those checks do not prove visual realism.
