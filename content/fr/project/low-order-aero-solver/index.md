---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: Solveur aérodynamique 3D d'ordre réduit (panneaux + VLM)
summary: Un solveur Python qui prédit l'écoulement non visqueux 3D — jeu en tête inclus — autour des rotors de compresseurs et de soufflantes en quelques secondes, pour l'exploration de conception amont.
tags:
  - Scientific Python
  - CFD
date: '2024-06-01T00:00:00Z'

external_link: ''

image:
  caption: 'Discrétisation hybride panneaux / maillage de tourbillons d''un rotor'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: 'https://hal.science/hal-04734815'
url_slides: ''
url_video: ''
---

Le projet phare de ma thèse : un **solveur aérodynamique tridimensionnel d'ordre réduit** en Python qui combine la **méthode des panneaux** et la **méthode du maillage de tourbillons** via une condition aux limites mixte, avec un modèle itératif dédié au **jeu en tête** (*tip-leakage flow*).

**Pourquoi c'est utile.** La CFD haute-fidélité (RANS/LES) est précise mais bien trop lente pour explorer de nombreuses conceptions de rotor. Ce solveur ramène le coût d'une prédiction d'écoulement 3D à **quelques secondes**, permettant une large exploration de l'espace de conception — y compris des géométries de rupture — dès les premières phases.

**Points clés**
- Formulation hybride panneaux + maillage de tourbillons avec condition aux limites mixte.
- Modèle itératif de jeu en tête et condition de périodicité validée qui réduit fortement les coûts mémoire et CPU.
- Vérifié et validé face à la **RANS** pour l'écoulement moyen et le jeu en tête.
- Code Python propre, modulaire et testé.

Publié dans l'*International Journal of Turbomachinery, Propulsion and Power* (2025) et présenté à la European Turbomachinery Conference (2023).
