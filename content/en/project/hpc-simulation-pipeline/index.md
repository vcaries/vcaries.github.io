---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: HPC simulation & data pipeline
summary: Automated submission, monitoring and post-processing of high-fidelity LES on HPC clusters (SLURM), with reproducible, parallel data workflows.
tags:
  - Data Engineering
  - CFD
date: '2022-12-01T00:00:00Z'

external_link: ''

image:
  caption: 'Automated HPC workflow: submit, monitor, post-process'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- TEMPLATE: replace this description, the dates and the repository link with one of your real projects. -->

A pipeline that **automates large simulation campaigns** on HPC clusters: it generates run configurations, submits and monitors **SLURM** jobs, gathers the outputs and triggers post-processing — all reproducibly.

**What it solves.** Manually launching and bookkeeping dozens of expensive LES runs is error-prone. This pipeline makes campaigns repeatable and auditable.

**Highlights**
- Templated run generation and SLURM job orchestration.
- Automatic collection and consolidation of distributed output.
- Parallel, reproducible data workflows ready for downstream analysis.
