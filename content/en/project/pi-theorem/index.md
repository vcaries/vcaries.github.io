---
draft: false
title: 'Pi-Scope — dimensional analysis in the browser'
summary: 'A full-stack scientific web app that derives the dimensionless groups governing a physical problem with the Vaschy–Buckingham (Π) theorem. The real Python + SymPy engine runs entirely in the browser via WebAssembly.'
tags:
  - Scientific Python
  - Web
  - Dimensional analysis
date: '2026-05-25T00:00:00Z'

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: 'Pi-Scope deriving the dimensionless groups of the Chen (1990) compressor tip-clearance case'
  focal_point: Smart

links:
  - name: Live demo
    url: 'https://vcaries.github.io/pi_theorem/'
    icon_pack: fas
    icon: play
url_code: 'https://github.com/vcaries/pi_theorem'
---

**Pi-Scope** turns a set of dimensioned physical variables into the **dimensionless groups** that govern them, using the **Vaschy–Buckingham (Π) theorem**. It pairs a rigorous scientific engine with a modern, bilingual, theme-aware interface — and, in its showcase deployment, runs the actual Python engine *inside the browser*.

👉 **[Try the live demo](https://vcaries.github.io/pi_theorem/)** · **[Source on GitHub](https://github.com/vcaries/pi_theorem)**

## Scientific context

Dimensional analysis is a cornerstone of physics and engineering. The **Buckingham Π theorem** states that any physically meaningful relation between *n* variables involving *k* independent base dimensions can be rewritten as a relation between just *n − k* **dimensionless groups**. Reducing the number of parameters this way is what makes wind-tunnel scaling, similarity laws and the famous numbers of fluid mechanics (Reynolds, Mach, Nusselt…) possible.

Concretely, the dimensionless groups form a **basis of the null space of the dimensional matrix** — the matrix whose columns are each variable's exponents over the SI base dimensions. Pi-Scope assembles that matrix, computes its rank and a null-space basis with **exact rational arithmetic** (no floating-point drift), and renders each group as clean LaTeX.

The flagship example reproduces the similarity parameters of *Chen, Greitzer, Tan & Marble, “Similarity Analysis of Compressor Tip Clearance Flow Structure” (1990)* — eleven variables reduced to eight independent dimensionless groups.

## Technical implementation

The project is built as a **decoupled, professional full-stack application**, then deployed in a way that needs no server at all:

- **Scientific engine — Python + SymPy.** A web-framework-free core extends the analysis to all **seven SI base dimensions** (mass, length, time, temperature, current, amount of substance, luminous intensity), computes the null-space basis symbolically, and reduces each group to its smallest integer exponents.
- **Backend — FastAPI.** A typed REST API (Pydantic schemas, automatic OpenAPI docs) exposes the engine, a curated variable library organised by physics domain, and citeable worked examples.
- **Frontend — React + TypeScript + Tailwind.** A responsive engineering-grade UI with KaTeX equation rendering, the explicit dimensional matrix, light/dark themes, full French/English internationalisation, and JSON/LaTeX export.
- **In-browser execution — Pyodide (WebAssembly).** For the public demo, the *exact same* Python engine is compiled to WebAssembly and runs client-side via Pyodide. The result is a **100 % static, offline-capable** site hosted directly on GitHub Pages — instant, free, and with no cold starts.
- **Engineering quality.** Unit + integration tests, linting and static typing (Ruff, Mypy), Docker images, and GitHub Actions CI/CD for both the API and the static demo.

## Skills demonstrated

- **Scientific computing & modelling:** dimensional analysis, exact linear algebra, symbolic mathematics.
- **Software architecture:** clean separation of a reusable engine, an API layer, and a UI; typed end-to-end.
- **Web integration:** React/TypeScript front end and the non-trivial feat of running a real Python scientific stack in the browser via WebAssembly.
- **Delivery & DevOps:** automated testing, containerisation, and continuous deployment to GitHub Pages.

This project is a compact demonstration of taking a piece of applied physics from a research script all the way to a polished, deployable product.
