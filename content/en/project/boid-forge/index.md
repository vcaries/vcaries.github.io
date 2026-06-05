---
draft: false
title: "BoidForge: Engineering Collective Behavior from Python to Native C"
summary: "How do you turn a textbook flocking model into a simulation that scales to tens of thousands of agents and renders like a fluid? This case study walks through the boids algorithm, four progressively faster solver backends benchmarked side by side (up to about 330 times faster than naïve Python), and a GPU visualization engine built with ModernGL."
authors:
  - admin
tags:
  - Scientific Python
  - Python
  - C / CPython C-API
  - NumPy
  - High-Performance Computing
  - ModernGL
  - GPU
  - Simulation
  - Optimization
date: '2026-06-05T00:00:00Z'
toc: true

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: 'A 4K render of the BoidForge turbulence scene, coloured by speed'
  focal_point: Smart
  preview_only: false

links:
url_code: 'https://github.com/vcaries/boid_forge'
url_pdf: ''
url_slides: ''
url_video: 'https://youtu.be/5iVkLb3eyhE'
---

## In one minute

**BoidForge** is a 2D flocking simulator built around a single principle: a swarm is *computed* once and *rendered* afterwards, never both at the same time. A **solver** advances the physics and streams every timestep to a compact binary file. A separate **visualization engine** then replays that file on the GPU. The two halves share no memory, only an on disk format, so each one can be optimised on its own.

The result is a project that is equal parts numerical computing and real time graphics. The same flocking model is implemented in **four interchangeable backends**, ranging from a naïve Python reference to a hand written **C extension**, and all four are proven to produce strictly identical results down to the last bit. A **ModernGL** renderer then turns the raw trajectories into the cinematic footage below.

{{< youtube 5iVkLb3eyhE >}}

<figcaption style="text-align:center;font-size:0.9em;margin-top:0.5em;"><strong>Video.</strong> The <em>turbulence</em> scene, rendered offline in 4K at 60&nbsp;fps and coloured by speed. It was produced by replaying a recorded simulation through the GPU visualization engine described further down.</figcaption>

👉 **[Source code on GitHub](https://github.com/vcaries/boid_forge)**

### Highlights

- **One model, four backends, identical output.** Naïve Python (L1), vectorized NumPy (L2), a uniform grid spatial hash (L3), and a native C/CPython kernel (L4), all bit for bit identical under a strict determinism contract.
- **Up to about 330 times faster.** The C backend reaches roughly 120 to 330 times the throughput of the naïve reference over the benchmarked range, and is designed to scale to tens of thousands of agents.
- **GPU visualization in ModernGL.** Instanced point sprites, additive HDR accumulation, motion trails, bloom, and ACES tone mapping, rendered without a display and streamed straight to FFmpeg for 4K export.
- **Reproducible by construction.** Every result is a pure function of the configuration and a seed, so the same inputs give the same bytes on any machine.

## Inspirations

This project grew out of two pieces of online science and engineering culture. The first is **Smarter Every Day**, whose [film on starling murmurations](https://www.youtube.com/watch?v=4LWmRuB-uNU) captures how thousands of birds can behave like a single fluid body, and asks the natural question of how such order can emerge with no leader and no plan. The second is **Sebastian Lague** and his *Coding Adventures* series, whose [episode on boids](https://www.youtube.com/watch?v=bqtqltqcQhw) shows how a few local rules translate into code and how much visual beauty a simple simulation can hold. BoidForge is my attempt to take that curiosity seriously as an engineer: to reproduce the phenomenon faithfully, to push it to a scale where the emergence becomes obvious, and to render it well enough to do the real murmurations justice.

## The flocking model

Flocking is an *emergent* behaviour. There is no leader and no global plan, yet thousands of agents organise themselves into coherent, fluid looking motion. The classic formulation is Craig Reynolds' **boids** model (1987), in which every agent obeys three local steering rules, each computed only from the neighbours that lie within a given radius.

Let agent $i$ have position $\mathbf{p}_i$ and velocity $\mathbf{v}_i$. Write $\mathcal{N}_i$ for the set of its neighbours inside the radius of the rule being evaluated. Each rule produces a steering acceleration.

**Separation** keeps the swarm from collapsing on itself. Each agent is pushed away from its close neighbours, and the push grows stronger the closer they are:

$$\mathbf{a}_{\text{sep}} = w_{\text{sep}} \sum_{j \in \mathcal{N}_i} \frac{\mathbf{p}_i - \mathbf{p}_j}{\lVert \mathbf{p}_i - \mathbf{p}_j \rVert^{2}}$$

The inverse square weighting is the important detail: a neighbour at half the distance repels four times as hard, which is what spaces the agents out and prevents collisions.

**Alignment** makes neighbours travel together, by steering each agent towards the average velocity $\overline{\mathbf{v}}$ of its neighbourhood:

$$\mathbf{a}_{\text{ali}} = w_{\text{ali}} \left( \overline{\mathbf{v}} - \mathbf{v}_i \right)$$

**Cohesion** holds the group together, by steering each agent towards the local centre of mass $\overline{\mathbf{p}}$ of its neighbourhood:

$$\mathbf{a}_{\text{coh}} = w_{\text{coh}} \left( \overline{\mathbf{p}} - \mathbf{p}_i \right)$$

The three contributions are summed into a single acceleration $\mathbf{a}_i$, whose magnitude is capped at a maximum steering force. The velocity is then advanced by one explicit Euler step and clamped to a speed band $[v_{\min}, v_{\max}]$ so that agents never freeze or run away:

$$\mathbf{v}_i \leftarrow \mathbf{v}_i + \mathbf{a}_i \Delta t$$

Finally the position is advanced with that new velocity, and a boundary rule (wrap around or reflect) keeps the swarm inside the world:

$$\mathbf{p}_i \leftarrow \mathbf{p}_i + \mathbf{v}_i \Delta t$$

Each rule uses its **own radius**, and the three weights $w_{\text{sep}}$, $w_{\text{ali}}$, $w_{\text{coh}}$ give a run its character. Tuning them is what produces the *murmuration*, *schooling*, *plasma*, and *turbulence* scenes in the repository. The model is short to state. The engineering work is in making it fast and reproducible.

## The computational bottleneck

The cost of the model is dominated by one question. For each agent, which other agents are its neighbours? Answered naïvely, every agent is compared against every other, which means $O(N^2)$ distance calculations per timestep. At a few hundred agents this is harmless. At tens of thousands it is hopeless, because quadratic growth means a swarm ten times larger costs a hundred times more.

BoidForge attacks the problem along two independent axes, and gives each one its own backend so that the contribution of every idea can be *measured* rather than assumed:

1. **Lower the constant factor.** Do the same $O(N^2)$ work, but express it in fewer and faster instructions. This is the path from a Python loop to vectorized NumPy and then to native C.
2. **Lower the complexity.** Stop doing $O(N^2)$ work at all, by only ever inspecting agents that could plausibly be neighbours. This is the spatial grid, which brings the search down to roughly $O(N)$.

All four backends are held to a single **determinism contract**: for the same configuration and seed, they must emit byte for byte identical output. The naïve backend is the reference, and any backend that disagrees with it is wrong by definition. A test runs every backend and compares their frames. This is a demanding constraint, because it forces even the C kernel to reproduce NumPy's exact `float32` summation order, but it is what makes the speedups trustworthy instead of merely fast.

## Four backends, and what each one buys

### L1, naïve Python (the reference)

A direct all pairs implementation, with an explicit Python loop over every pair of agents. It is deliberately simple, because its only job is to *define correctness*. Every other backend is validated against it. It is also, predictably, the slowest, since the per element overhead of the Python interpreter sits on top of the $O(N^2)$ work.

### L2, vectorized NumPy

The same all pairs algorithm, re expressed with NumPy. The pairwise displacement, distance, and separation terms are built once as whole arrays, and the clamping and integration run as bulk array operations.

*Why it is faster.* The arithmetic moves out of the Python interpreter and into NumPy's compiled C loops, which removes the per element interpreter overhead. On small and medium swarms this is roughly a twofold gain. It is not free, however. The pairwise arrays cost $O(N^2)$ *memory*, and at the top of the benchmarked range the cost of moving those large arrays through memory cancels the gain, to the point where L2 is marginally slower than L1 at 2000 agents. That trade off is the lesson in itself: vectorization buys speed with memory, and at scale memory becomes the limiting resource.

### L3, uniform grid spatial hash

The first *algorithmic* change. Agents are sorted into a grid whose cell side equals the neighbour radius. Each agent then inspects only its own cell and the eight cells around it, a three by three block, instead of the whole swarm. Because the cell side equals the radius, any genuine neighbour is guaranteed to fall inside that block, so the grid prunes work without ever missing a neighbour.

*Why it is faster.* It changes the complexity of the neighbour search from $O(N^2)$ to about $O(N)$. The work per agent stops growing with the size of the swarm and depends only on the local density. This is the idea that makes large swarms tractable in principle. In pure Python, though, the bookkeeping of building the grid and gathering candidates carries enough overhead that, at the modest sizes benchmarked here, its timing stays close to the naïve loop. The algorithm is correct, but it is waiting for a faster host language to pay off.

### L4, native C extension (the production target)

That faster host is a hand written **CPython C extension**, written against the raw C API and built with CMake through scikit-build-core. It combines the $O(N)$ grid of L3 with a set of systems level optimisations that Python cannot offer:

- **Struct of Arrays buffers, shared without copying.** The state lives as four contiguous `float32` arrays (positions and velocities) shared with NumPy through the buffer protocol. There is no copy, no per agent object overhead, and a memory layout the processor can stream through efficiently.
- **A counting sort into cells.** The grid is built with a counting sort into a compact layout rather than a hash map, so gathering neighbours is a tight loop over contiguous indices instead of dictionary lookups.
- **The interpreter lock is released** around the compute loop, so the heavy numerical work runs as genuine native code, free of the Python global interpreter lock.
- **No memory allocation inside the hot loop.** A single workspace is sized once per timestep, and the inner per agent loop never calls the allocator.

*Why it is faster.* Each of these removes a layer of overhead that the Python backends cannot escape, namely interpreter dispatch, object indirection, and allocator pressure, while keeping the $O(N)$ neighbour search. Together they deliver roughly 120 to 330 times the throughput of the naïve reference and put tens of thousands of agents within reach. It does all of this while still producing output identical to L1 down to the bit, which required reproducing NumPy's pairwise summation algorithm exactly in C so that the `float32` rounding matches.

## Benchmarks

The harness times each backend across a sweep of swarm sizes, from 100 to 2000 agents, over 200 steps each and after a warm up, recording the mean time per frame and the speedup relative to L1.

<figure>
  <a href="/media/boid-forge/scaling.png" target="_blank" rel="noopener"><img src="/media/boid-forge/scaling.png" alt="Per-frame time versus number of agents, log-log, for the four backends" style="width:100%;height:auto;"></a>
  <figcaption><strong>Figure 1.</strong> Time per frame against swarm size, on logarithmic axes. The naïve (L1), vectorized (L2), and Python spatial hash (L3) backends sit close together at these sizes, while the native C backend (L4) runs one to two orders of magnitude below them. The gap widening towards the right is the $O(N)$ grid pulling away from the $O(N^2)$ all pairs cost. <em>(Click to enlarge.)</em></figcaption>
</figure>

<figure>
  <a href="/media/boid-forge/speedup.png" target="_blank" rel="noopener"><img src="/media/boid-forge/speedup.png" alt="Speedup of each backend relative to the naïve baseline, per swarm size" style="width:100%;height:auto;"></a>
  <figcaption><strong>Figure 2.</strong> Speedup over the naïve baseline. The native backend dominates, peaking around 330 times at 200 agents and holding well above 100 times across the range, while the pure Python optimisations (L2 and L3) stay close to 1 at these sizes. This confirms that the decisive gain comes from moving the $O(N)$ algorithm into C, and not from vectorization on its own.</figcaption>
</figure>

At 2000 agents the naïve reference spends about 202 ms per frame, the equivalent of roughly 5 frames per second, while the C backend spends about 1.7 ms, the equivalent of roughly 590 frames per second. That is the same physics computed about 120 times faster, with its lead still growing as the swarm gets larger.

## Visualization with ModernGL

The renderer never simulates. It reads precomputed frames from the binary stream and turns each one into an image on the GPU. It is built directly on **ModernGL**, a thin modern binding to OpenGL 3.3, with hand written GLSL shaders, and it is deliberately a small post processing pipeline rather than a game engine:

1. **Upload and draw.** Each frame is uploaded to a GPU vertex buffer and every agent is drawn as a single **point sprite**. The fragment shader shapes each sprite into a soft glowing core surrounded by a wide halo, and its colour is read from a small colour map texture indexed by speed, heading, local density, or a fixed value.
2. **Additive HDR accumulation.** Sprites are blended additively into a floating point buffer, so overlapping agents build up genuine brightness. This is what gives dense clusters their luminous look.
3. **Motion trails.** Instead of clearing that buffer between frames, it is faded slightly towards black. Agents therefore leave decaying trails behind them, which is the source of the silky, fluid sense of motion.
4. **Bloom.** A bright pass keeps only the most luminous pixels, a separable Gaussian blur spreads them out, and the glow is added back, producing the cinematic halo around fast and crowded regions.
5. **Composite.** A final fullscreen shader applies an ACES filmic tone map to bring the high dynamic range scene into a displayable range, together with exposure, an optional vignette, the background tint, and gamma correction.

Because the GPU context can be created off screen, the very same renderer runs without a display on a headless machine. For video, the rendered frames are streamed straight into an **FFmpeg** subprocess that encodes H.264, without ever holding the whole clip in memory. That is how the 4K footage at the top of this page was produced.

## Architecture: two subsystems, one contract

The design rule behind everything above is a strict separation between *computing* the swarm and *drawing* it:

```
Solver (compute)  --->  .bfs binary stream  --->  Visualization engine  --->  frames / video
```

The solver imports nothing from the visualization layer, with no OpenGL and no graphics of any kind, and the visualization layer never advances the physics. Their only shared knowledge is a small versioned **binary format** (`.bfs`): a 32 byte header followed by one record per frame holding the agent count and the four `float32` arrays back to back. That layout is chosen so the solver can write each array in a single bulk operation and the renderer can map it straight into a GPU buffer with no repacking on either side. A static test on the import boundaries enforces the separation so that it cannot erode over time.

This decoupling is what lets the solver be tuned for raw throughput and the renderer for image quality, each on its own terms. It is also why a long simulation can be computed once and then re rendered later with different colours, trails, or resolution as many times as needed.

## Skills demonstrated

- **High performance computing:** algorithmic complexity reduction from $O(N^2)$ to $O(N)$ with spatial hashing, NumPy vectorization and its memory trade offs, and a hand written CPython C extension with zero copy buffers, interpreter lock release, and an allocation free hot loop.
- **Numerical rigour:** a bit exact determinism contract across four independent implementations, including reproducing NumPy's `float32` pairwise summation in C.
- **GPU and real time graphics:** a ModernGL and GLSL pipeline with HDR accumulation, motion trails, bloom, and ACES tone mapping, running headless and exporting through FFmpeg.
- **Software architecture:** two strictly decoupled subsystems joined only by a versioned binary format, with an enforced import boundary.
- **Engineering discipline:** typed, documented, and tested Python (`ruff`, `mypy --strict`, `pytest`), a CMake and scikit-build-core native build, and reproducibility treated as a first class requirement.

## Repository

The full source is open, including the four solver backends, the C kernel, the binary input and output layer, the benchmark harness, and the ModernGL visualization engine.

The code lives at **[github.com/vcaries/boid_forge](https://github.com/vcaries/boid_forge)**, alongside an architecture document that describes the binary format and the determinism contract in full.

## Conclusion

A flocking model is three lines of vector algebra. Making it *scale* is an engineering project. BoidForge carries the model from a transparent Python reference to a native C kernel that is two orders of magnitude faster, proves at every step that the extra speed costs nothing in correctness, and then renders the result as something genuinely worth watching, all inside a clean architecture where computation and rendering never touch. The hard part was never the boids. It was making them fast, reproducible, and beautiful.
