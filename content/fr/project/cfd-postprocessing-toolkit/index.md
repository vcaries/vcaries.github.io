---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: Boîte à outils de post-traitement CFD
summary: Outils Python réutilisables pour analyser et visualiser de gros jeux de données RANS/LES — transformer les sorties brutes de solveur en figures claires et reproductibles.
tags:
  - Scientific Python
  - CFD
  - Data Engineering
date: '2023-09-01T00:00:00Z'

external_link: ''

image:
  caption: 'Des sorties brutes de solveur aux figures prêtes à publier'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- MODÈLE : remplacez cette description, les dates et le lien du dépôt par l'un de vos projets réels. -->

Un ensemble d'**utilitaires Python réutilisables** pour fluidifier le post-traitement des résultats CFD. La boîte à outils lit les sorties de solveur, extrait les grandeurs de l'écoulement, calcule les champs dérivés et produit des **figures reproductibles, prêtes à publier**, avec un style cohérent.

**Le problème résolu.** Le post-traitement se réduit souvent à une accumulation de scripts jetables. Cette boîte à outils standardise le flux pour que les résultats soient comparables entre cas et reproductibles des mois plus tard.

**Points clés**
- Lecture robuste de gros jeux de données avec NumPy / pandas.
- Couche de tracé réutilisable (Matplotlib) à l'identité visuelle cohérente.
- Traitement par lots sur de nombreux cas ; pipelines scriptables et reproductibles.
