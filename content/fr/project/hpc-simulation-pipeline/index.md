---
draft: true   # section masquée tant que les projets ne sont pas finalisés
title: Pipeline de simulation & de données HPC
summary: Soumission, supervision et post-traitement automatisés de LES haute-fidélité sur clusters HPC (SLURM), avec des workflows de données parallèles et reproductibles.
tags:
  - Data Engineering
  - CFD
date: '2022-12-01T00:00:00Z'

external_link: ''

image:
  caption: 'Workflow HPC automatisé : soumettre, superviser, post-traiter'
  focal_point: Smart

links:
url_code: 'https://github.com/vcaries'
url_pdf: ''
url_slides: ''
url_video: ''
---
<!-- MODÈLE : remplacez cette description, les dates et le lien du dépôt par l'un de vos projets réels. -->

Un pipeline qui **automatise les grandes campagnes de simulation** sur clusters HPC : il génère les configurations de calcul, soumet et supervise les jobs **SLURM**, rassemble les sorties et déclenche le post-traitement — le tout de manière reproductible.

**Le problème résolu.** Lancer et tenir à jour manuellement des dizaines de calculs LES coûteux est source d'erreurs. Ce pipeline rend les campagnes répétables et traçables.

**Points clés**
- Génération de calculs par templates et orchestration de jobs SLURM.
- Collecte et consolidation automatiques des sorties distribuées.
- Workflows de données parallèles et reproductibles, prêts pour l'analyse.
