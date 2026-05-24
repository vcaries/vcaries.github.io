---
# Laisser le titre vide pour utiliser le titre du site
title: ''
date: 2022-10-24
type: landing

sections:
  - block: about.biography
    id: about
    content:
      title: Biographie
      # Profil à afficher (nom de dossier dans `content/<lang>/authors/`)
      username: admin

  - block: markdown
    id: skills
    content:
      title: Compétences & Services
      subtitle: ''
      text: |-
        <p class="section-lead">J'aide les équipes d'ingénierie et de recherche à transformer une physique complexe en <strong>logiciels rapides, fiables et testés</strong> et à convertir des données de simulation brutes en information utile. Ouvert à des missions ponctuelles de freelance et de conseil.</p>

        <div class="services-grid">
          <div class="service-card">
            <h3>🐍 Python scientifique</h3>
            <p>Méthodes numériques, solveurs et bibliothèques réutilisables. Code propre, documenté et testé avec NumPy/SciPy, profilage de performance et packaging.</p>
          </div>
          <div class="service-card">
            <h3>🌀 CFD &amp; Simulation</h3>
            <p>Chaînes RANS &amp; LES, modèles aérodynamiques d'ordre réduit et multi-fidélité, gestion de maillage, mise en données, vérification &amp; validation.</p>
          </div>
          <div class="service-card">
            <h3>⚙️ Data engineering &amp; HPC</h3>
            <p>Pipelines de post-traitement, gestion de gros volumes de données, automatisation de calculs sur clusters HPC (SLURM), workflows reproductibles et parallèles.</p>
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
          <span class="tag-pill">Modélisation d'ordre réduit</span>
          <span class="tag-pill">LaTeX</span>
        </div>
    design:
      columns: '1'

  - block: experience
    id: experience
    content:
      title: Expérience
      date_format: Jan 2006
      items:
        - title: Ingénieur de recherche
          company: IFP Energies nouvelles (IFPEN)
          company_url: 'https://www.ifpenergiesnouvelles.com/'
          company_logo: ifpen
          location: Solaize, France
          date_start: '2025-04-14'
          date_end: ''
          description: |2-
              Recherche et développement sur les **systèmes de pompage polyphasique**.
              * Modélisation numérique et CFD des écoulements diphasiques.
              * Suivi de campagnes expérimentales et validation de modèles.
              * Développement scientifique pour la simulation, le traitement et l'analyse de données.

        - title: Doctorat — Modélisation aérodynamique
          company: Safran Aircraft Engines · École Centrale de Lyon
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel / Lyon, France
          date_start: '2022-03-21'
          date_end: '2025-06-11'
          description: |2-
              Modélisation multi-fidélité du jeu en tête d'un rotor de compresseur axial en écoulement compressible. Thèse soutenue le 11 juin 2025.
              * Conception et implémentation d'un **solveur aérodynamique 3D d'ordre réduit** (méthodes des panneaux + maillage de tourbillons) en Python, réduisant les prédictions d'écoulement de plusieurs heures à **quelques secondes**.
              * Validation des modèles face à la **RANS** et à des essais ; publications dans des revues à comité de lecture et conférences internationales.
              * Développement des outils de **traitement et de visualisation des données** associés.

        - title: Ingénieur CFD
          company: Safran Aircraft Engines
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel, France
          date_start: '2021-11-01'
          date_end: '2022-03-19'
          description: |2-
              * Développement et automatisation de méthodologies de simulation **RANS**.
              * Livraison d'outils Python pour fluidifier le pré- et le post-traitement.

        - title: Stage de recherche — CFD haute-fidélité
          company: Safran Aircraft Engines
          company_url: 'https://www.safran-group.com/companies/safran-aircraft-engines'
          company_logo: sae
          location: Moissy-Cramayel, France
          date_start: '2021-04-01'
          date_end: '2021-09-30'
          description: |2-
              Simulation aux grandes échelles résolue à la paroi (WRLES) de configurations d'hélices 2.5D.
              * Calculs **LES haute-fidélité sur clusters HPC** et développement de la méthodologie de post-traitement en Python.

        - title: Stage de recherche — Optimisation
          company: Louisiana State University
          company_url: 'https://www.lsu.edu/'
          company_logo: lsu
          location: Baton Rouge, LA, États-Unis
          date_start: '2019-03-01'
          date_end: '2019-08-30'
          description: |2-
              * Modèle Python pour l'**optimisation de stratégie de course Shell Eco-marathon** (dynamique véhicule, gestion d'énergie).
    design:
      columns: '2'

  # --------------------------------------------------------------------------
  # SECTION PROJETS — masquée temporairement (en cours de préparation).
  # Le contenu des projets reste dans content/fr/project/ (passé en draft).
  # Pour la publier plus tard :
  #   1) décommente le bloc `portfolio` ci-dessous,
  #   2) réajoute l'entrée « Projets » dans config/_default/menus.fr.yaml,
  #   3) repasse `draft: false` dans content/fr/project/**/index.md (et _index.md).
  # --------------------------------------------------------------------------
  #  - block: portfolio
  #    id: projects
  #    content:
  #      title: Projets
  #      subtitle: 'Sélection de projets d''ingénierie & de développement'
  #      text: ''
  #      filters:
  #        folders:
  #          - project
  #      default_button_index: 0
  #      buttons:
  #        - name: Tous
  #          tag: '*'
  #        - name: Python scientifique
  #          tag: Scientific Python
  #        - name: CFD
  #          tag: CFD
  #        - name: Data engineering
  #          tag: Data Engineering
  #        - name: Machine learning
  #          tag: Machine Learning
  #    design:
  #      columns: '1'
  #      view: showcase
  #      flip_alt_rows: false

  - block: collection
    id: publications
    content:
      title: Publications
      text: 'Articles de revue et de conférence à comité de lecture, et ma thèse de doctorat. Liste complète sur [Google Scholar](https://scholar.google.com/citations?hl=fr&user=Zk00T9YAAAAJ) et [HAL](https://hal.science/search/index/q/*/authIdHal_s/valentin-caries).'
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      columns: '2'
      view: card

  - block: collection
    id: talks
    content:
      title: Conférences
      filters:
        folders:
          - event
    design:
      columns: '2'
      view: card

  - block: collection
    id: teaching
    content:
      title: Enseignement
      filters:
        folders:
          - teaching
    design:
      columns: '2'
      view: card

  - block: contact
    id: contact
    content:
      title: Travaillons ensemble
      subtitle: 'Freelance & conseil — Python scientifique, CFD, data, ML'
      text: 'Un projet en tête, ou un problème à la frontière de la physique et du code ? Écrivez-moi.'
      email: valentin.caries@ifpen.fr
      autolink: true
    design:
      columns: '2'
---
