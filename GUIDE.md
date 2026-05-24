# Guide du site `vcaries.github.io`

Guide pratique pour maintenir, traduire, référencer et faire évoluer ton site
personnel (Hugo + thème Hugo Blox « Academic CV », déployé sur GitHub Pages).

> **Avant tout — deux actions manuelles à faire une fois :**
> 1. Supprime le fichier verrou git resté de la session : `D:\Codes\vcaries.github.io\.git\index.lock`
>    (sinon `git` refusera de committer). Sous PowerShell : `Remove-Item .git\index.lock`
> 2. Supprime le dossier de démos du thème : `content\_TO_DELETE_theme_demo\`
>    (anciens articles/projets « Lorem ipsum » que je n'ai pas pu effacer depuis l'atelier).
>    PowerShell : `Remove-Item -Recurse -Force content\_TO_DELETE_theme_demo`

---

## 1. Ce qui a changé

- **Site bilingue (FR par défaut + EN).** Stratégie : i18n natif de Hugo avec
  un répertoire de contenu par langue.
  - Français servi à la racine : `https://vcaries.github.io/`
  - Anglais servi sous : `https://vcaries.github.io/en/`
- **Nouvelle arborescence de contenu :**
  ```
  content/
    fr/        ← contenu français (langue par défaut, à la racine)
    en/        ← contenu anglais (/en/)
  ```
  Les deux arbres ont **les mêmes noms de dossiers (slugs)**. C'est ce qui permet
  au sélecteur de langue (en haut à droite) de relier automatiquement chaque page
  à sa traduction.
- **Profil réécrit** (bio, rôle, centres d'intérêt) orienté ingénierie /
  freelance, en FR et EN.
- **Nouvelle section « Compétences & Services »** (4 cartes : Python scientifique,
  CFD & simulation, Data engineering & HPC, ML pour l'ingénierie) + pastilles de
  technos.
- **Nouvelle section « Projets »** (vue *showcase* avec filtres) :
  1 projet réel (ton solveur d'ordre réduit) + 3 modèles de projets à compléter.
- **Publications** mises à jour (date de parution IJTPP corrigée au 6 fév. 2025,
  liens DOI/HAL/source/projet, anciennes URL préservées via `aliases`).
- **Design** : feuille de style `assets/scss/custom.scss` (cartes, pastilles,
  hiérarchie, mode sombre).
- **SEO** : descriptions par langue, image de partage `static/media/og-cover.png`,
  balises Open Graph/Twitter (`layouts/partials/head_custom.html`),
  `layouts/robots.txt`, sitemap multilingue automatique.

---

## 2. Modifier le site en local

### Pré-requis (à installer une fois)

- **Hugo *extended*, version EXACTE `0.124.1`** (la même que le déploiement,
  voir `.github/workflows/publish.yaml`).
  - ⚠️ **N'utilise PAS une version trop récente de Hugo.** À partir de Hugo
    0.143, la fonction `getCSV` (utilisée par le shortcode `table.html` du thème)
    a été supprimée → le build local échoue avec
    `function "getCSV" not defined`. Le thème est conçu pour Hugo 0.124.1.
  - **Télécharge** `hugo_extended_0.124.1_windows-amd64.zip` depuis
    https://github.com/gohugoio/hugo/releases/tag/v0.124.1
  - Tu n'as pas besoin de désinstaller ton Hugo actuel : extrais `hugo.exe` dans
    un dossier dédié (ex. `D:\Codes\hugo\`) et lance-le par son chemin :
    ```powershell
    D:\Codes\hugo\hugo.exe server -D
    ```
  - Vérifie : `D:\Codes\hugo\hugo.exe version` → doit afficher
    `v0.124.1 ... +extended ...`
- **Go** (≥ 1.21) : le thème est un *module Hugo* téléchargé via Go.
  - Windows : `winget install GoLang.Go`
- **Git** (déjà installé puisque le repo existe).

> **Bon à savoir :** les avertissements `WARN deprecated` (languageCode,
> cascade._target…) que tu vois avec une version récente de Hugo n'apparaissent
> PAS en 0.124.1 — ces clés y sont parfaitement valides. Ne les modifie pas,
> sinon tu casses le build du déploiement (qui tourne en 0.124.1).

### Lancer le serveur de prévisualisation

Dans le dossier du site (`D:\Codes\vcaries.github.io`), lance la version
*extended* 0.124.1 par son chemin complet (PowerShell) :

```powershell
D:\Codes\hugo\hugo.exe server -D
```

- Ouvre **http://localhost:1313/** → version française.
- **http://localhost:1313/en/** → version anglaise.
- Le `-D` affiche aussi les brouillons (`draft: true`).
- Le serveur recharge automatiquement à chaque sauvegarde ; arrête-le avec
  `Ctrl+C`.
- Première exécution : Hugo télécharge le thème (module Go), ça peut prendre une
  minute. Si tu es derrière un proxy d'entreprise, exporte
  `GOPROXY=https://proxy.golang.org,direct`.

> 💡 Pour taper juste `hugo` au lieu du chemin complet, tu peux ajouter
> `D:\Codes\hugo\` à ta variable d'environnement `PATH` — mais assure-toi alors
> qu'aucune autre version de Hugo (plus récente) ne soit prioritaire dans le
> `PATH`, sinon l'erreur `getCSV` reviendra.

### Où modifier quoi

| Pour changer… | Fichier(s) |
|---|---|
| Ta bio / rôle / formation / réseaux | `content/fr/authors/admin/_index.md` **et** `content/en/authors/admin/_index.md` |
| La page d'accueil (sections, ordre, textes) | `content/fr/_index.md` **et** `content/en/_index.md` |
| Compétences & services | bloc `markdown` (`id: skills`) dans les deux `_index.md` |
| Le menu de navigation | `config/_default/menus.fr.yaml` et `menus.en.yaml` |
| Réglages globaux / SEO | `config/_default/params.yaml`, `languages.yaml`, `hugo.yaml` |
| Styles / couleurs | `assets/scss/custom.scss` (variable `--vc-accent` pour la couleur d'accent) |

> **Règle d'or du bilingue :** toute page créée en FR doit avoir son équivalent
> EN **avec le même nom de dossier**, et inversement. Sinon le sélecteur de
> langue n'aura rien à pointer.

### Architecture du site (accueil court + pages dédiées)

Le site est organisé en **deux niveaux** pour rester lisible quand il grandit :

- **La page d'accueil** (`content/<langue>/_index.md`) est volontairement **courte** :
  à propos, compétences & services, expérience, une **sélection** des publications
  les plus récentes, et le contact.
- **Les pages dédiées** listent l'intégralité d'une rubrique et sont accessibles
  via le menu : Publications (`/publication/`), Conférences (`/event/`),
  Enseignement (`/teaching/`) — et Projets (`/project/`) une fois publiés.

Concrètement : quand tu ajoutes une publication, elle apparaît **automatiquement**
sur la page `/publication/` et, si elle fait partie des plus récentes, dans la
sélection de l'accueil. Rien d'autre à faire.

Pour changer le nombre d'éléments affichés sur l'accueil, modifie `count:` dans le
bloc `collection` (id `publications`) des deux `_index.md`.

### ⚠️ État actuel : la section Projets est masquée

La section **Projets existe dans les sources mais n'est PAS publiée** sur le site
déployé (le temps que tu finalises tes projets). Concrètement :

- les pages dans `content/fr/project/` et `content/en/project/` sont en
  `draft: true` → **exclues du déploiement**, mais **visibles en local** avec
  `hugo server -D` (parfait pour travailler dessus une par une) ;
- le bloc `portfolio` est **commenté** dans les deux `_index.md` ;
- l'entrée de menu « Projets / Projects » est retirée des deux fichiers de menu.

**Pour publier la section quand tu seras prêt :**

1. Passe `draft: true` → `draft: false` (ou supprime la ligne) dans
   `content/<langue>/project/_index.md` et chaque `project/*/index.md`.
2. **Décommente** le bloc `portfolio` dans `content/fr/_index.md` et
   `content/en/_index.md` (retire le `#` devant chaque ligne du bloc).
3. **Réajoute** l'entrée de menu dans `config/_default/menus.fr.yaml` et
   `menus.en.yaml` (le modèle exact est en commentaire en haut de chaque fichier).
4. Vérifie avec `hugo server` (sans `-D` cette fois) que la section apparaît bien.

### Ajouter / modifier un projet (portfolio)

1. Duplique un dossier projet existant dans **les deux langues**, par ex. :
   ```
   content/fr/project/mon-projet/index.md
   content/en/project/mon-projet/index.md
   ```
2. Mets une image de couverture `featured.png` (idéalement 1200×630) dans chaque
   dossier. (Les couvertures actuelles ont été générées sur mesure ; tu peux les
   remplacer par des captures d'écran de tes vrais projets.)
3. Dans le `index.md`, renseigne `title`, `summary`, `date`, `tags` et les liens
   (`url_code`, `url_pdf`, …). **Les `tags` doivent correspondre aux filtres** du
   bloc `portfolio` (`Scientific Python`, `CFD`, `Data Engineering`,
   `Machine Learning`) pour apparaître sous le bon bouton.
4. Retire la ligne de commentaire `<!-- MODÈLE … -->` une fois personnalisé.

### Ajouter une publication

Le plus simple : duplique un dossier dans `content/fr/publication/` et
`content/en/publication/`, puis ajuste `title`, `authors`, `date`, `doi`,
`publication`, `abstract`, `summary`, `url_pdf`, etc.
*(Alternative : le dépôt contient un workflow qui convertit un fichier
`publications.bib` en pages — mais l'édition manuelle reste la plus simple ici.)*

### Préparer une image de couverture (n'importe quel format)

Le thème **recadre** automatiquement les images des cartes (publications, projets,
conférences) vers un format fixe. Une image trop large, trop haute ou de ratio
inhabituel paraît donc « zoomée » ou mal cadrée.

**Solution :** le script `tools/make_featured.py` normalise **n'importe quelle
image** vers un cadre uniforme **16:9 (1200×675)**, en plaçant l'image *entière*
(sans rognage) sur un **fond flou** généré à partir de l'image. Résultat : aucun
contenu coupé, aucun zoom, et toutes les cartes ont le même format propre.

```powershell
# Installe Pillow une fois : pip install pillow
# Écrase l'image existante :
python tools\make_featured.py content\fr\publication\mon-article\featured.png

# Ou depuis une image source quelconque vers la destination voulue :
python tools\make_featured.py "C:\chemin\ma-photo.jpg" content\fr\event\ma-conf\featured.jpg
```

Règles pratiques :

- Lance-le **dans les deux langues** (`content/fr/...` ET `content/en/...`), ou
  copie le `featured` généré dans les deux dossiers.
- Le format de sortie suit l'extension : `.png` reste PNG, `.jpg` reste JPEG.
- Astuce : si une image précise est mal cadrée, tu peux aussi forcer le centrage
  du recadrage du thème en ajoutant `focal_point: Center` (ou `Top`, `Smart`…)
  dans le bloc `image:` du fichier `index.md`.

---

## 3. Publier sur GitHub

```bash
# 0) (une seule fois) supprime le verrou resté de l'atelier
del .git\index.lock        # Windows CMD
# Remove-Item .git\index.lock   # PowerShell

# 1) vérifie ce qui va être committé
git status

# 2) ajoute tout
git add -A

# 3) committe
git commit -m "Refonte bilingue (FR/EN), section projets, design et SEO"

# 4) pousse
git push origin main
```

Le simple `push` sur la branche `main` **déclenche le déploiement automatique**
(workflow `.github/workflows/publish.yaml`).

---

## 4. Vérifier le déploiement GitHub Pages

1. Va sur le dépôt → onglet **Actions**. Tu verras un workflow
   *« Deploy website to GitHub Pages »* en cours puis ✅ vert (≈ 1–2 min).
2. En cas d'échec, clique dessus pour lire les logs (souvent une erreur YAML ou
   un module Go indisponible — relance le job).
3. Vérifie que **Settings → Pages** indique : *Source = GitHub Actions*.
4. Ouvre **https://vcaries.github.io/** (FR) et **/en/** (EN), fais un
   rafraîchissement forcé (Ctrl+F5) pour ignorer le cache.
5. Contrôle rapide : le sélecteur de langue bascule bien FR ↔ EN sur la même page.

> Astuce : teste **toujours** en local avec `hugo server` avant de pousser. Si ça
> build en local, ça buildera quasi à coup sûr sur GitHub Actions.

---

## 5. Stratégie SEO (concrète et actionnable)

### a) Ce qui est déjà en place

- **Balises title/description par langue** (`config/_default/languages.yaml`).
- **Open Graph + Twitter Card** avec image de partage
  (`static/media/og-cover.png`, injectée par `layouts/partials/head_custom.html`).
- **Sitemap multilingue** généré automatiquement à `…/sitemap.xml`
  (index renvoyant vers `…/fr/sitemap.xml` et `…/en/sitemap.xml`).
- **robots.txt** (`layouts/robots.txt`) qui pointe vers le sitemap.
- **Balises `hreflang`** FR/EN et **URL canoniques** : gérées nativement par le
  thème grâce à la config multilingue.
- **Données structurées `Person` (JSON-LD)** : activées via
  `marketing.seo.site_type: Person` dans `params.yaml`.

### b) Les 3 actions à faire toi-même (priorité haute)

1. **Google Search Console** (le plus important pour « apparaître sur Google ») :
   - Va sur https://search.google.com/search-console, ajoute la propriété
     `https://vcaries.github.io/`.
   - Méthode de validation la plus simple : *balise HTML*. Copie le code fourni
     (`content="xxxxxxxx"`) et colle-le dans `config/_default/params.yaml` :
     ```yaml
     marketing:
       verification:
         google: 'COLLE-ICI-TON-CODE'
     ```
     Pousse, attends le déploiement, puis clique « Valider ».
   - Une fois validé : **Sitemaps → ajouter `sitemap.xml`**. Cela force
     l'indexation. Tu peux aussi « Demander une indexation » de la page d'accueil.
2. **Backlinks de qualité** (Google fait confiance aux sites pointés par d'autres) :
   - Mets `https://vcaries.github.io` dans : ton **profil LinkedIn** (section
     « Coordonnées » + un post), ton **profil GitHub** (champ *Website* + le
     `README` de ton profil), ton **Google Scholar**, ton **ORCID**, ton **HAL**,
     ta **ResearchGate**, et la signature de tes mails.
   - Ces liens sont les plus rentables au début (forte autorité, gratuits).
3. **Cohérence du nom** : utilise systématiquement « Valentin Caries » (même
   graphie partout). Google relie ainsi le site, les publis et les profils à une
   même entité → meilleur classement sur la recherche de ton nom.

### c) Pages prioritaires pour le SEO

1. **La page d'accueil FR** (`/`) — ta page la plus forte ; elle cible ton nom +
   tes mots-clés (Python scientifique, CFD, simulation, data engineering).
2. **La page d'accueil EN** (`/en/`) — pour les recherches internationales.
3. **La page projet phare** (`/project/low-order-aero-solver/`) — contenu riche,
   technique, unique : excellent pour les mots-clés de niche.
4. **Les pages publications** — déjà bien référencées via DOI/HAL ; elles
   apportent de l'autorité thématique.

### d) Bonnes pratiques de contenu

- Garde des **titres et descriptions uniques** par page (50–60 car. pour le
  titre, 150–160 pour la description).
- Écris pour des **mots-clés que les gens tapent** : « ingénieur Python
  scientifique freelance », « consultant CFD », « simulation aérodynamique »…
  intègre-les naturellement dans tes textes (bio, services, projets).
- **Publier régulièrement** aide : un petit blog technique (réactivable via une
  section `post/`) sur tes sujets ferait remonter le site sur des requêtes longue
  traîne. Optionnel mais efficace.
- La vitesse et le mobile sont déjà bons (Hugo + thème). Vérifie avec
  **PageSpeed Insights** après mise en ligne.

---

## 6. Recommandations « portfolio freelance »

- **CV téléchargeable** : place ton CV à jour dans `static/uploads/resume.pdf`
  (le lien « CV » du menu pointe déjà dessus). Idéalement une version FR et une EN
  (`resume.pdf` / `resume-en.pdf`).
- **Appel à l'action clair** : la section Contact dit déjà « Travaillons
  ensemble ». Tu peux ajouter un bouton de prise de rendez-vous (Calendly) dans
  le bloc `contact` (`appointment_url`).
- **Projets concrets** : remplace les 3 modèles par 2–4 projets réels avec
  captures d'écran, résultat chiffré (« ×100 plus rapide », « -30 % de coût
  calcul ») et lien GitHub. C'est ce qui convertit un visiteur en client.
- **Preuve sociale** : si tu obtiens des retours clients/encadrants, ajoute une
  petite section témoignages (bloc `markdown`).
- **Nom de domaine** (optionnel mais pro) : un domaine type
  `valentincaries.com` ou `.dev` renforce la crédibilité freelance. Il se
  branche sur GitHub Pages via un fichier `CNAME` + config DNS (≈ 10 min).
- **Spécialise le message** : « j'aide les équipes R&D à transformer la physique
  en logiciel rapide et fiable » est plus vendeur que « doctorant ». Le site va
  déjà dans ce sens — garde ce positionnement.
- Quand ta thèse sera soutenue, passe le rôle de « Ingénieur de recherche &
  doctorant » à « Docteur-ingénieur » dans les deux `authors/admin/_index.md`.

---

## 7. Aide-mémoire des commandes

```powershell
D:\Codes\hugo\hugo.exe server -D       # prévisualisation locale (http://localhost:1313)
D:\Codes\hugo\hugo.exe --gc --minify   # build de production dans ./public (test)
D:\Codes\hugo\hugo.exe mod get -u      # mettre à jour le thème (module Go)
git add -A; git commit -m "…"; git push   # publier
```

---

## 8. En cas de problème

- **`git` refuse de committer (« index.lock »)** → supprime `.git\index.lock`.
- **Erreur `function "getCSV" not defined`** (au démarrage de `hugo server`) →
  ta version de Hugo est trop récente (≥ 0.143). Utilise **Hugo extended
  0.124.1** (voir §2). Le déploiement GitHub Actions, lui, n'est PAS affecté.
- **`WARN deprecated: languageCode / cascade._target …`** → simples
  avertissements d'une version de Hugo récente ; ils disparaissent en 0.124.1.
  Ne modifie pas ces clés.
- **Le SCSS ne se compile pas / erreur `resources.ToCSS`** → tu utilises Hugo
  *non*-extended. Réinstalle la version **extended**.
- **Une page n'a pas de bouton de langue** → il manque sa traduction (même nom de
  dossier dans l'autre langue).
- **Le build GitHub Actions échoue sur le module** → relance le job (« Re-run
  jobs ») ; c'est souvent un téléchargement réseau transitoire.
- **Une image de projet ne s'affiche pas** → vérifie qu'il y a bien un
  `featured.png` (ou `.jpg`) dans le dossier de la page.
