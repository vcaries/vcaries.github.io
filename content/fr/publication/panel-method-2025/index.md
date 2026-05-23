---
title: 'Panel Method for 3D Inviscid Flow Simulation of Low-Pressure Compressor Rotors with Tip-Leakage Flow'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - J. Boudet
  - E. Lippinois

# Author notes (optional)
#author_notes:
#  - 'Equal contribution'
#  - 'Equal contribution'

date: '2025-02-06T00:00:00Z'
doi: '10.3390/ijtpp10010003'

# Schedule page publish date (NOT publication's date).
publishDate: '2017-01-01T00:00:00Z'

# Préserve l'ancienne URL de la page (avant la refonte multilingue) pour le SEO.
aliases:
  - /publication/article_ijtpp_2024/

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ['Journal']

# Publication name and optional abbreviated publication name.
publication: International Journal of Turbomachinery Propulsion and Power
publication_short: In *IJTPP*

abstract:  This paper presents a low-order three-dimensional approach for predicting the inviscid flow around low-pressure compressors. The method is suitable for early design stages and allows a broad exploration of design possibilities at minimal cost. It combines the vortex lattice method with the panel method by using a mixed boundary condition. In addition, it models the tip-leakage flow using an iterative algorithm. First, the verification of the approach is carried out on a low-pressure compressor configuration. The wake length is a decisive parameter for ensuring correct flow deflection in ducted applications. A periodicity condition is introduced and validated, which reduces the computational and memory requirements. On average, the calculations take less than one minute in real time. The approach is validated on the same low-pressure compressor configuration. A good agreement is obtained with RANS concerning the mean flow and the tip-leakage flow characteristics. Sensitivity to the mass flow rate is also fairly well predicted, although discrepancies develop at lower mass flow rates. 

# Résumé court (optionnel).
summary: Cet article présente une méthode tridimensionnelle d'ordre réduit pour prédire l'écoulement non visqueux autour des soufflantes carénées, dédiée aux premières phases de conception. En combinant la méthode du maillage de tourbillons (VLM) et la méthode des panneaux via une condition aux limites mixte, elle permet d'explorer efficacement l'espace de conception. Le jeu en tête (tip-leakage flow) est modélisé par un algorithme itératif. Une condition de périodicité est validée, réduisant le coût de calcul à moins d'une minute. Les résultats concordent bien avec la RANS pour l'écoulement moyen et le jeu en tête, avec quelques écarts aux faibles débits.

tags: [Panel Method, Vortex Lattice Method, Axial Compressor Rotor, Tip-Leakage Flow]

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

url_pdf: 'https://hal.science/hal-04734815'
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: 'https://www.mdpi.com/2504-186X/10/1/3'
url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: 'Principe de la méthode hybride panneaux/VLM : cartographie des singularités et des points de collocation.'
  focal_point: ''
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
#projects:
#  - example

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
#slides: example
---
