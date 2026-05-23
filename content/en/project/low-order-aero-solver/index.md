---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: 3D low-order aerodynamic solver (panel + VLM)
summary: A Python solver that predicts the 3D inviscid flow — including tip-leakage — around compressor and fan rotors in seconds, built for early-stage design exploration.
tags:
  - Scientific Python
  - CFD
date: '2024-06-01T00:00:00Z'

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: 'Hybrid panel / vortex-lattice discretization of a rotor'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: 'https://hal.science/hal-04734815'
url_slides: ''
url_video: ''
---

The flagship of my PhD work: a **three-dimensional, low-order aerodynamic solver** written in Python that combines the **panel method** and the **vortex-lattice method** through a mixed boundary condition, with a dedicated iterative model for the **tip-leakage flow**.

**Why it matters.** High-fidelity CFD (RANS/LES) is accurate but far too slow to explore many rotor designs. This solver brings the cost of a 3D flow prediction down to **seconds**, enabling broad design-space exploration — including disruptive geometries — at the earliest stages of design.

**Highlights**
- Hybrid panel + vortex-lattice formulation with a mixed boundary condition.
- Iterative tip-leakage model and a validated periodicity condition that slashes memory and CPU cost.
- Verified and validated against **RANS** for mean flow and tip-leakage characteristics.
- Clean, modular, tested Python codebase.

Published in the *International Journal of Turbomachinery, Propulsion and Power* (2025) and presented at the European Turbomachinery Conference (2023).
