# How does a robot see you? - Science is Wonderful! 2027

An interactive booth proposal by TUAI doctoral candidates DC5 (sensor fusion) and DC7 (explainable AI) for the MSCA *Science is Wonderful! 2027* fair. The call deadline is **Tue 6 Oct 2026, 12:00 CEST**.

A small robot dog builds a picture of a visitor from its camera and microphone. Children switch its senses on and off and see what it knows, how sure it is, why it thinks so, and what it will never guess.

## Published links (private, share from each page's Share menu)

- Proposal for partners (with the demo video): https://claude.ai/artifact/RcbS2WeTLhfcNqHeaH3Sx4
- Interactive demo (exhibition screen, 6 recorded visitors): https://claude.ai/artifact/QtTQJbyT2cXppcQX7hR9Xf

## Deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | Concise proposal for partners | `docs/proposal/proposal.html` (published as an artifact) |
| 2 | Technical architecture + diagram | `docs/02_architecture.md`, `docs/assets/architecture.png` |
| 3 | Hardware recommendation, BOM, budget | `docs/03_hardware.md` |
| 4 | Prototype methodology and results | `docs/04_methodology.md`, `prototype/experiments/results/` |
| 5 | Working prototype (code, interactive demo, live mode) | `prototype/` (start with `prototype/README.md`) |
| 6 | Exhibition walkthrough (3-min round, 15-min group module) | `docs/06_exhibition_walkthrough.md` |
| 7 | Demo video (3 min 31 s, with the visitors' own voices) + storyboard | `prototype/video/out/how_does_a_robot_see_you.mp4`, `storyboard.md` |
| + | SIW application pack (form texts with measured lengths, video script, checklist) | `docs/08_siw_application_pack.md`, `docs/assets/booth_sketch.png` |
| + | Ethics, privacy and child safety | `docs/09_ethics_privacy.md` |
| + | Verified desk research with sources | `research/01-10` |
| + | Design brief (single source of truth) | `docs/_brief.md` |

## Folder map

```
docs/        proposal, deliverable documents, sketch and diagrams
prototype/   robotsees package, experiments, exhibition screen (demo/), live mode, video renderer, tests
research/    10 verified research reports (call, robots, audio, vision, generative, XAI, datasets, law, exhibition)
data/        (not in git) downloaded public data subsets - re-create with prototype/tools, see DATA.md
models/      (not in git) OpenVINO LCM + TAESD, Piper voice - re-create with prototype/tools/fetch_models.py
```
