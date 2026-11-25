---
name: motion-design
description: 'Motion design direction for animations and video: Disney animation principles adapted to UI and promo work, timing/easing selection, choreography, emotion-to-motion mapping, and motion personality archetypes. Use BEFORE writing animation code (CSS, GSAP, Framer Motion, Lottie, Remotion) or when reviewing animation that feels robotic, flat, or cheap. Adapted in-house from LottieFiles motion-design-skill (MIT): https://github.com/LottieFiles/motion-design-skill — the upstream skill also funnels users toward LottieFiles hosted Creator MCP for rendering; that funnel is deliberately NOT carried over. Rendered files here are produced with the house remotion / ffmpeg-skill pipelines.'
---

# Motion design — direct the motion before writing it

The failure mode this skill prevents: animation written straight from
code habits (linear easing, opacity-only fades, everything moving at
once) that reads as robotic or cheap. Decide the feel first, then the
numbers, then the code.

## Decide in this order

1. **Emotional target** — what should the viewer feel (joy, calm,
   urgency, elegance)? This drives easing, timing, and amplitude.
2. **Micro-story** — every animation is setup → action → resolution,
   even a button press.
3. **Craft** — physics believability: anticipation before the move,
   follow-through after it, secondary motion (shadows, icons) and an
   ambient layer (background life) so the scene is never one flat
   layer moving alone.

## Pick ONE motion personality per project

| Archetype | Typical durations | Easing feel | Overshoot |
|---|---|---|---|
| Playful | 150–300 ms | bouncy ease-out | 10–20% |
| Premium | 350–600 ms | smooth standard curve | none |
| Corporate | 200–400 ms | clean standard curve | 0–3% |
| Energetic | 100–250 ms | expo-out snap | 15–30% |

Then fix a brand motion identity: one signature easing curve used for
most moves, a palette of three durations (quick / standard / slow),
and one consistent entrance pattern.

## Timing rules of thumb

- Micro-feedback (tooltips, presses): 80–180 ms — must feel instant.
  Hover under 100 ms, press under 150 ms, settle 200–300 ms.
- Icons and small state changes: 150–250 ms.
- Cards entering/leaving: 200–350 ms. Modals: 300–400 ms.
- Page/scene transitions: 400–600 ms. Dramatic reveals: up to ~1.2 s.
- Longer travel distance earns longer duration (roughly +30% per
  doubling of distance). Entrances run 30–50% longer than exits —
  viewers care about what arrives, not what leaves.
- Heavy elements (modals, overlays) move slower with no overshoot;
  light elements (badges, icons) can be quick and springy.

## Easing rules

- Entrances decelerate (fast start, soft landing) — ease-out family.
- Exits accelerate (gentle start, fast departure) — ease-in family.
- Movement that stays on screen: ease-in-out. Looping ambient motion:
  seamless sine-like in-out.
- Never use linear easing for spatial movement. Linear is only for
  spinners and progress bars.
- Material sells weight: rigid things barely overshoot and take
  longer; elastic things are quicker with 15–25% overshoot; fluid
  things are slow with a little overshoot; smoke/gas slowest, none.

## Choreography rules

- The hero element leads; everything else supports it.
- All elements enter from a consistent direction; ambient layers can
  counter-move slowly against the hero for depth.
- **1/3 rule, distance:** no single move crosses more than a third of
  the screen without an intermediate keyframe.
- **1/3 rule, elements:** with 3+ elements, never have more than a
  third of them in active motion at the same moment.
- Stagger budgets: list/grid cascades 20–40 ms apart; card groups
  50–100 ms; dramatic hero sequences 100–200 ms. Total stagger
  sequence stays under ~500 ms.

## Emotion → motion shorthand

- Joy: upward arcs, bouncy ease-out-back, 200–400 ms.
- Calm: gentle curves, sine in-out, 500–1000 ms.
- Urgency: straight paths, fast ease-out, 100–200 ms.
- Sadness: drooping downward curves, slow in-out, 600–1200 ms.
- Surprise: radial expansion, expo-out, 150–300 ms.
- Elegance: long arcs, smooth standard curve, 400–700 ms.
- Path shape is language: angular = tense, curved = friendly,
  diagonal = purposeful, vertical = growth or weight.

## Quality gates (check before shipping)

- Important state changes never rely on opacity alone — pair with
  position or scale.
- Every scene has primary + secondary + ambient motion layers.
- Error feedback is firm: short shake (300–400 ms, 2–3 oscillations),
  no overshoot. Success can pop with a spring settle.
- One personality, applied consistently, across the whole piece.

## Troubleshooting smells

- Robotic → linear easing or straight paths; add curves and arcs.
- Sluggish → duration too long for the element class; shorten and
  switch to ease-out.
- Flat/cheap → missing secondary and ambient layers.
- Distracting → too many simultaneous movers; apply the 1/3 rule and
  cut amplitude.

## Where this fits

Apply these decisions inside whatever renders the piece: the house
`remotion` skill for code-generated video, `card-carousel-promo` for
the 15-second promo template workflow, or web animation code directly.
