# Animation contract

V2: **1536 × 2288**, 8 columns × 11 rows. Cell: **192 × 208**. 73 used cells; 15 unused cells must stay fully transparent.

| Row | State | Frames | Duration in milliseconds |
| --- | --- | ---: | --- |
| 0 | idle | 6 | 280, 110, 110, 140, 140, 320 |
| 1 | running-right | 8 | 120 × 7, 220 |
| 2 | running-left | 8 | 120 × 7, 220 |
| 3 | waving | 4 | 140 × 3, 280 |
| 4 | jumping | 5 | 140 × 4, 280 |
| 5 | failed | 8 | 140 × 7, 240 |
| 6 | waiting | 6 | 150 × 5, 260 |
| 7 | running | 6 | 120 × 5, 220 |
| 8 | review | 6 | 150 × 5, 280 |
| 9 | look 000–157.5 | 8 | pointer-driven poses |
| 10 | look 180–337.5 | 8 | pointer-driven poses |

Look poses move clockwise in screen coordinates: 000 is up, 090 right, 180 down, 270 left. The preview loops these poses at 150 ms for inspection; that loop is not a claim about pointer movement in the application.

`running` means active work/thinking, rather than foot-running. Classic idle uses approximately 100%, 50%, 0%, 30%, 70%, 100% eye aperture. First and last resting frames match exactly. Since v1.0.1, all six classic idle frames share the exact original body and alpha; only feathered, color-matched eye regions vary. A pixel-level regression check rejects body color changes.

## Production and acceptance

Original user-supplied references → image-generation strips → connected-component extraction → shared-scale registration → one chroma-edge cleanup pass → exact atlas → structural checks → motion and directional review → Pets service preflight.

The classic version retains all non-idle original rows. The 3D version was generated separately. No optical-flow or preview-only interpolation is used. The final PNGs are the source of the README animations.

## Limits

The platform fixes the number and duration of frames. The last locomotion frame has a longer hold. Near-cardinal secondary gaze axes in the classic version are subtle and were accepted with recorded review warnings. These are stylized discrete animations, not 60-fps skeletal models.

## Release policy

Changing visible art requires new previews, frame review, integrity hashes and a release note. Never change only a preview while leaving the installed atlas behind. Do not overwrite the classic edition with a different gait or art style; introduce a separately named variant for a substantial redesign.
