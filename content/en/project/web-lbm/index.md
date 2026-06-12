---
draft: false
title: "Web-LBM: A Real-Time CFD Wind Tunnel in the Browser"
summary: "What does it take to run a genuine computational fluid dynamics solver at interactive frame rates inside a browser tab? Web-LBM is a 2D wind tunnel built on the Lattice Boltzmann Method: a C engine compiled to WebAssembly, a zero-copy WebGL2 rendering pipeline, a turbulence model, and multithreading — all on a 100 % static page."
authors:
  - admin
tags:
  - C / WebAssembly
  - CFD
  - Lattice Boltzmann
  - Aerodynamics
  - High-Performance Computing
  - WebGL
  - Simulation
  - Web
date: '2026-06-12T00:00:00Z'
toc: true

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: 'The von Kármán vortex street behind a cylinder, computed and rendered live in the browser'
  focal_point: Smart

links:
  - name: Try the simulation
    url: 'https://vcaries.github.io/web_lbm/'
    icon_pack: fas
    icon: play
url_code: 'https://github.com/vcaries/web_lbm'
url_pdf: ''
---

## In one minute

**Web-LBM** is an interactive two-dimensional wind tunnel that runs entirely in your browser. Behind the canvas sits a genuine **computational fluid dynamics (CFD)** solver — a **Lattice Boltzmann (D2Q9)** engine written in C, compiled to **WebAssembly**, and rendered on the GPU through **WebGL2**. You can drop in a cylinder or a NACA airfoil, change the angle of attack, spin an obstacle to feel the Magnus effect, paint your own geometry with the mouse, and watch the wake respond — with live lift and drag coefficients, and even virtual microphones that let you *see the sound* of vortex shedding.

CFD normally lives on clusters and overnight batch jobs. Bringing it to a browser tab — no install, no server, no framework, hosted as plain static files on GitHub Pages — is both a pedagogical statement and an engineering exercise: every constraint of the platform (no shared memory by default, no filesystem, one thread unless you earn more) has to be solved without giving up physical fidelity or interactivity.

👉 **[Try the simulation](https://vcaries.github.io/web_lbm/)** · **[Source code on GitHub](https://github.com/vcaries/web_lbm)**

### Highlights

- **A real solver, not a toy.** D2Q9 Lattice Boltzmann with BGK (or compile-time MRT) collision, a **Smagorinsky LES** turbulence model, Hermite-regularized collision for stability, Zou–He velocity inlet, absorbing sponge layers, and momentum-exchange force evaluation for live $C_l$ / $C_d$.
- **Real-time performance.** A branchless, SIMD-vectorized hot loop and **WebAssembly threads** (pthreads over `SharedArrayBuffer`) with a deterministic, lock-free row partition.
- **Zero-copy rendering.** Field data flows from the wasm heap to the screen without a single intermediate copy: typed-array views → `R32F` WebGL2 texture → colormap lookup in the fragment shader.
- **Aeroacoustics included.** Because LBM is weakly compressible, the engine resolves acoustic waves: schlieren ($|\nabla\rho|$) and dilatation ($\nabla\cdot\mathbf{u}$) views, plus virtual microphones with a live FFT that picks up the aeolian tone of the shedding wake.
- **100 % static deployment.** Two engine builds (single- and multi-threaded) are selected at runtime; a service worker supplies the cross-origin isolation headers GitHub Pages cannot send.

## Why CFD in the browser?

Three reasons, in increasing order of difficulty.

**Pedagogy.** Fluid dynamics is taught with equations and validated with expensive simulations, but *intuition* comes from immediate cause and effect: tilt an airfoil and watch the stall, spin a cylinder and watch the lift appear. An interactive simulation with a feedback loop measured in milliseconds is a fundamentally different learning tool from a static plot.

**Accessibility.** A browser page with no install and no backend reaches anyone — students, colleagues, recruiters — on any machine, indefinitely, at zero hosting cost. That requires the entire solver to run client-side, which is precisely what WebAssembly makes possible.

**The engineering challenge.** Real-time CFD is a stress test for the whole stack: a numerical method stable enough to survive whatever the user throws at it, a memory layout the compiler can vectorize, a threading model that fits the browser's security constraints, and a rendering path fast enough to never be the bottleneck. Solving all four at once is the core of this project.

## The physics: Lattice Boltzmann in brief

### A different route to fluid dynamics

Classical CFD discretizes the **Navier–Stokes equations** directly: velocity and pressure live on a mesh, and each timestep requires solving coupled, *global* systems — typically a pressure Poisson equation whose solution couples every cell in the domain to every other.

The **Lattice Boltzmann Method (LBM)** takes a route one level below the macroscopic description. It evolves **particle distribution functions** $f_i(\mathbf{x}, t)$ — the amount of fluid at node $\mathbf{x}$ moving along a small set of discrete velocities $\mathbf{c}_i$. The macroscopic fields are simply moments of these distributions:

$$\rho = \sum_i f_i, \qquad \rho\,\mathbf{u} = \sum_i f_i\,\mathbf{c}_i$$

A Chapman–Enskog expansion shows that this kinetic system reproduces the incompressible Navier–Stokes equations in the low-Mach-number limit. The fluid viscosity is controlled by a single relaxation time $\tau$:

$$\nu = c_s^2\left(\tau - \tfrac{1}{2}\right)$$

What makes LBM exceptional for this project is its **locality**: each node updates from its immediate neighbours only. No global solve, no linear algebra, no convergence loop — which means the cost per timestep is fixed and predictable, the algorithm parallelizes almost trivially, and the simulation is *naturally unsteady*: vortex shedding is not an option you enable, it is what the method computes by default. As a bonus, LBM is weakly compressible, so pressure waves propagate physically — the simulation does acoustics for free.

### Collision and streaming

Each timestep is two conceptually simple operations. **Collision** relaxes the distributions toward a local equilibrium (the BGK approximation):

$$f_i(\mathbf{x}, t^{+}) = f_i(\mathbf{x}, t) - \frac{1}{\tau}\left[f_i(\mathbf{x}, t) - f_i^{\mathrm{eq}}(\rho, \mathbf{u})\right]$$

where the equilibrium is a second-order expansion of the Maxwell–Boltzmann distribution:

$$f_i^{\mathrm{eq}} = w_i\,\rho\left[1 + \frac{\mathbf{c}_i\cdot\mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i\cdot\mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}\cdot\mathbf{u}}{2c_s^2}\right]$$

**Streaming** then shifts each post-collision distribution to the neighbouring node in its direction of travel:

$$f_i(\mathbf{x} + \mathbf{c}_i\,\Delta t,\; t + \Delta t) = f_i(\mathbf{x}, t^{+})$$

Collision is purely local arithmetic; streaming is a pure memory move. That separation — heavy math with no communication, then communication with no math — is exactly the structure that SIMD units and multicore processors love, and the implementation below exploits it deliberately.

### Why D2Q9

The engine uses the **D2Q9** lattice: two dimensions, nine velocities (rest, four axis-aligned, four diagonal) with weights $w_0 = 4/9$, $w_{1\text{–}4} = 1/9$, $w_{5\text{–}8} = 1/36$. It is the smallest 2D lattice whose velocity moments are isotropic enough to recover Navier–Stokes correctly — fewer directions would bias the physics along the grid axes, more would cost memory and bandwidth for no gain at this level of description. Nine `float` fields per node also sets the memory budget: a 600 × 300 grid fits comfortably in a few tens of megabytes of wasm heap.

### Boundary conditions

Boundaries are where LBM implementations earn their keep, because after streaming, the distributions entering the domain from outside are unknown and must be reconstructed:

- **Inlet** — a **Zou–He** velocity boundary imposes the inflow profile (uniform, shear layer, or jet) by reconstructing the unknown distributions from mass and momentum constraints. A 400-step soft-start ramps the velocity after every (re)initialization so the impulsive start does not launch a shock down the tunnel.
- **Outlet** — zero-gradient extrapolation, backed by an **absorbing sponge layer** that smoothly raises dissipation near the boundary so vortices and acoustic waves leave the domain instead of reflecting back into it.
- **Obstacles** — **bounce-back**: distributions that hit a solid node return whence they came, producing a no-slip wall with no meshing whatsoever. Its **moving-wall** variant adds the wall-velocity momentum to reflected populations — that is the entire implementation of the rotating cylinder, and the Magnus effect follows from the physics. Summing the momentum exchanged in these reflections gives the aerodynamic force on each body — the live $C_l$ and $C_d$ in the HUD — at almost no cost.
- **Tunnel walls** — selectable free-slip (specular reflection) or no-slip bounce-back.

## Implementation

### Architecture

The project is two cleanly separated parts joined by one shared memory buffer:

```
C engine (lbm.c, C99)  --emcc-->  WebAssembly + wasm heap
                                        │ zero-copy Float32Array views
vanilla ES6 frontend  ── WebGL2 R32F textures ──>  colormap LUT in shader
```

- **The engine** is a single C99 file: the D2Q9 solver, LES, boundary conditions, analytic shape rasterizers (cylinder, flat plate, NACA 0012 / 4412), force evaluation, and derived-field computation (velocity, pressure, vorticity, schlieren, dilatation). It exposes a small flat C API (`lbm_init`, `lbm_step`, `lbm_set_params`, …) and knows nothing about JavaScript.
- **The frontend** is vanilla ES6 modules — no framework, no bundler, no build step beyond `emcc` itself. `main.js` drives the simulation loop and UI, `renderer.js` owns WebGL2, `obstacles.js` defines the analytic presets.
- **Two engine builds** are produced from the same source: a single-threaded variant that runs everywhere, and a `-pthread` variant using WebAssembly threads. The app feature-detects `crossOriginIsolated` at boot and picks the best one, falling back gracefully.

### The zero-copy data path

The cardinal rule of the rendering pipeline is that **field data is never copied on the JavaScript side**. The C engine computes, say, vorticity into a `float` array in the wasm heap; JavaScript wraps that memory in a `Float32Array` *view* (no allocation, no copy) and hands it directly to `texSubImage2D`, which uploads it into a single-channel floating-point (`R32F`) texture. The fragment shader then maps values to colour through a small lookup-table texture — the entire visual styling costs one texture fetch per pixel and lives on the GPU.

Two subtleties keep this honest. When the wasm heap grows (the user picks a finer grid), the underlying `ArrayBuffer` detaches and every view must be rebuilt — the app does this lazily, on demand. And in the multithreaded build the heap is a `SharedArrayBuffer`, which some browsers refuse to upload from directly; a single small staging buffer is the one sanctioned exception to the no-copy rule.

### Multithreading in a browser

The interior sweep is **row-partitioned** across a pool of wasm pthreads, with barriers separating the phases of each timestep. The partition is designed so that every slot of the destination array has *exactly one* producer — threads never contend, so there are no locks and no atomics in the hot path. Force contributions are reduced in fixed thread order, which makes results **bit-deterministic for a given thread count** — a property borrowed from serious HPC practice, where "fast but slightly different every run" is how bugs hide.

Browser threading comes with a catch: `SharedArrayBuffer` requires the page to be **cross-origin isolated**, which needs COOP/COEP HTTP headers that a static host like GitHub Pages cannot send. Web-LBM solves this with a root-scoped **service worker** that injects the headers client-side (one automatic reload on first visit). If anything in that chain fails — older browser, partial isolation — the app silently boots the single-threaded engine instead: progressive enhancement applied to HPC.

### Interaction

Everything in the tunnel is manipulable while the simulation runs: obstacles are placed by click, rotated, spun (rotating cylinders), or **painted freehand** with the mouse directly into the obstacle mask. Painted cells are resampled when the grid resolution changes, while preset shapes are re-rasterized *analytically* from their registry — so a NACA profile stays a crisp NACA profile at any resolution. Flow can be visualized as velocity, pressure, vorticity, schlieren, or dilatation, with streamline and particle overlays, and **virtual microphones** can be dropped anywhere in the field to plot a live FFT of the local pressure signal — placing one behind a cylinder reveals the sharp spectral peak of the shedding frequency, the same physics as the hum of wind through wires.

## Engineering challenges

### Numerical stability without a referee

An interactive simulation cannot reject user input: whatever Reynolds number, obstacle shape, or resolution the visitor chooses, the solver must not blow up. Plain BGK becomes unstable as $\tau \to 1/2$ (high Reynolds numbers), so the engine layers several defences, each addressing a distinct failure mode:

- A **Smagorinsky LES model** ($C_s = 0.18$) computes a local eddy viscosity from the strain rate — captured in LBM directly from the non-equilibrium distributions, with no finite differences — which both models the unresolved turbulent scales and keeps the effective $\tau$ away from the unstable limit exactly where the flow is most strained.
- **Hermite regularization** projects the non-equilibrium part of the distributions onto its physically meaningful (second-order Hermite) component before collision, filtering the spurious higher-order modes that otherwise accumulate and destabilize coarse grids.
- **Bulk-viscosity damping** selectively dissipates the acoustic part of the stress, taming pressure oscillations without touching the shear physics that creates vortices.
- **Sponge layers and a soft-started inlet** prevent the two classic transients — reflected outflow waves and the initial impulse — from contaminating the domain.

The result is a tunnel that survives being abused, which is the difference between a demo and a product.

### Keeping the hot loop hot

The collide-and-stream sweep over interior cells dominates the runtime, and it is written so that **LLVM can auto-vectorize it to WebAssembly SIMD** — worth roughly a 3× speedup. That imposes a discipline: the loop contains *no branches at all*. No obstacle checks, no boundary special cases; the LES model is folded into straight-line arithmetic, and `restrict`-qualified pointer copies tell the compiler no aliasing can occur. Solid cells are handled by a separate, cheap **fixup pass** after the sweep. The lesson generalizes: structuring code so the compiler can prove things about it routinely beats hand-optimizing the code itself.

The data layout serves the same goal: a **structure-of-arrays** of nine flat `float` fields, indexed `y·Nx + x`, so streaming in each direction is a contiguous memory move and the SIMD lanes always load adjacent values.

### The browser as an HPC platform

The browser is a hostile environment by HPC standards, and several of its constraints shaped the design directly: wasm memory growth **detaches every live view** (handled by lazy view rebuilding); `texSubImage2D` may reject SAB-backed views (handled by the single staging buffer); cross-origin isolation is unobtainable on static hosts without the service-worker shim; and the thread pool must be sized and spawned at module load, because workers cannot be created synchronously mid-frame. Each workaround is small, but knowing *where* they are needed is exactly the platform expertise the project set out to build.

## What you can explore

A few experiments that each take under a minute in the [live tunnel](https://vcaries.github.io/web_lbm/):

1. **Vortex shedding** — keep the default cylinder, switch to the vorticity view, and watch the von Kármán street establish itself; the HUD shows $C_l$ oscillating at the shedding frequency.
2. **Stall** — place a NACA 4412 airfoil and increase the angle of attack: the lift coefficient climbs, then the suction-side flow separates.
3. **The Magnus effect** — spin a cylinder and watch the wake deflect and a steady lift force appear, the physics behind curved free kicks.
4. **Aeroacoustics** — switch to the schlieren or dilatation view to see pressure waves radiate from the wake, then drop a microphone behind the cylinder and find the shedding tone in the live spectrum.
5. **Your own geometry** — paint an arbitrary obstacle with the mouse and see how the flow negotiates it.

## Skills demonstrated

- **Computational fluid dynamics:** the Lattice Boltzmann Method end to end — lattice choice, collision models (BGK, MRT, regularization), boundary conditions, turbulence modelling (Smagorinsky LES), force evaluation, and aeroacoustics.
- **Numerical methods & scientific computing:** stability analysis in practice — identifying failure modes and layering targeted remedies; a physics engine written in portable C99 with embedded smoke tests.
- **Performance engineering:** SIMD-friendly branchless kernels, structure-of-arrays memory layout, lock-free deterministic multithreading, and profiling-driven separation of hot and cold paths.
- **Software architecture:** a strict engine/frontend boundary with a zero-copy data contract across the C/JavaScript frontier; runtime feature detection with graceful degradation.
- **Web technologies:** WebAssembly (Emscripten, wasm threads, shared memory), WebGL2 (floating-point textures, shader-based colormapping), service workers, and fully static deployment.
- **Interactive scientific visualization & UI design:** real-time field rendering, multiple physically meaningful views, and an interface that invites experimentation without a manual.
- **Scientific communication:** making graduate-level fluid dynamics tangible — and fun — for a general technical audience.

## Repository

The full source is open: the C engine (extensively commented, including every compiler flag and its rationale), the WebGL2 renderer, the build scripts, and the physics smoke tests.

The code lives at **[github.com/vcaries/web_lbm](https://github.com/vcaries/web_lbm)** — and the tunnel itself runs at **[vcaries.github.io/web_lbm](https://vcaries.github.io/web_lbm/)**.

## Conclusion

Web-LBM compresses the whole span of simulation engineering — a kinetic numerical method, turbulence modelling, SIMD and multithreaded optimization, GPU rendering, and product-grade interaction design — into a single page that anyone can open. The Lattice Boltzmann Method is the enabling choice: local, parallel, naturally unsteady, and quietly capable of acoustics. The browser is the forcing function: every one of its constraints had to be engineered around, never waved away. The result is a wind tunnel in a tab — and a demonstration that *real* scientific computing does not have to live behind a queue on a cluster.
