# Common blocks

English text to reuse almost verbatim in every generated prompt. Replace each `{PLACEHOLDER}` with the game's own content and delete the braces. The finished prompt must contain no braces at all (the checker treats any brace as a leftover placeholder), so write JS objects in words: "sim.input(slot, intent) with intent = steer, throttle".

Keep the wording, the numbers and the warnings unless the game makes them wrong. These blocks are already compressed: once filled in they take about 1,100 words, which leaves about 850 words for the game-specific parts (field, physics, rules, actions, AI, key context, director cuts, sounds, stats, test targets). Do not lengthen them. `example-kart-race.txt` shows every block filled in.

Spelling follows the reference (colour, initialised, metres). Plain ASCII only: straight quotes, `-` for ranges and dashes, `x` for "times", `->` for arrows.

---

## Title and pitch line (top of the prompt)

```
{Game Title}
Build a single-file HTML5 game, "{Game Title}": {one-line pitch: who plays, how many, what a match / race is} in pixel-art 3D on a floating voxel island. three.js r128 from cdnjs, everything else inline, no asset files, no build step for the player. three.js and Google Fonts need internet: load cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js, on error the same build from cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js, and if both fail show "three.js could not load - check your connection" in the stage; fonts fall back to system stacks.
```

## ARCHITECTURE

```
ARCHITECTURE

* Split sim from render. All game logic is one plain-JS sim in its own <script> block: no DOM, no THREE, no Date, no Math.random (seeded mulberry32), fixed step 1/120 s. API: createSim(seed, mode, level, {OPTIONS}), sim.step(), sim.input(slot, intent) with intent = {INTENT FIELDS}; sim.state is plain data; sim.events feeds sounds, captions and log. AI and humans write the same intents.
* The renderer reads state, interpolates the last two steps and never writes it. Accumulator loop, at most 8 steps per frame; game speed multiplies steps, not dt. Every phase has a maximum duration and a fallback transition.
* Expose window.GAME (createSim, runHeadless(seconds, opts) returning stats); the sim block must run unchanged in Node via vm, so tests step thousands of seconds without a browser.
```

## LOOK - rendering pipeline (first bullet)

```
* Render to a low-res target (2 px art pixels on wide stages, 1 px on phones; slider 1-6; NearestFilter, CSS image-rendering: pixelated), then a post pass: depth-based outlines, snap every pixel to one fixed 90-colour OKLab palette, ordered 4x4 Bayer dither. Orthographic camera with smooth azimuth / elevation / zoom, pixel-snapped in view space so voxels never shimmer. Sun shadow map; Day / Dusk / Night / Auto lighting. {NIGHT LIGHTS: how many and where, max 8} must be registered as point lights BEFORE the lights are initialised, otherwise night is pitch black; no point-light shadows. r128 has no CapsuleGeometry and no core mergeBufferGeometries; use renderer.outputEncoding.
```

## LOOK - island (second bullet)

```
* Island: a {SIZE} m slab of 1 m voxel columns with a rounded outline {plus satellites and bridges if the game needs them}; {TOP SURFACE} top (three tones from noise), {PATHS}, layered rock strata underneath, floating rocks; solid through the centre from any angle. A ground canvas paints {MARKINGS with dimensions}.
```

## LOOK - field / track / course (third bullet, game-specific)

```
* {Court / Track / Course}: {dimensions in m, fixed equipment with heights, animated parts, officials' furniture, a scoreboard with a canvas texture ({CONTENT}; redrawn only on change)}.
```

## LOOK - surroundings and doll's-house lift (fourth and fifth bullets)

```
* Surroundings: {N} tiered wooden stands ({WHERE}) with an instanced crowd in {SIDES}' colours who jump more at {BIG EVENTS}; {5-8 THEME PROPS}, palms, gulls, clouds in the sky shader.
* Doll's-house lift: {stands and other tall structures} are lift groups; a group the sight line from camera target to camera crosses below roof height slides up in 0.4 s (bounding-box test) and stops casting shadows; option "Stands lift away". Merge static meshes by material with a small inline merge (bake matrixWorld, concatenate attributes, castShadow after merging); {ANIMATED PARTS} stay separate.
```

## Actors section - rig and poses (PLAYERS / DRIVERS / FIGHTERS ...)

```
* Jointed box rigs: hips, torso, head with {HEADWEAR}, upper arms and forearms on shoulder and elbow groups, thighs and shins on hip and knee groups, a hand anchor. {SIDES: original names, two colours each, distinct after palette snapping}; different skin tones and hair styles.
* A pose function per state returns channels (hip height, torso pitch / twist, head, shoulders (pitch, roll), elbows, hips, knees, body offset, air height): {IDLE} breathes; run cycle from gait phase and speed; {6-12 GAME POSES, each with a 2-6 word body description}, celebrate, sad; {OFFICIAL POSES}. Keyframed ease-in-out, then a critically damped spring per channel so poses never snap. Feet stay on the ground: hip height from leg length when grounded. {OFFICIAL} turns their head to follow {OBJECT}.
```

## HUMAN CONTROL - modes, keys, touch

```
* Modes: Watch ({ALL SIDES} on autopilot, the default), {SIDE A}, {SIDE B}, Two players on one keyboard. A human slot overrides the autopilot for its own {ACTOR} only.
* P1: WASD move (Left Shift {MODIFIER}), {P1 ACTION KEYS}; P2: arrows (Right Shift {MODIFIER}), {P2 ACTION KEYS}; one player accepts both sets. {CONTEXT RULES: what each key does in which situation, how aiming works}. Read e.code, preventDefault Space and arrows, blur panel buttons after a click so Space never re-presses them. Movement is camera-relative. Input is ignored during {SCRIPTED PHASES}. An arrow bobs over each human {ACTOR}.
* Touch: {JOYSTICK / PAD} plus {BUTTON NAMES} buttons in a dock below the stage, only on (pointer: coarse); pointer capture, touch-action: none.
```

## CAMERAS

```
* Director (default): {CUTS for each phase of play}; fixed: {5-6 CAMERA NAMES}. Zoom in metres of visible width, aspect-corrected. Drag to turn, wheel / pinch to zoom, Q / E rotate, 1-6 pick, L light, P pause, N new {match / race}, M sound; a user drag pauses the director for 4 s.
```

## UI - layout, panel, stats, note

Heading: `UI (CSS tokens on :root, dark scheme; fonts: {DISPLAY}, {CONDENSED}, {BODY}, system fallbacks)`

```
* Masthead with {LIVE SCORE / STANDINGS}; a framed stage with the {SCORE BUG content}, {COUNTERS}, call-out captions, chips (paused / speed / camera / {OPTION} / quality tier) and the latest log line. Control panel on the right (below on phones): mode, level, {LENGTH OPTION}, {GAME OPTIONS}, speed 0.5x / 1x / 2x / 4x, New {match} / Pause; how-to-play; camera, light, turn / zoom, pixel size, Outlines / Dither / Raw 3D / Sound / Stands lift; {match} stats ({6-8 STATS}); {event} log; a "How it's drawn" note with the palette swatches. No horizontal scroll at 390 px.
```

## UI - sound

```
* Sound: Web Audio API only, off by default; create or resume the AudioContext in the click that enables it, otherwise it stays silent. {8-12 NAMED SOUNDS, each with a synthesis hint}, {AMBIENCE}, an occasional gull.
```

## SCOPE

```
SCOPE

* MUST: sim / render split, rendering pipeline, island and {FIELD}, {ACTORS} with rigs and poses, physics, all rules and calls, AI on every level, Watch + {ONE HUMAN MODE}, director and fixed cameras, panel, stats, log, sound.
* IF ROOM, only after every MUST works, cut in reverse order: Two players, touch dock, {GAME EXTRAS}, gulls, clouds, Auto light. Never cut a MUST for an IF ROOM item.
```

## PERFORMANCE

```
PERFORMANCE

* Target 30 fps at 2 px on a mid-range laptop with integrated graphics, 30 fps at 1 px on a recent phone. Budget: under 150 draw calls, InstancedMesh crowd, one 2048 shadow map (1024 on phones), at most 8 point lights. Below 28 fps over 2 s, step down: shadow map 1024 -> crowd every other frame -> {GAME-SPECIFIC CUT} -> art pixel +1 -> shadows off; show the tier in a chip. Never slow the sim.
```

## QUALITY BAR

```
QUALITY BAR

* Node tests, seeds 1-{N}: {N} {matches / races} per level in Watch, {M} per level in each human mode with a scripted bot on sim.input. Assert: no NaN or Infinity, no stuck phase ({PHASE max seconds, ...}), {RULE INVARIANTS}, and the same seed gives the same final state hash.
* Targets on Normal: {2-4 AVERAGES WITH RANGES}. Out of range: tune {KNOBS}, rerun; after 3 rounds report the measured values instead of hiding them.
* Browser: no console errors on load and after 60 s of Watch; every control and key works; touch dock only on coarse pointers; no horizontal scroll at 390 px; fps measured or marked unmeasured. Headless software GL is too slow for real-time checks: the renderer gets an error check and a screenshot only. Scan the file for personal data (emails, absolute paths) and broken characters before publishing.
```

## REPORT

```
REPORT

* End with an honest report: what is done; what was verified and how (test counts, averages, fps); what was not verified; what was simplified or cut (name the IF ROOM items dropped); known bugs.
```
