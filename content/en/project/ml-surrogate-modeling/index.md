---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: ML surrogate models for design exploration
summary: Data-driven surrogate and response-surface models that emulate expensive simulations, enabling fast design-space exploration while respecting the physics.
tags:
  - Machine Learning
  - Scientific Python
date: '2024-02-01T00:00:00Z'

external_link: ''

image:
  caption: 'Surrogate models accelerating design-space exploration'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- TEMPLATE: replace this description, the dates and the repository link with one of your real projects. -->

**Surrogate models** (response surfaces, Gaussian processes, regression) that learn from a limited set of high-fidelity simulations and then predict performance across the design space **orders of magnitude faster**.

**What it solves.** When each simulation costs hours, exhaustive exploration is impossible. A well-built surrogate turns a handful of runs into a fast, queryable model — ideal for optimization and sensitivity studies.

**Highlights**
- Multi-fidelity strategies combining cheap and expensive data sources.
- scikit-learn / NumPy pipelines with proper cross-validation.
- Physics-aware feature design and uncertainty awareness.
