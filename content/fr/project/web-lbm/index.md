---
draft: false
title: "Web-LBM : une soufflerie CFD temps réel dans le navigateur"
summary: "Que faut-il pour faire tourner un véritable solveur de mécanique des fluides numérique à cadence interactive dans un onglet de navigateur ? Web-LBM est une soufflerie 2D fondée sur la méthode de Boltzmann sur réseau : un moteur C compilé en WebAssembly, un pipeline de rendu WebGL2 sans copie, un modèle de turbulence et du multithreading — le tout sur une page 100 % statique."
authors:
  - admin
tags:
  - C / WebAssembly
  - CFD
  - Boltzmann sur réseau
  - Aérodynamique
  - Calcul haute performance
  - WebGL
  - Simulation
  - Web
date: '2026-06-12T00:00:00Z'
toc: true

# URL externe optionnelle (remplace la page de détail du projet).
external_link: ''

image:
  caption: 'L''allée tourbillonnaire de von Kármán derrière un cylindre, calculée et rendue en direct dans le navigateur'
  focal_point: Smart

links:
  - name: Essayer la simulation
    url: 'https://vcaries.github.io/web_lbm/'
    icon_pack: fas
    icon: play
url_code: 'https://github.com/vcaries/web_lbm'
url_pdf: ''
---

## En une minute

**Web-LBM** est une soufflerie numérique bidimensionnelle interactive qui s'exécute entièrement dans votre navigateur. Derrière le canvas se trouve un véritable solveur de **mécanique des fluides numérique (CFD)** — un moteur **Boltzmann sur réseau (D2Q9)** écrit en C, compilé en **WebAssembly** et rendu sur le GPU via **WebGL2**. On peut y déposer un cylindre ou un profil NACA, changer l'angle d'attaque, mettre un obstacle en rotation pour ressentir l'effet Magnus, peindre sa propre géométrie à la souris et observer la réponse du sillage — avec les coefficients de portance et de traînée en direct, et même des microphones virtuels qui permettent de *voir le son* du lâcher tourbillonnaire.

La CFD vit d'ordinaire sur des clusters et des calculs de nuit. L'amener dans un onglet de navigateur — sans installation, sans serveur, sans framework, hébergée en simples fichiers statiques sur GitHub Pages — est à la fois un parti pris pédagogique et un exercice d'ingénierie : chaque contrainte de la plateforme (pas de mémoire partagée par défaut, pas de système de fichiers, un seul thread sauf à le mériter) doit être résolue sans sacrifier ni la fidélité physique ni l'interactivité.

👉 **[Essayer la simulation](https://vcaries.github.io/web_lbm/)** · **[Code source sur GitHub](https://github.com/vcaries/web_lbm)**

### Points clés

- **Un vrai solveur, pas un jouet.** Boltzmann sur réseau D2Q9 avec collision BGK (ou MRT à la compilation), un modèle de turbulence **LES de Smagorinsky**, une collision régularisée de Hermite pour la stabilité, une entrée en vitesse de Zou–He, des couches éponges absorbantes et l'évaluation des efforts par échange de quantité de mouvement pour des $C_l$ / $C_d$ en direct.
- **Des performances temps réel.** Une boucle chaude sans branchement, vectorisée SIMD, et des **threads WebAssembly** (pthreads sur `SharedArrayBuffer`) avec un partitionnement par lignes, déterministe et sans verrou.
- **Un rendu sans copie.** Les champs voyagent du tas wasm jusqu'à l'écran sans la moindre copie intermédiaire : vues typées → texture WebGL2 `R32F` → table de couleurs dans le fragment shader.
- **L'aéroacoustique en prime.** La LBM étant faiblement compressible, le moteur résout les ondes acoustiques : vues schlieren ($|\nabla\rho|$) et dilatation ($\nabla\cdot\mathbf{u}$), plus des microphones virtuels avec FFT en direct qui captent le sifflement éolien du sillage.
- **Un déploiement 100 % statique.** Deux variantes du moteur (mono- et multi-thread) sélectionnées à l'exécution ; un service worker fournit les en-têtes d'isolation cross-origin que GitHub Pages ne peut pas envoyer.

## Pourquoi la CFD dans le navigateur ?

Trois raisons, par ordre de difficulté croissante.

**La pédagogie.** La mécanique des fluides s'enseigne avec des équations et se valide avec des simulations coûteuses, mais *l'intuition* naît du lien immédiat entre cause et effet : inclinez un profil et observez le décrochage, faites tourner un cylindre et regardez la portance apparaître. Une simulation interactive dont la boucle de rétroaction se mesure en millisecondes est un outil d'apprentissage fondamentalement différent d'une figure statique.

**L'accessibilité.** Une page web sans installation ni backend touche tout le monde — étudiants, collègues, recruteurs — sur n'importe quelle machine, indéfiniment, pour un coût d'hébergement nul. Cela impose que tout le solveur tourne côté client : exactement ce que WebAssembly rend possible.

**Le défi d'ingénierie.** La CFD temps réel met toute la pile à l'épreuve : une méthode numérique assez stable pour survivre à tout ce que l'utilisateur lui impose, une organisation mémoire que le compilateur sait vectoriser, un modèle de threading compatible avec les contraintes de sécurité du navigateur et un chemin de rendu assez rapide pour ne jamais devenir le goulot d'étranglement. Résoudre les quatre à la fois est le cœur de ce projet.

## La physique : Boltzmann sur réseau en bref

### Un autre chemin vers la dynamique des fluides

La CFD classique discrétise directement les **équations de Navier–Stokes** : vitesse et pression vivent sur un maillage, et chaque pas de temps exige la résolution de systèmes couplés *globaux* — typiquement une équation de Poisson pour la pression, dont la solution relie chaque cellule du domaine à toutes les autres.

La **méthode de Boltzmann sur réseau (LBM)** emprunte une voie située un niveau en dessous de la description macroscopique. Elle fait évoluer des **fonctions de distribution de particules** $f_i(\mathbf{x}, t)$ — la quantité de fluide au nœud $\mathbf{x}$ se déplaçant le long d'un petit ensemble de vitesses discrètes $\mathbf{c}_i$. Les champs macroscopiques sont simplement les moments de ces distributions :

$$\rho = \sum_i f_i, \qquad \rho\,\mathbf{u} = \sum_i f_i\,\mathbf{c}_i$$

Un développement de Chapman–Enskog montre que ce système cinétique reproduit les équations de Navier–Stokes incompressibles dans la limite des faibles nombres de Mach. La viscosité du fluide est pilotée par un unique temps de relaxation $\tau$ :

$$\nu = c_s^2\left(\tau - \tfrac{1}{2}\right)$$

Ce qui rend la LBM exceptionnelle pour ce projet, c'est sa **localité** : chaque nœud ne se met à jour qu'à partir de ses voisins immédiats. Pas de résolution globale, pas d'algèbre linéaire, pas de boucle de convergence — donc un coût par pas de temps fixe et prévisible, un algorithme qui se parallélise presque trivialement, et une simulation *naturellement instationnaire* : le lâcher tourbillonnaire n'est pas une option que l'on active, c'est ce que la méthode calcule par défaut. En bonus, la LBM est faiblement compressible : les ondes de pression se propagent physiquement, et la simulation fait de l'acoustique gratuitement.

### Collision et propagation

Chaque pas de temps se compose de deux opérations conceptuellement simples. La **collision** relaxe les distributions vers un équilibre local (approximation BGK) :

$$f_i(\mathbf{x}, t^{+}) = f_i(\mathbf{x}, t) - \frac{1}{\tau}\left[f_i(\mathbf{x}, t) - f_i^{\mathrm{eq}}(\rho, \mathbf{u})\right]$$

où l'équilibre est un développement au second ordre de la distribution de Maxwell–Boltzmann :

$$f_i^{\mathrm{eq}} = w_i\,\rho\left[1 + \frac{\mathbf{c}_i\cdot\mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i\cdot\mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}\cdot\mathbf{u}}{2c_s^2}\right]$$

La **propagation** (*streaming*) décale ensuite chaque distribution post-collision vers le nœud voisin dans sa direction de déplacement :

$$f_i(\mathbf{x} + \mathbf{c}_i\,\Delta t,\; t + \Delta t) = f_i(\mathbf{x}, t^{+})$$

La collision est de l'arithmétique purement locale ; la propagation, un pur déplacement mémoire. Cette séparation — du calcul intensif sans communication, puis de la communication sans calcul — est exactement la structure qu'adorent les unités SIMD et les processeurs multicœurs, et l'implémentation décrite plus bas l'exploite délibérément.

### Pourquoi D2Q9

Le moteur utilise le réseau **D2Q9** : deux dimensions, neuf vitesses (repos, quatre axiales, quatre diagonales) avec les poids $w_0 = 4/9$, $w_{1\text{–}4} = 1/9$, $w_{5\text{–}8} = 1/36$. C'est le plus petit réseau 2D dont les moments de vitesse sont suffisamment isotropes pour retrouver correctement Navier–Stokes — moins de directions biaiseraient la physique le long des axes de la grille, davantage coûteraient mémoire et bande passante sans gain à ce niveau de description. Neuf champs `float` par nœud fixent aussi le budget mémoire : une grille 600 × 300 tient confortablement dans quelques dizaines de mégaoctets de tas wasm.

### Conditions aux limites

Les frontières sont l'endroit où une implémentation LBM fait ses preuves : après la propagation, les distributions entrant dans le domaine depuis l'extérieur sont inconnues et doivent être reconstruites :

- **Entrée** — une condition en vitesse de **Zou–He** impose le profil d'entrée (uniforme, couche cisaillée ou jet) en reconstruisant les distributions inconnues à partir des contraintes de masse et de quantité de mouvement. Un démarrage progressif sur 400 pas accompagne chaque (ré)initialisation pour que le démarrage impulsif ne lance pas une onde de choc dans la veine.
- **Sortie** — une extrapolation à gradient nul, adossée à une **couche éponge absorbante** qui augmente progressivement la dissipation près de la frontière, pour que tourbillons et ondes acoustiques quittent le domaine au lieu de s'y réfléchir.
- **Obstacles** — le **rebond (*bounce-back*)** : les distributions qui frappent un nœud solide repartent d'où elles viennent, produisant une paroi adhérente sans aucun maillage. Sa variante à **paroi mobile** ajoute la quantité de mouvement de la paroi aux populations réfléchies — c'est là toute l'implémentation du cylindre tournant, et l'effet Magnus découle de la physique. La somme des quantités de mouvement échangées dans ces réflexions donne l'effort aérodynamique sur chaque corps — les $C_l$ et $C_d$ affichés en direct — pour un coût quasi nul.
- **Parois de la veine** — au choix : glissement libre (réflexion spéculaire) ou adhérence (rebond).

## Mise en œuvre

### Architecture

Le projet se compose de deux parties proprement séparées, reliées par un unique tampon mémoire partagé :

```
Moteur C (lbm.c, C99)  --emcc-->  WebAssembly + tas wasm
                                        │ vues Float32Array sans copie
Frontend ES6 vanilla  ── textures WebGL2 R32F ──>  LUT de couleurs dans le shader
```

- **Le moteur** est un unique fichier C99 : le solveur D2Q9, la LES, les conditions aux limites, les rastériseurs analytiques de formes (cylindre, plaque plane, NACA 0012 / 4412), l'évaluation des efforts et le calcul des champs dérivés (vitesse, pression, vorticité, schlieren, dilatation). Il expose une petite API C plate (`lbm_init`, `lbm_step`, `lbm_set_params`, …) et ignore tout de JavaScript.
- **Le frontend** est en modules ES6 vanilla — pas de framework, pas de bundler, aucune étape de build au-delà d'`emcc` lui-même. `main.js` pilote la boucle de simulation et l'interface, `renderer.js` possède WebGL2, `obstacles.js` définit les formes analytiques.
- **Deux variantes du moteur** sont produites à partir de la même source : une version mono-thread qui fonctionne partout, et une version `-pthread` utilisant les threads WebAssembly. L'application détecte `crossOriginIsolated` au démarrage et choisit la meilleure, avec repli transparent.

### Le chemin de données sans copie

La règle cardinale du pipeline de rendu : **les champs ne sont jamais copiés côté JavaScript**. Le moteur C calcule, par exemple, la vorticité dans un tableau `float` du tas wasm ; JavaScript enveloppe cette mémoire dans une *vue* `Float32Array` (aucune allocation, aucune copie) et la passe directement à `texSubImage2D`, qui la téléverse dans une texture flottante mono-canal (`R32F`). Le fragment shader fait ensuite correspondre les valeurs aux couleurs via une petite texture de table de correspondance — tout l'habillage visuel coûte une lecture de texture par pixel et vit sur le GPU.

Deux subtilités maintiennent cette promesse. Quand le tas wasm grandit (l'utilisateur choisit une grille plus fine), l'`ArrayBuffer` sous-jacent se détache et chaque vue doit être reconstruite — l'application le fait paresseusement, à la demande. Et dans la version multithread, le tas est un `SharedArrayBuffer`, que certains navigateurs refusent de téléverser directement ; un unique petit tampon de transit constitue la seule exception sanctionnée à la règle du zéro-copie.

### Du multithreading dans un navigateur

Le balayage intérieur est **partitionné par lignes** sur un pool de pthreads wasm, avec des barrières séparant les phases de chaque pas de temps. Le partitionnement garantit que chaque case du tableau de destination a *exactement un* producteur — les threads ne sont jamais en concurrence, donc ni verrous ni atomiques dans le chemin chaud. Les contributions aux efforts sont réduites dans un ordre de threads fixe, ce qui rend les résultats **déterministes au bit près à nombre de threads donné** — une exigence empruntée aux bonnes pratiques du HPC, où « rapide mais légèrement différent à chaque exécution » est la cachette préférée des bugs.

Le threading en navigateur a un piège : `SharedArrayBuffer` exige que la page soit **isolée cross-origin**, ce qui requiert des en-têtes HTTP COOP/COEP qu'un hébergeur statique comme GitHub Pages ne peut pas envoyer. Web-LBM résout cela avec un **service worker** de portée racine qui injecte les en-têtes côté client (un rechargement automatique à la première visite). Si quoi que ce soit échoue dans cette chaîne — navigateur ancien, isolation partielle — l'application démarre silencieusement le moteur mono-thread : l'amélioration progressive appliquée au HPC.

### Interaction

Tout, dans la soufflerie, se manipule pendant que la simulation tourne : les obstacles se placent au clic, pivotent, tournent sur eux-mêmes (cylindres en rotation) ou se **peignent à main levée** à la souris, directement dans le masque d'obstacles. Les cellules peintes sont rééchantillonnées quand la résolution de grille change, tandis que les formes prédéfinies sont re-rastérisées *analytiquement* depuis leur registre — un profil NACA reste donc un profil NACA net à n'importe quelle résolution. L'écoulement se visualise en vitesse, pression, vorticité, schlieren ou dilatation, avec des surcouches de lignes de courant et de particules, et des **microphones virtuels** se déposent n'importe où dans le champ pour tracer la FFT en direct du signal de pression local — en placer un derrière un cylindre révèle le pic spectral net de la fréquence de lâcher, la même physique que le sifflement du vent dans les fils.

## Défis d'ingénierie

### La stabilité numérique sans arbitre

Une simulation interactive ne peut pas refuser les entrées de l'utilisateur : quels que soient le nombre de Reynolds, la forme d'obstacle ou la résolution choisis, le solveur ne doit pas diverger. Le BGK brut devient instable quand $\tau \to 1/2$ (hauts nombres de Reynolds) ; le moteur superpose donc plusieurs défenses, chacune visant un mode de défaillance distinct :

- Un **modèle LES de Smagorinsky** ($C_s = 0{,}18$) calcule une viscosité turbulente locale à partir du taux de déformation — obtenu en LBM directement depuis les distributions hors équilibre, sans différences finies — qui à la fois modélise les échelles turbulentes non résolues et éloigne le $\tau$ effectif de la limite instable précisément là où l'écoulement est le plus cisaillé.
- La **régularisation de Hermite** projette la partie hors équilibre des distributions sur sa composante physiquement signifiante (Hermite d'ordre deux) avant la collision, filtrant les modes parasites d'ordre supérieur qui, sinon, s'accumulent et déstabilisent les grilles grossières.
- Un **amortissement de viscosité de volume** dissipe sélectivement la partie acoustique du tenseur des contraintes, calmant les oscillations de pression sans toucher à la physique du cisaillement qui crée les tourbillons.
- Les **couches éponges et le démarrage progressif de l'entrée** éliminent les deux transitoires classiques — les ondes réfléchies en sortie et l'impulsion initiale.

Le résultat est une soufflerie qui survit aux mauvais traitements : c'est la différence entre une démo et un produit.

### Garder la boucle chaude… chaude

Le balayage collision-propagation des cellules intérieures domine le temps d'exécution, et il est écrit pour que **LLVM puisse le vectoriser automatiquement en SIMD WebAssembly** — un gain d'environ 3×. Cela impose une discipline : la boucle ne contient *aucun branchement*. Pas de test d'obstacle, pas de cas particulier de frontière ; le modèle LES est fondu dans l'arithmétique séquentielle, et des copies de pointeurs qualifiées `restrict` garantissent au compilateur l'absence d'aliasing. Les cellules solides sont traitées par une **passe de correction** séparée et bon marché, après le balayage. La leçon se généralise : structurer le code pour que le compilateur puisse *prouver* des propriétés bat régulièrement l'optimisation manuelle du code lui-même.

L'organisation des données sert le même objectif : une **structure de tableaux** de neuf champs `float` plats, indexés `y·Nx + x`, de sorte que la propagation dans chaque direction soit un déplacement mémoire contigu et que les voies SIMD chargent toujours des valeurs adjacentes.

### Le navigateur comme plateforme HPC

Le navigateur est un environnement hostile au regard des standards du HPC, et plusieurs de ses contraintes ont directement façonné la conception : la croissance de la mémoire wasm **détache toutes les vues actives** (gérée par reconstruction paresseuse des vues) ; `texSubImage2D` peut refuser les vues adossées à un `SharedArrayBuffer` (géré par l'unique tampon de transit) ; l'isolation cross-origin est inaccessible sur hébergement statique sans le service worker ; et le pool de threads doit être dimensionné et lancé au chargement du module, car on ne peut pas créer de workers de façon synchrone en cours de frame. Chaque contournement est modeste, mais savoir *où* ils sont nécessaires est exactement l'expertise de plateforme que ce projet visait à construire.

## Ce que vous pouvez explorer

Quelques expériences d'une minute chacune dans la [soufflerie en ligne](https://vcaries.github.io/web_lbm/) :

1. **Le lâcher tourbillonnaire** — gardez le cylindre par défaut, passez en vue vorticité et regardez l'allée de von Kármán s'établir ; le HUD montre $C_l$ oscillant à la fréquence de lâcher.
2. **Le décrochage** — placez un profil NACA 4412 et augmentez l'angle d'attaque : le coefficient de portance grimpe, puis l'écoulement décolle à l'extrados.
3. **L'effet Magnus** — faites tourner un cylindre et observez le sillage dévier et une portance stationnaire apparaître : la physique des coups francs enroulés.
4. **L'aéroacoustique** — passez en vue schlieren ou dilatation pour voir les ondes de pression rayonner depuis le sillage, puis déposez un microphone derrière le cylindre et retrouvez le ton de lâcher dans le spectre en direct.
5. **Votre propre géométrie** — peignez un obstacle arbitraire à la souris et regardez l'écoulement composer avec.

## Compétences démontrées

- **Mécanique des fluides numérique :** la méthode de Boltzmann sur réseau de bout en bout — choix du réseau, modèles de collision (BGK, MRT, régularisation), conditions aux limites, modélisation de la turbulence (LES de Smagorinsky), évaluation des efforts et aéroacoustique.
- **Méthodes numériques & calcul scientifique :** l'analyse de stabilité en pratique — identifier les modes de défaillance et superposer des remèdes ciblés ; un moteur physique en C99 portable avec tests de validation embarqués.
- **Ingénierie de la performance :** noyaux sans branchement adaptés au SIMD, organisation mémoire en structure de tableaux, multithreading déterministe sans verrou et séparation des chemins chauds et froids guidée par le profilage.
- **Architecture logicielle :** une frontière stricte moteur/frontend avec un contrat de données zéro-copie à travers la frontière C/JavaScript ; détection de capacités à l'exécution avec dégradation élégante.
- **Technologies web :** WebAssembly (Emscripten, threads wasm, mémoire partagée), WebGL2 (textures flottantes, colorisation dans le shader), service workers et déploiement entièrement statique.
- **Visualisation scientifique interactive & conception d'interface :** rendu de champs en temps réel, vues multiples physiquement signifiantes, et une interface qui invite à l'expérimentation sans mode d'emploi.
- **Communication scientifique :** rendre tangible — et ludique — une mécanique des fluides de niveau master pour un public technique généraliste.

## Dépôt

Tout le code est ouvert : le moteur C (abondamment commenté, jusqu'à chaque drapeau de compilation et sa justification), le moteur de rendu WebGL2, les scripts de build et les tests physiques de validation.

Le code vit sur **[github.com/vcaries/web_lbm](https://github.com/vcaries/web_lbm)** — et la soufflerie elle-même tourne sur **[vcaries.github.io/web_lbm](https://vcaries.github.io/web_lbm/)**.

## Conclusion

Web-LBM condense tout l'éventail de l'ingénierie de simulation — une méthode numérique cinétique, la modélisation de la turbulence, l'optimisation SIMD et multithread, le rendu GPU et une interaction de qualité produit — dans une seule page que chacun peut ouvrir. La méthode de Boltzmann sur réseau est le choix qui rend tout possible : locale, parallèle, naturellement instationnaire et discrètement capable d'acoustique. Le navigateur est la contrainte qui structure tout : chacune de ses limites a dû être contournée par l'ingénierie, jamais éludée. Le résultat : une soufflerie dans un onglet — et la démonstration que le *vrai* calcul scientifique n'est pas condamné à vivre derrière une file d'attente sur un cluster.
