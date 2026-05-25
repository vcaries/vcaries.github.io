---
draft: false
title: 'Pi-Scope — l''analyse dimensionnelle dans le navigateur'
summary: 'Une application web scientifique full-stack qui détermine les groupes adimensionnels gouvernant un problème physique via le théorème de Vaschy–Buckingham (Π). Le véritable moteur Python + SymPy s''exécute entièrement dans le navigateur grâce à WebAssembly.'
tags:
  - Scientific Python
  - Web
  - Dimensional analysis
date: '2026-05-25T00:00:00Z'

# URL externe optionnelle (remplace la page de détail du projet).
external_link: ''

image:
  caption: 'Pi-Scope déterminant les groupes adimensionnels du cas du jeu en tête de compresseur (Chen, 1990)'
  focal_point: Smart

links:
  - name: Démo en ligne
    url: 'https://vcaries.github.io/pi_theorem/'
    icon_pack: fas
    icon: play
url_code: 'https://github.com/vcaries/pi_theorem'
---

**Pi-Scope** transforme un ensemble de variables physiques dimensionnées en les **groupes adimensionnels** qui les gouvernent, grâce au **théorème de Vaschy–Buckingham (Π)**. Le projet associe un moteur scientifique rigoureux à une interface moderne, bilingue et thématisable — et, dans son déploiement vitrine, exécute le véritable moteur Python *à l'intérieur du navigateur*.

👉 **[Essayer la démo en ligne](https://vcaries.github.io/pi_theorem/)** · **[Code source sur GitHub](https://github.com/vcaries/pi_theorem)**

## Contexte scientifique

L'analyse dimensionnelle est un pilier de la physique et de l'ingénierie. Le **théorème de Buckingham Π** énonce que toute relation physiquement significative entre *n* variables faisant intervenir *k* dimensions de base indépendantes peut se réécrire comme une relation entre seulement *n − k* **groupes adimensionnels**. C'est cette réduction du nombre de paramètres qui rend possibles les lois de similitude, les essais en soufflerie à échelle réduite et les nombres célèbres de la mécanique des fluides (Reynolds, Mach, Nusselt…).

Concrètement, les groupes adimensionnels forment une **base du noyau de la matrice dimensionnelle** — la matrice dont les colonnes sont les exposants de chaque variable sur les dimensions de base SI. Pi-Scope assemble cette matrice, calcule son rang et une base du noyau en **arithmétique rationnelle exacte** (sans dérive en virgule flottante), puis affiche chaque groupe en LaTeX.

L'exemple phare reproduit les paramètres de similitude de *Chen, Greitzer, Tan & Marble, « Similarity Analysis of Compressor Tip Clearance Flow Structure » (1990)* — onze variables réduites à huit groupes adimensionnels indépendants.

## Mise en œuvre technique

Le projet est conçu comme une **application full-stack découplée et professionnelle**, puis déployé d'une manière qui ne nécessite aucun serveur :

- **Moteur scientifique — Python + SymPy.** Un cœur indépendant de tout framework web étend l'analyse aux **sept dimensions de base SI** (masse, longueur, temps, température, courant, quantité de matière, intensité lumineuse), calcule la base du noyau de façon symbolique et réduit chaque groupe à ses plus petits exposants entiers.
- **Backend — FastAPI.** Une API REST typée (schémas Pydantic, documentation OpenAPI automatique) expose le moteur, une bibliothèque de variables organisée par domaine physique et des cas d'étude citables.
- **Frontend — React + TypeScript + Tailwind.** Une interface responsive de niveau ingénierie avec rendu des équations en KaTeX, affichage explicite de la matrice dimensionnelle, thèmes clair/sombre, internationalisation complète français/anglais et export JSON/LaTeX.
- **Exécution dans le navigateur — Pyodide (WebAssembly).** Pour la démo publique, *le même* moteur Python est compilé en WebAssembly et s'exécute côté client via Pyodide. Le résultat est un site **100 % statique, fonctionnel hors-ligne**, hébergé directement sur GitHub Pages — instantané, gratuit et sans temps de démarrage.
- **Qualité logicielle.** Tests unitaires et d'intégration, linting et typage statique (Ruff, Mypy), images Docker, et CI/CD GitHub Actions pour l'API comme pour la démo statique.

## Compétences démontrées

- **Calcul scientifique & modélisation :** analyse dimensionnelle, algèbre linéaire exacte, mathématiques symboliques.
- **Architecture logicielle :** séparation nette entre un moteur réutilisable, une couche API et une interface ; typage de bout en bout.
- **Intégration web :** front end React/TypeScript et la prouesse non triviale d'exécuter une véritable pile scientifique Python dans le navigateur via WebAssembly.
- **Livraison & DevOps :** tests automatisés, conteneurisation et déploiement continu sur GitHub Pages.

Ce projet illustre, de façon compacte, la capacité à mener un sujet de physique appliquée d'un simple script de recherche jusqu'à un produit soigné et déployable.
