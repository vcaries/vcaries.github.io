---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: Modèles de substitution (ML) pour l'exploration de conception
summary: Modèles de substitution et surfaces de réponse pilotés par les données qui émulent des simulations coûteuses, pour explorer rapidement l'espace de conception tout en respectant la physique.
tags:
  - Machine Learning
  - Scientific Python
date: '2024-02-01T00:00:00Z'

external_link: ''

image:
  caption: 'Des modèles de substitution qui accélèrent l''exploration de conception'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- MODÈLE : remplacez cette description, les dates et le lien du dépôt par l'un de vos projets réels. -->

Des **modèles de substitution** (surfaces de réponse, processus gaussiens, régression) qui apprennent à partir d'un nombre limité de simulations haute-fidélité, puis prédisent les performances sur tout l'espace de conception **plusieurs ordres de grandeur plus vite**.

**Le problème résolu.** Quand chaque simulation coûte des heures, l'exploration exhaustive est impossible. Un bon modèle de substitution transforme une poignée de calculs en un modèle rapide et interrogeable — idéal pour l'optimisation et les études de sensibilité.

**Points clés**
- Stratégies multi-fidélité combinant sources de données peu et très coûteuses.
- Pipelines scikit-learn / NumPy avec validation croisée rigoureuse.
- Variables conçues en cohérence avec la physique et conscience de l'incertitude.
