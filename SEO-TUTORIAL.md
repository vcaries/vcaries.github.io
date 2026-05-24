# Tutoriel SEO complet — `vcaries.github.io`

Objectif : faire en sorte que ton site sorte facilement sur Google, à la fois
quand quelqu'un **tape ton nom** et quand quelqu'un cherche **tes domaines**
(Python scientifique, CFD, simulation, écoulements diphasiques, data engineering,
machine learning…).

Ce tutoriel est rangé par ordre de **priorité / rapport effort-impact**. Fais les
étapes 1 à 3 en premier : elles représentent 80 % du résultat.

---

## 0. Comment Google fonctionne (en 30 secondes)

Trois étapes successives :

1. **Explorer (crawl)** — le robot Google découvre tes pages (via le sitemap et les liens).
2. **Indexer** — il stocke et comprend chaque page.
3. **Classer (rank)** — quand quelqu'un cherche, il ordonne les pages par pertinence + autorité.

Le SEO consiste à **faciliter** ces trois étapes : un site lisible par les robots
(technique), un contenu clair sur les bons mots-clés (on-page), et de la
crédibilité (liens entrants + cohérence d'identité).

---

## 1. Ce qui est DÉJÀ en place (le socle technique) ✅

Tu n'as rien à refaire ici, c'est configuré :

- **Sitemap XML multilingue** généré automatiquement : `https://vcaries.github.io/sitemap.xml`
  (il référence `…/fr/sitemap.xml` et `…/en/sitemap.xml`).
- **robots.txt** (`layouts/robots.txt`) qui autorise l'exploration et pointe vers le sitemap.
- **Balises `title` et `meta description`** par langue (dans `config/_default/languages.yaml`).
- **Open Graph + Twitter Card** avec image de partage (`static/media/og-cover.png`,
  injectée par `layouts/partials/head_custom.html`) → aperçus riches sur LinkedIn, X, etc.
- **Données structurées `Person` (JSON-LD)** : activées via `marketing.seo.site_type: Person`.
  Google relie ainsi le site à l'entité « Valentin Caries » et à tes profils
  (Scholar, ORCID, GitHub, LinkedIn…) déclarés dans ton profil auteur.
- **`hreflang` FR/EN** et **URL canoniques** : gérés nativement (évite le « duplicate content » entre langues).
- **Mobile + vitesse** : Hugo génère un site statique rapide (minifié) — un gros atout SEO.
- **Favicon / logo** : `assets/media/icon.png`.

> En clair : le terrain est prêt. Il reste surtout des actions **hors-code** (Search Console, liens) et **de contenu**.

---

## 2. ÉTAPE 1 (priorité absolue) — Google Search Console

C'est **l'action n°1** pour « apparaître sur Google ». Sans ça, Google finit par
te trouver, mais lentement ; avec ça, tu accélères et tu mesures tout.

### 2.1 Créer la propriété

1. Va sur https://search.google.com/search-console
2. Connecte-toi avec ton compte Google.
3. « Ajouter une propriété » → choisis **Préfixe d'URL** → saisis exactement :
   `https://vcaries.github.io/`

### 2.2 Vérifier la propriété (⚠️ point important pour toi)

Google propose deux méthodes. **Choisis-en UNE** et fais-la correctement :

**Méthode A — Balise HTML (recommandée avec ce thème)**
- Dans Search Console, choisis « Balise HTML ». Google affiche quelque chose comme :
  `<meta name="google-site-verification" content="LA_VALEUR_ICI" />`
- Copie **uniquement** `LA_VALEUR_ICI` (une longue chaîne, ~43 caractères) et colle-la dans
  `config/_default/params.yaml` :
  ```yaml
  marketing:
    verification:
      google: 'LA_VALEUR_ICI'
  ```
- ⚠️ **Attention** : la valeur actuelle dans ton fichier (`googlec913110af28d88a5`)
  ressemble au **jeton de la méthode "fichier HTML"**, pas à la valeur de la balise meta.
  Si tu utilises la méthode Balise HTML, remplace-la par la vraie valeur `content="…"`.

**Méthode B — Fichier HTML**
- Si tu préfères, Google te donne un fichier à télécharger, ex. `googlec913110af28d88a5.html`.
- Place ce fichier dans le dossier **`static/`** du site (ex. `static/googlec913110af28d88a5.html`).
  Hugo le copiera à la racine du site → accessible à `https://vcaries.github.io/googlec913110af28d88a5.html`.
- Dans ce cas, **laisse `marketing.verification.google` VIDE** (sinon tu mélanges les méthodes).

Puis : commit + push, attends le déploiement (1-2 min), et clique **« Valider »** dans Search Console.

### 2.3 Soumettre le sitemap

Une fois la propriété validée :
1. Menu **Sitemaps**.
2. Saisis `sitemap.xml` et clique **Envoyer**.
3. Google explorera tes pages FR et EN automatiquement.

### 2.4 Forcer l'indexation des pages clés

1. En haut, utilise **l'Inspection de l'URL**.
2. Saisis `https://vcaries.github.io/` → « Demander une indexation ».
3. Répète pour : `https://vcaries.github.io/en/` et tes pages de publications les plus importantes.

### 2.5 Bonus : Bing Webmaster Tools

Bing (et donc aussi les IA qui s'appuient dessus) : https://www.bing.com/webmasters
Tu peux **importer directement depuis Search Console** en un clic. Quelques minutes, ça vaut le coup.

**☑ Checklist étape 1 :** propriété créée · vérifiée · sitemap soumis · indexation demandée · Bing fait.

---

## 3. ÉTAPE 2 — Identité & crédibilité (E-E-A-T)

Google classe mieux les entités **cohérentes et reconnues**. Pour une personne, ça veut dire :

- **Toujours le même nom** : « Valentin Caries » à l'identique partout (site, LinkedIn,
  GitHub, Scholar, ORCID, HAL, ResearchGate, IFPEN, signatures de mail).
- **Le site pointe vers tes profils** (déjà fait : tes liens sociaux sont dans le profil
  auteur → ils alimentent le `sameAs` des données structurées).
- **Tes profils pointent vers le site** (voir étape 3 — les backlinks).
- **Une adresse de contact cohérente** : tu as basculé ton email vers `valentin.caries@ifpen.fr`
  dans ton profil ; pense à l'aligner aussi dans le bloc **Contact** de la page d'accueil
  (`content/fr/_index.md` et `content/en/_index.md`, champ `email:`) si tu veux la même partout.

---

## 4. ÉTAPE 3 — Backlinks (le levier le plus rentable au début)

Google fait confiance à un site **pointé par d'autres sites crédibles**. Tu as un
avantage : tes profils académiques ont une forte autorité. Mets ton URL partout :

- [ ] **LinkedIn** : section « Coordonnées » → site web `https://vcaries.github.io` + 1 post d'annonce avec le lien.
- [ ] **GitHub** : champ *Website* de ton profil + un lien dans le `README` de ton profil (`github.com/vcaries`).
- [ ] **Google Scholar** : champ « Page d'accueil ».
- [ ] **ORCID** : section « Websites & social links ».
- [ ] **HAL / IdRef** : lien vers le site sur ta fiche auteur.
- [ ] **ResearchGate** : champ site web.
- [ ] **Page IFPEN / annuaire labo** (si possible) : demander l'ajout du lien.
- [ ] **Co-auteurs / page du LMFA / ECL** : un lien depuis une page institutionnelle a beaucoup de poids.
- [ ] **Signature d'email** : ajoute l'URL.

> Ces liens sont gratuits, rapides, et très efficaces pour un nouveau site. C'est
> ce qui fera que « Valentin Caries » te renverra **toi** en haut des résultats.

---

## 5. ÉTAPE 4 — Optimisation on-page (mots-clés & structure)

### 5.1 Tes mots-clés cibles

Pense « ce que les gens tapent ». Exemples pour toi :

**Français :** ingénieur de recherche CFD · consultant Python scientifique ·
simulation numérique CFD · modélisation d'ordre réduit · écoulements diphasiques ·
pompes multiphasiques · machine learning ingénierie · data engineering scientifique ·
freelance calcul scientifique.

**Anglais :** scientific Python developer · CFD consultant · reduced-order modeling ·
tip-leakage flow · multiphase pump · research engineer aerodynamics · surrogate modeling ·
HPC data pipeline · scientific computing freelance.

Intègre-les **naturellement** dans : ta bio, la section Compétences & Services, les
titres et résumés de tes publications et (plus tard) de tes projets. Pas de bourrage
de mots-clés (Google pénalise) — vise un texte fluide qui contient ces termes.

### 5.2 Titres & descriptions

- **Title** (50-60 caractères) et **description** (150-160) doivent être **uniques** par page
  et donner envie de cliquer. Le thème les génère depuis le titre + le `summary` de chaque page :
  soigne donc le `summary` de chaque publication / page.
- La description du site (par langue) est dans `config/_default/languages.yaml` → garde-la
  riche en mots-clés et lisible.

### 5.3 Structure & accessibilité

- **Un seul H1 par page** (le thème s'en occupe), puis des sous-titres logiques (H2/H3).
- **Texte ALT des images** : décris tes figures (utile pour le SEO image et l'accessibilité).
  Dans Hugo Blox, le champ `image.caption` sert de légende ; pour les images en Markdown,
  utilise `![description précise](image.png)`.
- **Maillage interne** : lie tes pages entre elles (une publi qui renvoie au projet associé,
  etc.). Ça aide Google à comprendre la structure.

---

## 6. ÉTAPE 5 — Contenu qui attire (longue traîne) — optionnel mais puissant

Le meilleur moyen de ressortir sur **tes domaines** (pas seulement ton nom) est de
**publier du contenu utile** régulièrement. Un petit blog technique te ferait remonter
sur des requêtes « longue traîne » (très ciblées, peu concurrentielles) :

- Idées d'articles : « Méthode des panneaux expliquée simplement », « Accélérer un
  post-traitement CFD en Python », « Modèles de substitution pour la conception »,
  « CAPE-OPEN pour les pompes multiphasiques »…
- Techniquement : réactiver une section `post/` (blog) dans le thème. Dis-le-moi et je
  la remets en place, bilingue, proprement.

Même 4-6 articles de qualité peuvent générer un trafic durable et crédibiliser ton profil freelance.

---

## 7. Spécificités bilingues (FR/EN)

- Le `hreflang` est déjà en place : Google sert la bonne langue selon l'utilisateur et
  **ne te pénalise pas** pour contenu dupliqué entre FR et EN.
- Garde les **deux versions à jour** : une page qui n'existe que dans une langue affaiblit le couple.
- Les deux sitemaps (FR et EN) sont soumis via le sitemap racine — rien à faire de plus.

---

## 8. ÉTAPE 6 — Mesurer & itérer

Le SEO se pilote avec des données :

- **Search Console** (gratuit, essentiel) → onglet **Performances** : tu vois les
  *requêtes* qui te trouvent, les *impressions*, les *clics* et ta *position moyenne*.
  Regarde 1×/mois : sur quelles requêtes apparais-tu en position 5-15 ? Renforce ces pages.
- **Couverture / Indexation** : vérifie qu'il n'y a pas de pages en erreur.
- **Google Tag Manager** est déjà installé (`GTM-PXT3GFHN`) : tu peux y brancher
  **Google Analytics 4** pour suivre le trafic. (Si tu veux, je t'explique comment, ou
  on renseigne directement `marketing.analytics.google_analytics` avec ton ID GA4.)
- **PageSpeed Insights** : https://pagespeed.web.dev → teste ton URL, vise le vert
  (Hugo part déjà avec une bonne note).

---

## 9. Checklist & calendrier réaliste

**Jour 1 (≈ 1 h)**
- [ ] Vérifier le bon code de vérification Google (voir 2.2) + push.
- [ ] Search Console : créer + vérifier la propriété.
- [ ] Soumettre `sitemap.xml`.
- [ ] Demander l'indexation de `/` et `/en/`.
- [ ] Bing Webmaster Tools (import depuis Search Console).

**Semaine 1 (≈ 1-2 h)**
- [ ] Ajouter l'URL du site sur LinkedIn, GitHub, Scholar, ORCID, HAL, ResearchGate.
- [ ] Aligner l'email de contact (si souhaité).
- [ ] Relire titres / résumés de chaque publication (mots-clés naturels).

**Chaque mois (≈ 30 min)**
- [ ] Lire le rapport « Performances » de Search Console.
- [ ] Renforcer 1-2 pages proches de la 1re page (position 5-15).
- [ ] (Optionnel) publier 1 article de blog.

---

## 10. Pièges à éviter

- ❌ **Bourrage de mots-clés** (répéter un terme à l'excès) → pénalisé.
- ❌ **Acheter des backlinks** → risque de pénalité ; privilégie des liens naturels/profils.
- ❌ **Contenu dupliqué** non géré → ici c'est OK grâce au `hreflang`.
- ❌ **Mélanger les méthodes de vérification** Google (balise meta ET fichier en même temps).
- ❌ **Tout attendre tout de suite** : voir ci-dessous.

---

## 11. Attentes réalistes (délais)

- **Ton nom** (« Valentin Caries ») : tu devrais ressortir en **quelques jours à 2-3 semaines**
  après indexation + backlinks profils (peu de concurrence sur ton nom).
- **Termes métier** (« consultant CFD », etc.) : **plusieurs mois**, et surtout avec du
  contenu régulier + des backlinks. C'est un travail de fond, mais durable.

Le plus important : **fais l'étape 1 (Search Console) aujourd'hui**, puis les backlinks.
Le reste se construit dans le temps.

---

*Besoin d'aide pour une étape précise (réactiver le blog, brancher GA4, corriger la
vérification Google, rédiger des descriptions optimisées) ? Demande-moi.*
