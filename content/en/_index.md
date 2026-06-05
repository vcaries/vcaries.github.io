---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

# SEO description (meta description / Google preview snippet). The theme reads
# the `summary` key first; set per-page and per-language, it overrides the
# global params.yaml description.
summary: 'PhD in aerodynamics and research engineer. I build fast, reliable scientific software for fluid mechanics: CFD, simulation, reduced-order modeling, data and high-performance computing. Projects and freelance work.'

sections:
  - block: about.biography
    id: about
    content:
      title: Biography
      # Choose a user profile to display (a folder name within `content/<lang>/authors/`)
      username: admin

  - block: markdown
    id: skills
    content:
      title: Skills & Services
      subtitle: ''
      text: |-
        <p class="section-lead">I help engineering and research teams turn complex physics into <strong>fast, reliable, well-tested software</strong> and turn raw simulation data into insight. Open to selected freelance and consulting missions.</p>

        <div class="services-grid">
          <div class="service-card">
            <h3>🐍 Scientific Python</h3>
            <p>Numerical methods, solvers and reusable packages. Clean, documented, tested code with NumPy/SciPy, performance profiling and packaging.</p>
          </div>
          <div class="service-card">
            <h3>🌀 CFD &amp; Simulation</h3>
            <p>RANS &amp; LES workflows, reduced-order and multi-fidelity aerodynamic models, mesh handling, solver setup, verification &amp; validation.</p>
          </div>
          <div class="service-card">
            <h3>⚙️ Data Engineering &amp; HPC</h3>
            <p>Post-processing pipelines, large dataset handling, job automation on HPC clusters (SLURM), reproducible and parallel workflows.</p>
          </div>
        </div>

        <div class="skills-tags">
          <span class="tag-pill">Python</span>
          <span class="tag-pill">NumPy</span>
          <span class="tag-pill">SciPy</span>
          <span class="tag-pill">pandas</span>
          <span class="tag-pill">Fortran</span>
          <span class="tag-pill">C</span>
          <span class="tag-pill">Git</span>
          <span class="tag-pill">Linux / HPC</span>
          <span class="tag-pill">SLURM</span>
          <span class="tag-pill">CFD (RANS / LES)</span>
          <span class="tag-pill">Reduced-order modeling</span>
          <span class="tag-pill">LaTeX</span>
        </div>
    design:
      columns: '1'

  - block: experience
    id: experience
    content:
      title: Experience
      date_format: Jan 2006
      items:
        - title: Research Engineer
          company: IFP Energies nouvelles (IFPEN)
          company_url: 'https://www.ifpenergiesnouvelles.com/'
          company_logo: ifpen
          location: Solaize, France
          date_start: '2025-04-14'
          date_end: ''
          description: |2-
              Research and scientific development on **multiphase pump systems**.
              * Numerical modeling and CFD of multiphase flows.
              * Experimental campaigns and data analysis.
              * Scientific **Python** development for simulation, data processing and analysis.

        - title: PhD — Aerodynamic modeling
          company: Safran Aircraft Engines · École Centrale de Lyon
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel / Lyon, France
          date_start: '2022-03-21'
          date_end: '2025-06-11'
          description: |2-
              Multi-fidelity modeling of the tip-leakage flow for an axial compressor rotor in compressible flow. PhD defended on 11 June 2025.
              * Designed and implemented a **3D low-order aerodynamic solver** (panel + vortex-lattice methods) in Python, reducing rotor flow predictions from hours to **seconds**.
              * Validated the models against **RANS** simulations and experiments; published in peer-reviewed journals and international conferences.
              * Built the supporting **data processing and visualization** tooling.

        - title: CFD Engineer
          company: Safran Aircraft Engines
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel, France
          date_start: '2021-11-01'
          date_end: '2022-03-19'
          description: |2-
              * Developed and automated **RANS** simulation methodologies.
              * Delivered Python tooling to streamline pre- and post-processing.

        - title: Research Intern — High-fidelity CFD
          company: Safran Aircraft Engines
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel, France
          date_start: '2021-04-01'
          date_end: '2021-09-30'
          description: |2-
              Wall-Resolved Large Eddy Simulation (WRLES) of 2.5D propeller configurations.
              * Ran **high-fidelity LES on HPC clusters** and developed the post-processing methodology in Python.

        - title: Research Intern — Optimization
          company: Louisiana State University
          company_url: 'https://www.lsu.edu/'
          company_logo: lsu
          location: Baton Rouge, LA, USA
          date_start: '2019-03-01'
          date_end: '2019-08-30'
          description: |2-
              * Built a Python model for **Shell Eco-marathon race-strategy optimization** (vehicle dynamics, energy management).
    design:
      columns: '2'

  # --------------------------------------------------------------------------
  # PROJECTS SECTION — temporarily hidden (work in progress).
  # The project content still lives in content/en/project/ (set to draft).
  # To publish it later:
  #   1) uncomment the `portfolio` block below,
  #   2) re-add the "Projects" entry in config/_default/menus.en.yaml,
  #   3) set `draft: false` in content/en/project/**/index.md (and _index.md).
  # --------------------------------------------------------------------------
  - block: portfolio
    id: projects
    content:
      title: Projects
      subtitle: 'Selected engineering & software projects'
      text: ''
      filters:
        folders:
          - project
      default_button_index: 0
      buttons:
        - name: All
          tag: '*'
        - name: Scientific Python
          tag: Scientific Python
        - name: CFD & Aerodynamics
          tag: Aerodynamics
        - name: High-Performance Computing
          tag: High-Performance Computing
        - name: Web Apps
          tag: Web
    design:
      columns: '1'
      view: showcase
      flip_alt_rows: false

  - block: collection
    id: publications
    content:
      title: Recent publications
      count: 4
      text: 'A selection of my recent work — see [all publications](/en/publication/). Also on [Google Scholar](https://scholar.google.com/citations?hl=en&user=Zk00T9YAAAAJ) and [HAL](https://hal.science/search/index/q/*/authIdHal_s/valentin-caries).'
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      columns: '2'
      view: card

  # Talks and Teaching now have their own pages, reachable from the menu
  # (/en/event/ and /en/teaching/). This keeps the homepage short.

  - block: contact
    id: contact
    content:
      title: Let's work together
      subtitle: 'Freelance & consulting: scientific Python, CFD, simulation, data engineering'
      # Professional email to be added later; routing contact via LinkedIn for now
      # (the IFPEN work address is intentionally not used for freelance contact).
      text: 'Have a project in mind, or a problem at the boundary of physics and code? Reach out on [LinkedIn](https://www.linkedin.com/in/valentin-caries/).'
    design:
      columns: '2'
---
