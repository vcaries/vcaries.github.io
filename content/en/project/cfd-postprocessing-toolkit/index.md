---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: CFD post-processing toolkit
summary: Reusable Python tooling to parse, analyze and visualize large RANS/LES datasets — turning raw solver output into clear, reproducible figures.
tags:
  - Scientific Python
  - CFD
  - Data Engineering
date: '2023-09-01T00:00:00Z'

external_link: ''

image:
  caption: 'From raw solver output to publication-ready figures'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- TEMPLATE: replace this description, the dates and the repository link with one of your real projects. -->

A set of **reusable Python utilities** to streamline the post-processing of CFD results. The toolkit reads solver output, extracts flow quantities, computes derived fields and produces **publication-ready, reproducible figures** with a consistent style.

**What it solves.** Post-processing is often a pile of one-off scripts. This toolkit standardizes the workflow so results are comparable across cases and reproducible months later.

**Highlights**
- Robust parsing of large datasets with NumPy / pandas.
- Reusable plotting layer (Matplotlib) with a consistent visual identity.
- Batch processing across many cases; reproducible, scriptable pipelines.
