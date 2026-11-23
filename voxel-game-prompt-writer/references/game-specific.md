# Game-specific parts

What to invent for each idea, how to name the sections, plausible starting numbers and the pitfalls worth writing into the prompt as rules.

## 1. Section names by genre

The order never changes. Only the names of the third to sixth sections (and the field bullet inside LOOK) follow the game.

| Genre | Field bullet in LOOK | Actors | Physics | Rules | Actions |
|---|---|---|---|---|---|
| Net / racket sports (volleyball, tennis, badminton, padel) | Court | PLAYERS | BALL AND PHYSICS | RULES | ACTIONS AND CONTACT |
| Team field sports (football, basketball, hockey, rugby) | Pitch | PLAYERS | BALL AND PHYSICS | RULES | ACTIONS AND CONTACT |
| Racing (kart, boats, bikes, carts) | Track | KARTS AND DRIVERS / BOATS AND CREWS | DRIVING PHYSICS | RACE RULES | DRIVING AND CONTACT |
| Golf family (mini golf, golf, croquet) | Course | PLAYERS | BALL AND PHYSICS | RULES | SHOTS AND CONTACT |
| Rolling / sliding targets (bowling, curling, bocce, billiards) | Lanes / Sheet / Table | PLAYERS | BALL AND PHYSICS / STONE AND PHYSICS | RULES | THROWS AND CONTACT |
| Arena / combat (sumo, jousting, pillow fight) | Arena | FIGHTERS | MOVEMENT AND PHYSICS | RULES | MOVES AND HITS |
| Throwing / shooting at targets (darts, archery, frisbee) | Range | PLAYERS | PROJECTILE AND PHYSICS | RULES | THROWS AND SCORING |

Fixed full order of headings in the prompt:
title line, pitch line, ARCHITECTURE, LOOK, {ACTORS}, {PHYSICS}, {RULES}, {ACTIONS}, AI, HUMAN CONTROL, CAMERAS, UI, SCOPE, PERFORMANCE, QUALITY BAR, REPORT.

A heading may carry a short note in brackets like the reference: `PLAYERS (four voxel athletes + a referee)`, `AI (all karts not driven by a human)`, `UI (CSS tokens on :root ...)`.

## 2. Island adaptations

The floating voxel island is always there. Adapt it, never drop it.
- Small field (court, lanes, arena): one slab, field in the middle, stands around.
- Long field (race track, golf course): a bigger main slab (100-140 m) plus 1-3 satellite islands linked by bridges or ramps; the track or holes wind across them.
- Several short holes (mini golf): 9 holes spread over terraces of one slab, or small islands joined by boardwalks; one hole visible at a time with the director.
- Water sports: a lagoon cut into the slab (water plane with a simple wave shader), the slab solid underneath.
- Falling off the island is a game event only if the game makes it plausible (racing, sumo); give it a call and a respawn time.

## 3. What to invent, section by section

Every item below needs concrete values in the prompt. When the idea does not say, choose plausible values, keep units consistent (m, s, m/s, m/s2 written as "m/s2" or "m/s per s"), and list the key choices in the outline as "Scelte fatte".

LOOK
- Field bullet: dimensions in metres, markings painted by the ground canvas, fixed equipment with heights, parts that animate (net, flags, windmill), officials' furniture, the scoreboard sign and exactly what it shows.
- Night lights: name them and how many (max 8): poles, lamp posts, lanterns.
- Surroundings: where the stands go, what the crowd reacts to, 5-8 props that fit the theme (no brand names), which structures are lift groups besides the stands (tunnel, tower, clubhouse).

ACTORS
- Sides with original names and two colours each that stay distinct after palette snapping (pick hues at least 60 degrees apart; avoid two greens).
- Equipment carried or driven (racket, club, kart) and how it attaches (hand anchor, seat).
- The game's poses: 6-12 states, each with a 2-6 word body description, plus celebrate, sad and the official's poses.

PHYSICS
- Integration rate (120 Hz default), gravity 9.81, drag, restitution, friction or rolling resistance, spin if it matters, wind if it fits (Calm / Breeze / Gale).
- Surfaces with their own values (sand, grass, ice, water, ramp).
- The aiming solver the AI and the human aim assist use (iterative, with drag), and what to do when no solution exists.
- What ends a play (ball dead, crossing the line, stopped for 0.5 s below 0.05 m/s ...).

RULES
- Scoring with 2-3 selectable lengths, win condition, tie-breaks, turn or serve order, side changes, fouls, tolerances in cm or s.
- Calls: 8-14 exact captions in capitals, the game's own (ACE, HOLE IN ONE, PHOTO FINISH, STRIKE ...).
- After-event sequence with timings (whistle, flag, celebrate, slump, N s to the next play) and what happens at the end: automatic new match (endless).

ACTIONS
- Every action: duration, contact window, reach radius or contact shape, outcome target and error model.
- Levels Easy / Normal / Pro as a small table of numbers (error, reaction time, top speed, probability of the hard move). These are the difficulty knobs the QUALITY BAR tunes.
- Occasional unforced errors so AI-vs-AI is not perfect.
- Particles tied to actions (sand puffs, sparks, splashes, divots).

AI
- How it predicts (sampled trajectory, racing line, shot simulation), how it scores candidate actions, roles inside a team, what it must never do (play out of turn, cross a line, drive the wrong way), and a recovery rule for stuck situations with a time limit.

HUMAN CONTROL
- Which actor the human drives and how the choice changes during play, the context rule for each key (one button does different things by situation), how aiming works (held direction, charge bar, drag), scripted phases where input is ignored, touch button names.

CAMERAS
- Director cuts for each phase of play and a list of 5-6 fixed cameras with names.

UI
- Score bug content, counters on the stage, game options in the panel (laps, holes, wind, length), 6-8 stats, what the log records.
- Sounds: 8-12 named sounds, each with a synthesis hint (noise burst + lowpass, sine sweep, oscillator with pitch LFO), one or two ambience loops.

SCOPE
- MUST: everything needed for one complete, rule-correct match in Watch and one human mode.
- IF ROOM: second human mode, touch dock, cosmetic extras (gulls, clouds, Auto light cycle, skid marks, extra props), in the order they would be cut.

PERFORMANCE
- One game-specific step in the degradation ladder (fewer particles, simpler water, lower crowd density).

QUALITY BAR
- N and M (runs per level and per human mode; 30-100 is usual), the max duration of every phase, the rule invariants, 2-4 balance averages with ranges, the knobs to tune.

## 4. Numeric anchors

Starting points, not truths. Adjust to the game and keep them consistent with each other.

- Air drag on light balls: exponential 0.10-0.20 per s; heavy balls 0.01-0.05.
- Restitution: beach ball on sand 0.15, tennis ball on court 0.75, golf ball on turf 0.4, on wood or stone 0.6, bowling pins 0.5.
- Rolling deceleration: golf green 0.5-0.7 m/s2, rough 2-3 m/s2, mini golf carpet 0.6-0.9 m/s2, bowling lane oil 0.1 then dry 0.3 m/s2, curling ice 0.08 m/s2.
- Hole capture (golf): ball drops if centre is within 5 cm of the cup centre (cup radius 5.4 cm) and speed below 1.3 m/s; lip-out above.
- Human running: 6-7 m/s sprint, 4 m/s jog, 0.25 s reaction on Pro, 0.45 s on Easy.
- Karts: top speed 18-22 m/s, 0 to top in 3-4 s, braking 10-12 m/s2, lateral grip 1.2-1.4 g asphalt, 0.6-0.8 g grass.
- Boats: top speed 12-16 m/s, water drag strong (speed halves in 2-3 s off throttle), turning radius 6-10 m.
- Jumps: vertical take-off 4-5 m/s for athletes; air time 0.8-1.0 s.
- Match lengths for an endless Watch mode: 3-8 minutes per match or race.

## 5. Pitfall bank

Pick the ones that apply and write them as rules in the right section, in the reference's style ("X must ... BEFORE ..., otherwise ...").

- Point lights must be registered before the lights are initialised, otherwise night is pitch black; keep at most 8 and no point-light shadows.
- three.js r128 has no CapsuleGeometry and no core mergeBufferGeometries; renderer.outputEncoding, not outputColorSpace.
- Low-res target: NearestFilter, no mipmaps, CSS image-rendering: pixelated; rebuild it on resize and devicePixelRatio change.
- Pixel snapping: snap the camera target in view space to the size of one art pixel, or static voxels shimmer.
- Canvas textures (scoreboard, number plates): redraw and set needsUpdate only when the content changes.
- InstancedMesh crowd: frustumCulled false or a correct bounding sphere, otherwise the whole crowd vanishes at some angles.
- Springs and poses run on real frame time clamped to 0.05 s; the sim runs on the fixed step. Never mix them.
- Space re-presses the last clicked panel button unless buttons are blurred after a click; preventDefault Space and arrows so the page does not scroll.
- AudioContext starts suspended until a user gesture: create or resume it in the click that turns sound on.
- Every phase needs a maximum duration and a fallback transition (serve, positioning, countdown, aiming), otherwise Watch mode can stall forever.
- A ball, kart or player can tunnel through thin walls at 120 Hz if it moves more than its radius per step: sub-step or sweep fast objects.
- The AI must never use information a human could not have (no reading the human's next input).
- Determinism: no Math.random, no Date, no iteration over object keys whose order depends on insertion timing inside the sim.
