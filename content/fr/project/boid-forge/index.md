---
draft: false
title: "BoidForge : ingénierie des comportements collectifs du Python au C natif"
summary: "Comment transformer un modèle de nuée tiré des manuels en une simulation qui passe à l'échelle de dizaines de milliers d'agents et se rend comme un fluide ? Cette étude de cas présente l'algorithme des boids, quatre backends de solveur de plus en plus rapides comparés côte à côte (jusqu'à environ 330 fois plus rapides que le Python naïf), et un moteur de visualisation GPU conçu avec ModernGL."
authors:
  - admin
tags:
  - Scientific Python
  - Python
  - C / API C de CPython
  - NumPy
  - Calcul haute performance
  - ModernGL
  - GPU
  - Simulation
  - Optimisation
date: '2026-06-05T00:00:00Z'
toc: true

# URL externe optionnelle (remplace la page de détail du projet).
external_link: ''

image:
  caption: "Un rendu 4K de la scène turbulence de BoidForge, coloré par la vitesse"
  focal_point: Smart
  preview_only: false

links:
url_code: 'https://github.com/vcaries/boid_forge'
url_pdf: ''
url_slides: ''
url_video: 'https://youtu.be/5iVkLb3eyhE'
---

## En une minute {#en-une-minute}

**BoidForge** est un simulateur de nuées 2D bâti autour d'un principe unique : une nuée est *calculée* une fois puis *rendue* ensuite, jamais les deux en même temps. Un **solveur** fait avancer la physique et écrit chaque pas de temps dans un fichier binaire compact. Un **moteur de visualisation** distinct rejoue ensuite ce fichier sur le GPU. Les deux moitiés ne partagent aucune mémoire, seulement un format sur disque, de sorte que chacune peut être optimisée séparément.

Il en résulte un projet à parts égales calcul numérique et graphisme temps réel. Le même modèle de nuée est implémenté dans **quatre backends interchangeables**, depuis une référence Python naïve jusqu'à une **extension C** écrite à la main, et tous les quatre produisent des résultats strictement identiques jusqu'au dernier bit. Un moteur de rendu **ModernGL** transforme ensuite les trajectoires brutes en la séquence cinématographique ci-dessous.

{{< youtube 5iVkLb3eyhE >}}

<figcaption style="text-align:center;font-size:0.9em;margin-top:0.5em;"><strong>Vidéo.</strong> La scène <em>turbulence</em>, rendue hors-ligne en 4K à 60&nbsp;ips et colorée par la vitesse. Elle a été produite en rejouant une simulation enregistrée dans le moteur de visualisation GPU décrit plus bas.</figcaption>

👉 **[Code source sur GitHub](https://github.com/vcaries/boid_forge)**

### Points forts {#points-forts}

- **Un modèle, quatre backends, une sortie identique.** Python naïf (L1), NumPy vectorisé (L2), un hachage spatial sur grille uniforme (L3) et un noyau natif C/CPython (L4), tous identiques bit à bit sous un contrat de déterminisme strict.
- **Jusqu'à environ 330 fois plus rapide.** Le backend C atteint environ 120 à 330 fois le débit de la référence naïve sur la plage testée, et est conçu pour passer à l'échelle de dizaines de milliers d'agents.
- **Visualisation GPU en ModernGL.** Sprites instanciés, accumulation HDR additive, traînées de mouvement, bloom et tonemapping ACES, rendus sans affichage et transmis directement à FFmpeg pour l'export 4K.
- **Reproductible par construction.** Chaque résultat est une fonction pure de la configuration et d'une graine, si bien que les mêmes entrées donnent les mêmes octets sur n'importe quelle machine.

## Inspirations {#inspirations}

Ce projet est né de deux références de la culture scientifique et technique en ligne. La première est **Smarter Every Day**, dont la [vidéo sur les murmurations d'étourneaux](https://www.youtube.com/watch?v=4LWmRuB-uNU) montre comment des milliers d'oiseaux peuvent se comporter comme un seul corps fluide, et pose la question naturelle de la façon dont un tel ordre peut émerger sans chef et sans plan. La seconde est **Sebastian Lague** et sa série *Coding Adventures*, dont l'[épisode consacré aux boids](https://www.youtube.com/watch?v=bqtqltqcQhw) montre comment quelques règles locales se traduisent en code et combien de beauté visuelle une simulation simple peut contenir. BoidForge est ma manière de prendre cette curiosité au sérieux en ingénieur : reproduire le phénomène fidèlement, le pousser à une échelle où l'émergence devient évidente, et le rendre assez bien pour rendre justice aux véritables murmurations.

## Le modèle de nuée {#le-modele}

Le comportement de nuée est un phénomène *émergent*. Il n'y a ni chef ni plan global, et pourtant des milliers d'agents s'organisent en un mouvement cohérent, semblable à un fluide. La formulation classique est le modèle des **boids** de Craig Reynolds (1987), dans lequel chaque agent obéit à trois règles de pilotage locales, calculées uniquement à partir des voisins situés dans un rayon donné.

Soit un agent $i$ de position $\mathbf{p}_i$ et de vitesse $\mathbf{v}_i$. Notons $\mathcal{N}_i$ l'ensemble de ses voisins situés dans le rayon de la règle évaluée. Chaque règle produit une accélération de pilotage.

**La séparation** empêche la nuée de s'effondrer sur elle-même. Chaque agent est repoussé par ses voisins proches, et la poussée est d'autant plus forte qu'ils sont près :

$$\mathbf{a}_{\text{sep}} = w_{\text{sep}} \sum_{j \in \mathcal{N}_i} \frac{\mathbf{p}_i - \mathbf{p}_j}{\lVert \mathbf{p}_i - \mathbf{p}_j \rVert^{2}}$$

La pondération en inverse du carré est le détail important : un voisin deux fois plus proche repousse quatre fois plus fort, ce qui espace les agents et évite les collisions.

**L'alignement** fait voyager les voisins de concert, en orientant chaque agent vers la vitesse moyenne $\overline{\mathbf{v}}$ de son voisinage :

$$\mathbf{a}_{\text{ali}} = w_{\text{ali}} \left( \overline{\mathbf{v}} - \mathbf{v}_i \right)$$

**La cohésion** maintient le groupe rassemblé, en dirigeant chaque agent vers le centre de masse local $\overline{\mathbf{p}}$ de son voisinage :

$$\mathbf{a}_{\text{coh}} = w_{\text{coh}} \left( \overline{\mathbf{p}} - \mathbf{p}_i \right)$$

Les trois contributions sont sommées en une seule accélération $\mathbf{a}_i$, dont la norme est plafonnée à une force de pilotage maximale. La vitesse est alors avancée par un pas d'Euler explicite, puis bornée à une plage $[v_{\min}, v_{\max}]$ pour que les agents ne se figent jamais ni ne s'emballent :

$$\mathbf{v}_i \leftarrow \mathbf{v}_i + \mathbf{a}_i \Delta t$$

Enfin, la position est avancée avec cette nouvelle vitesse, et une règle de bord (rebouclage ou réflexion) maintient la nuée à l'intérieur du domaine :

$$\mathbf{p}_i \leftarrow \mathbf{p}_i + \mathbf{v}_i \Delta t$$

Chaque règle possède son **propre rayon**, et les trois poids $w_{\text{sep}}$, $w_{\text{ali}}$, $w_{\text{coh}}$ donnent à une simulation son caractère. Leur réglage est ce qui produit les scènes *murmuration*, *banc de poissons*, *plasma* et *turbulence* du dépôt. Le modèle est court à énoncer. Le travail d'ingénierie consiste à le rendre rapide et reproductible.

## Le goulot d'étranglement de calcul {#goulot}

Le coût du modèle est dominé par une seule question. Pour chaque agent, quels sont les autres agents qui sont ses voisins ? Répondue naïvement, chaque agent est comparé à tous les autres, soit $O(N^2)$ calculs de distance par pas de temps. À quelques centaines d'agents, cela reste inoffensif. À des dizaines de milliers, c'est sans espoir, car la croissance quadratique signifie qu'une nuée dix fois plus grande coûte cent fois plus cher.

BoidForge s'attaque au problème selon deux axes indépendants, et donne à chacun son propre backend afin que la contribution de chaque idée puisse être *mesurée* plutôt que supposée :

1. **Abaisser le facteur constant.** Effectuer le même travail $O(N^2)$, mais l'exprimer en moins d'instructions, plus rapides. C'est le chemin de la boucle Python vers le NumPy vectorisé, puis vers le C natif.
2. **Abaisser la complexité.** Cesser totalement d'effectuer un travail $O(N^2)$, en n'inspectant que les agents susceptibles d'être voisins. C'est la grille spatiale, qui ramène la recherche à environ $O(N)$.

Les quatre backends sont soumis à un unique **contrat de déterminisme** : pour une même configuration et une même graine, ils doivent émettre une sortie identique octet par octet. Le backend naïf est la référence, et tout backend qui s'en écarte est faux par définition. Un test exécute chaque backend et compare leurs images. C'est une contrainte exigeante, car elle force même le noyau C à reproduire l'ordre de sommation `float32` exact de NumPy, mais c'est elle qui rend les gains de vitesse dignes de confiance plutôt que simplement rapides.

## Quatre backends, et ce que chacun apporte {#backends}

### L1, Python naïf (la référence) {#l1}

Une implémentation directe, toutes paires, avec une boucle Python explicite sur chaque paire d'agents. Elle est volontairement simple, car son seul rôle est de *définir la correction*. Tous les autres backends sont validés contre elle. C'est aussi, sans surprise, le plus lent, puisque le surcoût par élément de l'interpréteur Python s'ajoute au travail $O(N^2)$.

### L2, NumPy vectorisé {#l2}

Le même algorithme toutes paires, réexprimé avec NumPy. Les termes de déplacement, de distance et de séparation par paire sont construits une fois sous forme de tableaux entiers, et les bornages ainsi que l'intégration s'exécutent en opérations groupées sur ces tableaux.

*Pourquoi c'est plus rapide.* L'arithmétique sort de l'interpréteur Python pour passer dans les boucles C compilées de NumPy, ce qui supprime le surcoût par élément. Sur les petites et moyennes nuées, le gain est d'environ un facteur deux. Il n'est pas gratuit pour autant. Les tableaux par paire coûtent une *mémoire* $O(N^2)$, et au sommet de la plage testée, le coût du transfert de ces grands tableaux en mémoire annule le gain, au point que L2 est légèrement plus lent que L1 à 2000 agents. Ce compromis est la leçon en soi : la vectorisation achète de la vitesse avec de la mémoire, et à grande échelle, la mémoire devient la ressource limitante.

### L3, hachage spatial sur grille uniforme {#l3}

Le premier changement *algorithmique*. Les agents sont rangés dans une grille dont le côté de cellule égale le rayon de voisinage. Chaque agent n'inspecte alors que sa propre cellule et les huit qui l'entourent, un bloc de trois sur trois, au lieu de toute la nuée. Comme le côté de cellule égale le rayon, tout voisin réel tombe forcément dans ce bloc, de sorte que la grille élague du travail sans jamais manquer un voisin.

*Pourquoi c'est plus rapide.* Cela fait passer la complexité de la recherche de voisins de $O(N^2)$ à environ $O(N)$. Le travail par agent cesse de croître avec la taille de la nuée et ne dépend plus que de la densité locale. C'est l'idée qui rend les grandes nuées traitables en principe. En Python pur, toutefois, la gestion de la construction de la grille et du rassemblement des candidats comporte assez de surcoût pour que, aux tailles modestes testées ici, son temps reste proche de celui de la boucle naïve. L'algorithme est correct, mais il attend un langage hôte plus rapide pour porter ses fruits.

### L4, extension C native (la cible de production) {#l4}

Cet hôte plus rapide est une **extension C de CPython** écrite à la main, développée avec l'API C brute et compilée avec CMake via scikit-build-core. Elle combine la grille $O(N)$ de L3 à un ensemble d'optimisations de bas niveau hors de portée de Python :

- **Des tampons en structure de tableaux, partagés sans copie.** L'état réside en quatre tableaux `float32` contigus (positions et vitesses) partagés avec NumPy via le protocole tampon. Il n'y a pas de copie, pas de surcoût d'objet par agent, et une disposition mémoire que le processeur peut parcourir efficacement en flux.
- **Un tri par comptage en cellules.** La grille est construite par un tri par comptage dans une disposition compacte plutôt que par une table de hachage, de sorte que le rassemblement des voisins est une boucle serrée sur des indices contigus, et non des recherches dans un dictionnaire.
- **Le verrou de l'interpréteur est libéré** autour de la boucle de calcul, si bien que le gros du travail numérique s'exécute en véritable code natif, affranchi du verrou global de Python.
- **Aucune allocation mémoire dans la boucle critique.** Un unique espace de travail est dimensionné une fois par pas de temps, et la boucle interne par agent n'appelle jamais l'allocateur.

*Pourquoi c'est plus rapide.* Chacun de ces points supprime une couche de surcoût à laquelle les backends Python ne peuvent échapper, à savoir la répartition de l'interpréteur, l'indirection d'objets et la pression sur l'allocateur, tout en conservant la recherche de voisins $O(N)$. Ensemble, ils procurent environ 120 à 330 fois le débit de la référence naïve et mettent des dizaines de milliers d'agents à portée. Et tout cela en produisant une sortie identique à L1 jusqu'au bit, ce qui a exigé de reproduire exactement en C l'algorithme de sommation par paires de NumPy afin que l'arrondi `float32` corresponde.

## Bancs d'essai {#benchmarks}

Le banc de mesure chronomètre chaque backend sur un balayage de tailles de nuée, de 100 à 2000 agents, sur 200 pas chacun et après un préchauffage, en enregistrant le temps moyen par image et l'accélération relative à L1.

<figure>
  <a href="/media/boid-forge/scaling.png" target="_blank" rel="noopener"><img src="/media/boid-forge/scaling.png" alt="Temps par image en fonction du nombre d'agents, log-log, pour les quatre backends" style="width:100%;height:auto;"></a>
  <figcaption><strong>Figure 1.</strong> Temps par image en fonction de la taille de la nuée, en axes logarithmiques. Les backends naïf (L1), vectorisé (L2) et hachage spatial Python (L3) restent proches à ces tailles, tandis que le backend C natif (L4) s'exécute un à deux ordres de grandeur en dessous. L'écart qui se creuse vers la droite est la grille $O(N)$ qui se détache du coût toutes paires $O(N^2)$. <em>(Cliquez pour agrandir.)</em></figcaption>
</figure>

<figure>
  <a href="/media/boid-forge/speedup.png" target="_blank" rel="noopener"><img src="/media/boid-forge/speedup.png" alt="Accélération de chaque backend par rapport à la référence naïve, par taille de nuée" style="width:100%;height:auto;"></a>
  <figcaption><strong>Figure 2.</strong> Accélération par rapport à la référence naïve. Le backend natif domine, culminant autour de 330 fois à 200 agents et se maintenant bien au-dessus de 100 fois sur toute la plage, tandis que les optimisations Python pur (L2 et L3) restent proches de 1 à ces tailles. Cela confirme que le gain décisif vient du passage de l'algorithme $O(N)$ en C, et non de la seule vectorisation.</figcaption>
</figure>

À 2000 agents, la référence naïve dépense environ 202 ms par image, soit l'équivalent de 5 images par seconde, tandis que le backend C dépense environ 1,7 ms, soit l'équivalent de 590 images par seconde. C'est la même physique calculée environ 120 fois plus vite, avec une avance qui continue de croître à mesure que la nuée grandit.

## Visualisation avec ModernGL {#visualisation}

Le moteur de rendu ne simule jamais. Il lit les images précalculées dans le flux binaire et transforme chacune en image sur le GPU. Il est bâti directement sur **ModernGL**, une liaison fine et moderne vers OpenGL 3.3, avec des shaders GLSL écrits à la main, et c'est délibérément un petit pipeline de post-traitement plutôt qu'un moteur de jeu :

1. **Téléversement et tracé.** Chaque image est téléversée dans un tampon de sommets GPU et chaque agent est tracé comme un unique **sprite ponctuel**. Le fragment shader façonne chaque sprite en un cœur lumineux diffus entouré d'un large halo, et sa couleur est lue dans une petite texture de palette indexée par la vitesse, le cap, la densité locale ou une valeur fixe.
2. **Accumulation HDR additive.** Les sprites sont mélangés de manière additive dans un tampon en virgule flottante, si bien que les agents qui se chevauchent accumulent une véritable luminosité. C'est ce qui donne aux grappes denses leur aspect lumineux.
3. **Traînées de mouvement.** Au lieu d'effacer ce tampon entre deux images, on l'estompe légèrement vers le noir. Les agents laissent donc derrière eux des traînées décroissantes, source de la sensation de mouvement soyeuse et fluide.
4. **Bloom.** Une passe de seuil ne conserve que les pixels les plus lumineux, un flou gaussien séparable les étale, et la lueur est réinjectée, produisant le halo cinématographique autour des régions rapides et denses.
5. **Composition.** Un dernier shader plein écran applique un tonemapping filmique ACES pour ramener la scène à grande plage dynamique dans une plage affichable, avec exposition, vignette optionnelle, teinte de fond et correction gamma.

Comme le contexte GPU peut être créé hors écran, ce même moteur de rendu fonctionne sans affichage sur une machine sans écran. Pour la vidéo, les images rendues sont transmises directement à un sous-processus **FFmpeg** qui encode en H.264, sans jamais conserver tout le clip en mémoire. C'est ainsi qu'a été produite la séquence 4K en tête de page.

## Architecture : deux sous-systèmes, un contrat {#architecture}

La règle de conception derrière tout ce qui précède est une séparation stricte entre *calculer* la nuée et la *dessiner* :

```
Solveur (calcul)  --->  flux binaire .bfs  --->  Moteur de visualisation  --->  images / vidéo
```

Le solveur n'importe rien de la couche de visualisation, sans OpenGL ni aucun graphisme, et la couche de visualisation ne fait jamais avancer la physique. Leur seule connaissance partagée est un petit **format binaire** versionné (`.bfs`) : un en-tête de 32 octets suivi d'un enregistrement par image contenant le nombre d'agents et les quatre tableaux `float32` bout à bout. Cette disposition est choisie pour que le solveur puisse écrire chaque tableau en une seule opération groupée et que le moteur de rendu puisse le mapper directement dans un tampon GPU sans réempaquetage de part et d'autre. Un test statique sur les frontières d'import garantit la séparation pour qu'elle ne s'érode pas avec le temps.

Ce découplage est ce qui permet d'optimiser le solveur pour le débit brut et le moteur de rendu pour la qualité d'image, chacun selon ses propres critères. C'est aussi pourquoi une longue simulation peut être calculée une fois puis rendue à nouveau plus tard avec d'autres couleurs, traînées ou résolutions, autant de fois que nécessaire.

## Compétences démontrées {#competences}

- **Calcul haute performance :** réduction de complexité algorithmique de $O(N^2)$ à $O(N)$ par hachage spatial, vectorisation NumPy et ses compromis mémoire, et une extension C de CPython écrite à la main avec tampons sans copie, libération du verrou de l'interpréteur et boucle critique sans allocation.
- **Rigueur numérique :** un contrat de déterminisme exact au bit près entre quatre implémentations indépendantes, dont la reproduction en C de la sommation par paires `float32` de NumPy.
- **GPU et graphisme temps réel :** un pipeline ModernGL et GLSL avec accumulation HDR, traînées de mouvement, bloom et tonemapping ACES, fonctionnant sans affichage et exportant via FFmpeg.
- **Architecture logicielle :** deux sous-systèmes strictement découplés reliés seulement par un format binaire versionné, avec une frontière d'import imposée.
- **Discipline d'ingénierie :** un code Python typé, documenté et testé (`ruff`, `mypy --strict`, `pytest`), une compilation native CMake et scikit-build-core, et la reproductibilité traitée comme une exigence de premier ordre.

## Dépôt {#depot}

L'intégralité du code source est ouverte, y compris les quatre backends de solveur, le noyau C, la couche d'entrée et sortie binaire, le banc de mesure et le moteur de visualisation ModernGL.

Le code se trouve sur **[github.com/vcaries/boid_forge](https://github.com/vcaries/boid_forge)**, accompagné d'un document d'architecture qui décrit en détail le format binaire et le contrat de déterminisme.

## Conclusion {#conclusion}

Un modèle de nuée tient en trois lignes d'algèbre vectorielle. Le faire *passer à l'échelle* est un projet d'ingénierie. BoidForge mène le modèle d'une référence Python transparente à un noyau C natif deux ordres de grandeur plus rapide, prouve à chaque étape que la vitesse supplémentaire ne coûte rien en correction, puis rend le résultat sous une forme réellement digne d'être regardée, le tout dans une architecture nette où calcul et rendu ne se touchent jamais. Le plus difficile n'a jamais été les boids. C'était de les rendre rapides, reproductibles et beaux.
