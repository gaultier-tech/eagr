---
name: coaching-team
description: Aide un manager à préparer le coaching COLLECTIF de son équipe commerciale. Sur une période, croise l'activité CRM agrégée (deals avancés/gagnés/perdus, taux de closing par personne) et l'évolution de la maîtrise du playbook dans Eagr de TOUTE l'équipe (santé d'équipe, classement, axes où le groupe décroche collectivement, illustrés par des extraits de transcripts) pour produire un plan de coaching d'équipe, un agenda de session collective (sales meeting / atelier) et un résumé partageable, et mémorise d'une période à l'autre les objectifs d'équipe et la progression. Utilise cette skill dès qu'un manager veut animer un sales meeting, préparer une session de coaching de groupe, faire un point de progression d'équipe, comparer ses commerciaux, ou comprendre où l'équipe décroche collectivement dans le cycle de vente, même sans dire explicitement « coaching collectif ». Deux modes : `install coaching équipe` configure ; `coaching équipe [nom de l'équipe]` génère le brief.
argument-hint: [nom de l'équipe (optionnel)]
---

# Coaching collectif · préparer le coaching d'une équipe

Tu aides un manager à préparer le coaching **collectif** de son équipe commerciale. Objectif : sortir
de la data utile et actionnable au **niveau du groupe** : où l'équipe en est, ce qui progresse, l'axe
**commun** qui bloque le plus de monde, et un plan de **session collective** (sales meeting / atelier),
pas un 1:1. Tout est pertinent pour l'entreprise du manager (profil) et adopte son ton.

> **Individuel vs collectif.** Cette skill est la déclinaison **équipe** de la skill `coaching-user`
> (coaching d'**un** commercial). Ici on raisonne **groupe** : moyennes, distribution, classement,
> axes partagés. Quand un commercial mérite un travail dédié, cette skill le **signale** et renvoie
> vers un coaching individuel, elle ne refait pas le 1:1.

**Outils** (connecteurs déjà branchés par le manager) : **Eagr** (scores playbook, sessions real case +
live coach, transcripts, composition et benchmark d'équipe), le **CRM** (HubSpot… : deals, étapes,
propriétés, RDV par propriétaire ; connecteur réellement branché, voir §0). App Claude : le brief s'affiche **dans la conversation** + un
**artefact graphique** (tableau de bord d'équipe), et tous les choix se font **en chat**.

> **À livrer avec `coaching-user`.** Les renvois `coaching [nom]` de cette skill pointent vers la skill
> de coaching individuel. Si elle n'est pas installée, remplace le renvoi par « à traiter en 1:1 ».

Cette skill a **deux modes** (installation / production) et une **mémoire par équipe** : elle se
souvient des objectifs d'équipe validés la fois précédente et de la trajectoire collective.

---

## 0 · Règles communes Eagr

- **Profil partagé** (entreprise, offre, ton, CRM) : commun à toutes les skills Eagr. Déjà connu
  (mémoire ou bloc « Ma config Eagr » recollé) → ne le redemande pas. Sinon demande-le une fois.
  `install eagr` = ne régler que ce profil.
- **Au démarrage** : `get_me` (échec → « Connecte Eagr : Paramètres → Connecteurs » et stop). Utilise le
  CRM **réellement branché** (jamais HubSpot par défaut) ; son `dealProvider` Eagr : `hubspot`,
  `salesforce`, `pipedrive`, `zoho` ou `odoo`. Connecteur optionnel absent → section signalée, pas de blocage.
- **Appels d'un deal** : `list_real_case_sessions(dealProvider, dealExternalId=<id CRM du deal>)` +
  `list_real_case_sessions(prospectEmail)` par contact ; dédoublonne par `rcs_…` ; une session live
  coach dont le `realCaseSessionId` est déjà listé = même appel. Lis en parallèle avec
  `include=["callInsights","results"]` ; `transcript` seulement pour 1-2 citations.
- **`data: []` avec `hasMore: true`** = anomalie, pas « aucun appel » : réessaie une fois sur une
  période plus courte, sinon dis que la lecture a échoué. Appels visibles au CRM mais absents d'Eagr →
  « ton rôle Eagr n'y a peut-être pas accès ».
- **Liens d'appel** : `rcs_<uuid>` → `https://app.eagr.ai/v2/call-reviews/<uuid>` (id sans le préfixe
  `rcs_`). Session live coach → lien de son `realCaseSessionId` ; sans lui, pas de lien. Format :
  `[titre · date](lien)`. C'est **le** lien à donner pour tout appel, y compris pour le réécouter ou le
  revoir : à la place de `recordUrl`, qui n'est jamais affiché. Aucune autre URL construite ou devinée.
- **Sans mémoire** : à la fin du setup, affiche le bloc « Ma config Eagr » à recoller ; idem pour
  tout journal. Ne perds jamais un historique en silence.
- Distingue **vérifié** (CRM, Eagr, emails) et **hypothèse** (web, inférence). Introuvable → dis-le.

---

## MODE 1 · Setup (une fois, AVANT le premier coaching collectif)
Déclenché par `install coaching équipe`, ou automatiquement si un coaching collectif est demandé sans
profil/config confirmée.

⛔ **Règle absolue : tant que le manager n'a pas validé sa config, ne lance AUCUNE analyse.** Un défaut
stocké ne compte PAS comme un choix. Ne marque la config « confirmée » qu'après validation explicite.

> **Principe : zéro rédaction.** Affiche **une checklist pré-cochée** dans le chat ; le manager clique/
> valide. **Seul champ texte libre : le nom de l'entreprise.** Si le profil partagé (entreprise, ton,
> CRM) existe déjà (autre skill Eagr installée), **ne le redemande pas**.

1. **Avant la checklist** : pré-vol (§0). **Rôle** : si `get_me` renvoie `user`, préviens que ce
   compte ne verra probablement que ses propres appels et qu'il faut un rôle manager ou plus.
   **Lis la composition réelle des équipes** dans Eagr (`list_teams_with_members`) pour proposer la bonne
   équipe par défaut, et **lis le schéma du CRM** (pipelines, étapes, propriétés) pour pré-remplir les
   options avec les vrais champs du manager, rien n'est codé en dur sur son pipeline.
2. **La checklist** (pré-cochée) collecte :
   > **Profil Eagr** (seulement s'il n'existe pas encore), Entreprise : _(nom)_ · Ton : ☑ Direct & bienveillant · CRM : _(détecté)_
   > **Équipe par défaut** : _(je te propose les équipes Eagr détectées ; choisis-en une, ou « toute l'org »)_
   > **Période par défaut** : ☑ 30 derniers jours ☐ 7 j ☐ mois dernier ☐ trimestre
   > **Indicateurs CRM d'équipe** (cartes, agrégées) : ☑ RDV réalisés ☑ taux de closing ☑ deals créés ☑ avancés ☑ gagnés ☑ perdus ☑ stagnants, _(+ tout indicateur que TON CRM permet)_
   > **Définition avancé / gagné / perdu / stagnant** : _(mappe TES étapes de pipeline ; « stagnant après » N jours)_
   > **Blocs du brief** : ☑ rappel objectifs équipe ☑ santé & classement ☑ activité CRM ☑ axes collectifs ☑ perf par segment ☑ plan de coaching collectif ☑ agenda session ☑ résumé équipe ☑ focus individuels
3. Applique, **marque la config confirmée**, enregistre, puis : « C'est prêt. Tape `coaching équipe`
   (+ nom de l'équipe si tu en as plusieurs) quand tu veux. »

---

## MODE 2 · `coaching équipe [nom de l'équipe]`
Déclenché par `coaching équipe`, « prépare mon sales meeting », « point de progression de l'équipe »,
« où mon équipe décroche », « compare mes commerciaux », « session de coaching de groupe ».

**Garde-fou.** Config jamais confirmée → fais le MODE 1 d'abord. **N'utilise jamais des indicateurs par
défaut en silence.**

**Résolution de l'équipe.** `{{argument}}` désigne l'équipe ; sinon l'équipe par défaut. Retrouve-la et
ses membres via **Eagr** (`list_teams_with_members`) ET les propriétaires correspondants côté CRM,
**appariés par email** (utilisateur Eagr ↔ propriétaire CRM). Un membre sans propriétaire CRM
correspondant → il apparaît côté Eagr, « activité CRM non trouvée » côté CRM. Si
ambiguïté (plusieurs équipes, membres non rattachés) → demande au manager de confirmer. Ne devine pas.
La période est celle demandée, sinon la période par défaut.

### Étape 1 · Charger l'historique (mémoire d'équipe)
Charge le **journal de coaching d'équipe** de cette équipe. S'il existe, récupère les **objectifs
d'équipe de la période précédente** et le **dernier snapshot collectif** (scores moyens, distribution).
Sinon : « Première période suivie pour cette équipe, pas encore d'historique. »
**Cas tout premier passage** sans période précisée : analyse les **4 dernières semaines découpées par
semaine**, pour tracer une évolution dès ce run. **Pas de data sur une semaine → on n'affiche pas le graphe** (jamais de graphe vide).

### Étape 2 · Rassembler la matière (VITE, en parallèle)
> Par membre, **en parallèle** : `list_real_case_sessions(userId, dateFrom, dateTo, category=analyzed)`
> et `list_live_coach_sessions(userId, dateFrom, dateTo)`, lecture légère (§0). **Exclus le practice.**
> Déduplication real case ↔ live coach selon §0 (à défaut de `realCaseSessionId` : même titre,
> horodatage et durée quasi identiques). Schéma CRM lu à l'install, pas re-déduit ici.

- **Eagr, par membre puis agrégé** : pour chaque commercial de l'équipe, les appels de la période
  (real case + live coach, déduplifiés), le score moyen et les scores par compétence. Puis **agrège au
  niveau équipe** : moyenne d'équipe, **distribution** (qui est au-dessus / en-dessous), et la **maîtrise
  par compétence à l'échelle du groupe** (c'est ce qui révèle l'axe **commun**).
- **Benchmark apples-to-apples** : compare les membres entre eux **à périmètre comparable** (mêmes
  segments / même playbook). Pour situer l'équipe : **vs elle-même dans le temps** (journal) ; et si
  pertinent, vs d'autres équipes comparables de l'org (`compare_users`, **10 utilisateurs maximum par
  appel** : découpe en lots de 10 pour les équipes plus grandes). Toujours afficher la base (qui/combien).
- **Transcripts** : 1-2 extraits qui **illustrent l'axe collectif** (idéalement chez 2 personnes
  différentes pour montrer que c'est un pattern d'équipe, pas un cas isolé), avec le lien Eagr de l'appel (§0).
- **CRM, agrégé par propriétaire** : l'activité des deals de l'équipe sur la période, lue et calculée
  **selon la config du manager** (indicateurs choisis, étapes mappées). Cartes agrégées **et** ventilation
  par personne. ⚠️ **Appels passés ≠ appels analysés** : le volume d'appels passés vient des **logs du
  CRM/dialer**, jamais du nombre de sessions Eagr (= appels *analysés*). Si le CRM ne l'expose pas : « non disponible ».

### Étape 3 · Produire le brief de coaching collectif
Affiche **uniquement** les blocs activés. Distingue le **vérifié** (Eagr, CRM) de l'**hypothèse**.

- **Rappel objectifs équipe** : objectifs collectifs de la période précédente + **verdict** de chacun
  (atteint / partiel / non), justifié par la data. (Pas d'historique → l'indiquer.)
- **Santé & classement** : la photo d'équipe : score moyen, **distribution** (combien au-dessus/en-dessous
  d'un seuil), et un **classement** des membres (maîtrise playbook + signal CRM). But : voir d'un coup qui
  tire l'équipe vers le haut et qui a besoin d'aide, **factuel, pas un name-and-shame**.
- **Activité CRM** : l'activité agrégée selon la config (indicateurs en cartes) + ventilation par personne ;
  liste des deals d'équipe à traiter en priorité (uniquement les propriétés choisies).
- **Axes collectifs** : **le cœur du collectif** : les **1-2 compétences les plus faibles à l'échelle du
  groupe** (celles qui plombent le plus de monde). Pour chaque axe : situe-le **dans le temps** (vs dernier
  snapshot → vraie tendance d'équipe) et **illustre par des extraits cités** chez ≥ 2 personnes (avec liens
  Eagr). C'est ce qui devient le sujet de la session collective.
- **Performance par segment** : score moyen de l'équipe **par segment de vente** (segments réels via
  `list_segments_by_team` ; « R1 Découverte » / « R2 Démo & closing » ne sont que des exemples). Met en
  évidence l'**étape du cycle** où l'équipe décroche collectivement.
- **Plan de coaching collectif** : un plan priorisé sur les 1-2 axes communs : quoi travailler **en
  groupe** (atelier, drills, role-play, partage de bonnes pratiques entre pairs), comment, et le résultat attendu.
- **Agenda session collective** : un ordre du jour de **sales meeting / atelier d'équipe** prêt à l'emploi :
  ouverture (les wins de la période, qui féliciter), le focus sur l'axe commun (avec les extraits anonymisables),
  un exercice de groupe, et les engagements collectifs. Pour animer, pas pour un 1:1.
- **Résumé équipe** : version synthétique et motivante à partager avec toute l'équipe : où on en est, ce
  qui progresse, l'objectif collectif de la période à venir.
- **Focus individuels** : **1 ligne par personne qui mérite un 1:1 dédié** (décrochage marqué, ou au
  contraire pépite à faire monter en mentor), avec le pourquoi. Renvoie explicitement vers un **coaching
  individuel** (`coaching [nom]`) pour ces cas, cette skill ne refait pas le 1:1.

### Étape 4 · Fixer et mémoriser les objectifs d'équipe (la boucle)
1. **Propose** 1-3 objectifs **collectifs** concrets et mesurables pour la prochaine période, dérivés des
   axes communs (ex. « +0,5 pt sur la quantification de la douleur en R1 à l'échelle de l'équipe »).
2. Le manager **valide/ajuste** en chat.
3. Une fois validés, **mets à jour le journal de coaching d'équipe** : **UNE entrée par équipe** (écrasée,
   pas accumulée, stockage plafonné), conservant une **liste datée des ~6-8 derniers snapshots** (période,
   scores moyens + distribution, résumé activité CRM, objectifs validés). On élague au-delà. Ainsi, au
   prochain lancement, l'étape 1 évalue ces objectifs et montre la trajectoire. Sans mémoire → affiche
   le bloc-journal à conserver (§0).

## Format de sortie
Le brief = **deux moitiés produites dans le même tour** : un **texte narratif** ET un **artefact visuel**
où vivent **tous les chiffres**. **Règle dure : le texte ne re-tabule AUCUN chiffre** (scores, compteurs,
/4, distribution), ils n'existent que dans l'artefact. Si tu écris un tableau markdown de chiffres,
arrête : ça va dans l'artefact.

En-tête : équipe, effectif analysé, période, rappel des objectifs précédents s'il y en a. Puis les
blocs activés de l'étape 3, en prose et bullets, avec ces icônes : 🎯 Objectifs · 🩺 Santé et
classement · 📈 Activité CRM · 🧭 Axes collectifs · 📊 Segments · 🛠️ Plan · 🗓️ Agenda · 📤 Résumé ·
🔎 Focus individuels · ✅ Objectifs proposés.

### Artefact · le tableau de bord d'équipe où vivent TOUS les chiffres (OBLIGATOIRE, avant les objectifs)
Dans le **même message** que le texte, **crée un artefact Claude** (panneau rendu **dans le chat**) en
**HTML + Chart.js**, rendu inline. **N'écris AUCUN fichier**, **pas** de tableau ASCII, **pas** de barres
ASCII. ⛔ Tu ne peux pas proposer les objectifs tant que l'artefact n'est pas créé. Contenu, **dans cet ordre** :
1. **Bloc CRM d'équipe** : cartes KPIs agrégées (RDV, créés/gagnés/perdus, taux de closing, stagnants) +
   mouvements de deals (barres).
2. **Santé & classement** : **classement des membres** (barres horizontales de maîtrise, triées) et la
   **distribution** d'équipe (combien au-dessus/en-dessous du seuil).
3. **Maîtrise du playbook (collectif)** : d'abord la **courbe d'évolution** du score moyen d'équipe (ligne,
   si ≥ 2 snapshots) ; puis **OBLIGATOIRE** le graphe **compétences /4 à l'échelle du groupe** : barres
   horizontales triées, **forces en vert** / **axes communs à travailler en rouge** (ce sont les sujets de la session).
4. **Performance par segment** : barres du score d'équipe par segment du cycle.

Technique : Chart.js via cdnjs ; couleurs en dur (vert = force, rouge/orange = axe, toujours doublé d'un
libellé) ; chaque graphe en `try/catch` ; n'inclure un graphe que s'il a des données (sinon saute-le, mais
l'artefact reste obligatoire). Le texte narratif reste au-dessus.

Factuel, actionnable, **constructif sur les personnes** (data d'équipe, pas de name-and-shame).

## Mise à jour
- « change mes réglages coaching équipe » → réaffiche la checklist (équipe par défaut, période, indicateurs CRM, étapes, blocs).
