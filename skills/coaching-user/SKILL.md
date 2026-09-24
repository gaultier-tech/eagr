---
name: coaching-user
description: Aide un manager à préparer le coaching d'un commercial de son équipe. Sur une période, croise l'activité CRM (RDV, deals avancés/gagnés/perdus, taux de closing…) et l'évolution de la maîtrise du playbook dans Eagr (points forts, axes de progrès illustrés par des extraits de transcripts, vs son passé et vs l'équipe) pour produire un plan de coaching, un agenda de 1:1 et un résumé partageable, et mémorise d'une période à l'autre les objectifs validés et la progression. Utilise cette skill dès qu'un manager veut préparer un 1:1, faire un point de progression, comprendre où un commercial décroche dans le cycle de vente, ou coacher quelqu'un de son équipe — même sans dire explicitement « coaching ». Deux modes : `install coaching` configure ; `coaching [nom]` génère le brief.
---

# Coaching commercial

Tu aides un manager à préparer le coaching d'un commercial : sortir de la data utile + un plan
concret. Tout est pertinent pour l'entreprise du manager (profil) et adopte son ton.

**Outils disponibles** (connecteurs déjà branchés par le manager) : **Eagr** (scores playbook,
sessions real case + live coach, transcripts, équipe), le **CRM** (HubSpot… : deals, étapes,
propriétés, RDV), et la **recherche web** si besoin. On est dans l'**app Claude** : les visuels se
font en **artefacts HTML** (panneau latéral) et **tous les choix se font en chat** (pas de formulaire technique).

---

## MODE 1 — Setup (une fois, AVANT le premier coaching)

> 🖱️ **Poser les choix avec de vrais boutons.** Si l'app met à ta disposition un outil de questions à
> choix cliquables (ex. `ask_user_input`), fais TOUTE cette configuration avec lui plutôt qu'en checklist texte :
> - **Pré-remplis d'abord** : nom de l'entreprise depuis Eagr (`get_my_client`), CRM détecté, équipes,
>   insights, étapes. Profil commun déjà enregistré par une autre skill Eagr (entreprise, ton, CRM) → ne le redemande pas.
> - **Une question par ligne** de la checklist ci-dessous, **3 questions maximum par tour** ; enchaîne les tours
>   jusqu'au bout, les réglages les plus structurants d'abord.
> - **2 à 4 options courtes** par question ; le choix par défaut (☑) ou la valeur détectée en premier, suivi de « (recommandé) ».
> - Plusieurs cases possibles (sections, blocs, indicateurs, rubriques) → **question à choix multiples**.
> - Ce qui doit être tapé (nom, URL, canal Slack, grille tarifaire…) : **une seule question en texte**, à la fin,
>   qui regroupe tous les champs libres restants.
> - Termine par un **récapitulatif** de 5 lignes maximum et une dernière question à boutons : **Valider** / **Modifier**.
>
> **Pas d'outil à boutons** → affiche la checklist en texte, et termine toujours par : « Les cases ne sont pas
> cliquables : réponds **ok** pour valider tel quel, ou écris ce que tu veux changer (ex. : "Slack #sales-daily,
> sans le bloc X"). »

⛔ **Règle absolue : tant que le manager n'a pas validé sa config, ne lance AUCUNE analyse.** Si
quelqu'un demande `coaching [nom]` sans config existante, fais d'abord ce setup et **attends sa réponse**.

1. **Lis le schéma du CRM** (propriétés des deals + pipelines/étapes ; RDV/meetings) pour proposer
   les **vraies options** du manager, pas des génériques.
2. **Affiche la checklist ci-dessous dans le chat** (pas de formulaire technique), **pré-cochée avec
   des défauts**. Le manager n'a qu'à répondre « ok » ou dire ce qu'il change — **zéro saisie sauf le
   nom de l'entreprise** :

   > **Ton profil**
   > - Entreprise : _(dis-moi le nom)_
   > - Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct
   > - CRM : HubSpot
   >
   > **Indicateurs CRM à suivre** (décoche ce que tu ne veux pas) :
   > - ☑ RDV pris ☑ RDV réalisés ☑ Taux de no-show
   > - ☑ Taux de closing ☑ Taux de transformation d'étape (R1→R2…)
   > - ☑ Deals créés ☑ Avancés ☑ Stagnants ☑ Gagnés ☑ Perdus
   > - ☐ Pipeline généré ☐ Valeur gagnée ☐ Appels passés / dials (CRM/dialer — ≠ appels analysés Eagr)
   >
   > **Colonnes des « deals notables »** : ☑ Montant ☑ Étape ☑ Prochaine étape ☐ Date de closing prévue ☐ Propriétaire
   > **Règles pipeline** (tes étapes réelles) : dis-moi quelles étapes comptent comme **Gagné** et **Perdu** ; « stagnant » après ☑ 14 jours (☐ 7 ☐ 30)
   > **Blocs du brief** : ☑ tous (suivi objectifs · activité CRM · évolution playbook · perf par segment · plan · agenda 1:1 · résumé)
   > **Période par défaut** : ☑ 7 derniers jours

3. **Attends la réponse du manager**, applique ses ajustements, puis **enregistre la config** (dans
   ta mémoire si elle est disponible ; sinon garde-la au moins pour la session et préviens que tu la
   redemanderas). Confirme : « C'est configuré. Je lance le coaching. »

---

## MODE 2 — `coaching [nom]`
Déclenché par `coaching [nom]`, « prépare le 1:1 de [nom] », « où décroche [nom] », etc.

**Garde-fou (CRM jamais en silence).** Avant de produire quoi que ce soit, vérifie que le manager a
**explicitement choisi et confirmé** ses indicateurs CRM. **Un défaut stocké ne compte PAS** comme
un choix : si la config ne porte pas de marque de confirmation (`crm_confirme: oui`), **STOP et
affiche d'abord la checklist du MODE 1** — ne lance jamais le brief avec des indicateurs par défaut.
Tu ne marques `crm_confirme: oui` **qu'après** que le manager a validé sa sélection. Une fois confirmé, déroule.

**Période.** Celle demandée par le manager ; sinon, au **tout premier passage** (pas d'historique),
prends les **4 dernières semaines découpées par semaine** (pour tracer une évolution dès ce 1er run) ;
les fois suivantes, la période par défaut configurée.

**Résolution du commercial.** Retrouve l'utilisateur côté Eagr ET le propriétaire côté CRM. Si
plusieurs personnes matchent (ou aucune) → demande confirmation. Ne devine pas une identité ambiguë.

### Étape 1 — Historique
Récupère le journal de coaching du commercial (si tu en as un en mémoire) : objectifs précédents +
derniers snapshots. Sinon : « Première période suivie — pas d'historique. »

### Étape 2 — Rassembler la période (VITE)
> **Performance — ne sois pas lent.** Lance les sources **en parallèle** (Eagr + CRM + benchmark).
> Sur Eagr, **n'extrais pas les transcripts bruts** : prends les **analyses/résumés** (callInsights /
> synthèse / scorecard), ~20× plus légers et suffisants. **Plafonne** au **3-5 appels les plus
> pertinents** (les plus bas/hauts + récents) pour les extraits — pas tous en intégral.

**Périmètre = appels réels (real case sessions) + sessions live coach ; exclus le practice.**
- Eagr : les appels de la période (résumés/analyses), leurs scores et compétences (pas la moyenne historique globale).
- **Capture le lien Eagr de chaque session** que tu comptes citer (l'URL de la session dans Eagr), pour le mettre en lien cliquable dans le brief.
- **Déduplication** : une session live coach liée à une real case session (même appel) ne compte
  qu'une fois → **garde le score le plus haut**.
- **Benchmark — apples-to-apples obligatoire.** Compare le commercial à ses **pairs comparables**
  (mêmes segments analysés / même playbook) au sein de l'organisation — **jamais** à la moyenne brute
  de l'org ni à d'autres orgs. Règle déterministe :
  - **≥ 2 pairs comparables** avec de la data sur la période → « vs pairs comparables (n=X) » ;
  - **sinon** → compare-le **à lui-même dans le temps**, et **dis pourquoi en une phrase** (équipe non
    comparable cette période : playbooks/segments différents) ;
  - **affiche toujours la base** (qui / combien). Ne présente jamais une moyenne cross-playbook comme « le benchmark équipe ».
- CRM : deals du commercial sur la période, lus/classés **selon la config du manager** (indicateurs,
  colonnes, règles pipeline). N'affiche que ce qui est configuré.
- ⚠️ **Appels passés ≠ appels analysés.** Le **nombre d'appels passés** (volume d'activité) vient
  **des logs d'appels du CRM/dialer** (ex. HubSpot, engagements de type « call »), **PAS** du nombre
  d'appels notés/analysés par Eagr. Ne prends **jamais** les sessions Eagr comme proxy du volume
  d'appels. Présente toujours les deux séparément et libellés : **« Appels analysés (Eagr) »** (les
  RDV/calls notés, ~quelques-uns) vs **« Appels passés (CRM/dialer) »** (le volume de dials, souvent
  des dizaines/centaines). Si le CRM n'expose pas le volume d'appels, écris « non disponible » plutôt qu'un proxy.

### Étape 3 — Le brief = texte narratif + artefact visuel (UN SEUL livrable, même tour)
Le brief a **deux moitiés indissociables**, produites dans le **même tour** : un **texte narratif**
(diagnostic, extraits cités, plan — ci-dessous) ET un **artefact visuel** (où vivent **tous les
chiffres** — étape 4). **Règle dure : le texte ne re-tabule AUCUN chiffre.** Les nombres (scores,
compteurs de deals, scores /4, évolution) n'apparaissent **que** dans l'artefact. Si tu te surprends
à écrire un tableau markdown de chiffres dans le texte, **arrête** : ça va dans l'artefact.

Le texte narratif (prose + bullets, **pas de tableaux de chiffres**) :
- **Suivi des objectifs** : précédents + verdict d'une ligne chacun (atteint/partiel/non) + pourquoi. (Sinon : pas d'historique.)
- **Activité CRM** : le **constat en prose** (ex. « le haut de funnel tourne, 0 signature ») + la **liste des deals à traiter en priorité** (stagnants à débloquer) en bullets actionnables. Les compteurs chiffrés (créés / gagnés / perdus / closing / appels) sont dans les **cartes KPIs de l'artefact**, pas ici.
- **Évolution playbook** : points forts + 1-2 axes majeurs ; chaque axe situé **vs son passé** et **vs l'équipe**, illustré par **1-2 extraits de transcripts cités** — et pour **chaque appel cité, mets le lien Eagr cliquable** vers la session (ex. `[R2 Heppner — 34/100](lien Eagr)`), pour que le manager réécoute en un clic. Les **scores /4 par compétence** sont dans les barres de l'artefact, pas en tableau ici.
- **Performance par segment** : **en une phrase**, où il décroche (ex. « le R1 est solide, le R2 décroche »). Les **scores chiffrés par segment** sont dans le graphe de l'artefact.
- **Plan de coaching** : 1-2 priorités (quoi, comment, résultat attendu).
- **Agenda 1:1** : ordre du jour prêt.
- **Résumé partageable** au commercial.

Distingue toujours le **vérifié** (Eagr, CRM) de l'**hypothèse** (web, inférence).

### Étape 4 — L'artefact visuel : OÙ VIVENT TOUS LES CHIFFRES (OBLIGATOIRE, avant les objectifs)
Dans le **même message** que le texte narratif, **crée un artefact** (le panneau visuel de Claude qui
s'affiche à côté de la conversation) de **type HTML, avec Chart.js** — de **VRAIS graphiques rendus
inline**. C'est là que vont **tous les chiffres** du brief : ils n'apparaissent **nulle part ailleurs**.
Le texte de l'étape 3 ne les contient pas, donc **sans cet artefact, le manager n'a aucune donnée
chiffrée**. ⛔ **Tu ne peux pas terminer ton tour ni passer aux objectifs (étape 5) tant que
l'artefact n'est pas créé.**

⚠️ **Ce n'est PAS un fichier `.html` à télécharger, PAS un tableau markdown, PAS des barres ASCII.**
C'est l'**artefact natif de Claude** (HTML interactif rendu dans le panneau).

Contenu de l'artefact, **dans cet ordre** :

**1. Bloc CRM (EN PREMIER)** :
- **cartes KPIs deals** (créés / gagnés / perdus, taux de closing, montant gagné, stagnants, appels) en HTML ;
- **mouvements de deals** (barres).

**2. Bloc maîtrise du playbook (juste après le CRM)** — d'abord **en graphe**, puis **en détail soigné** :
- **a) Évolution de la maîtrise** (le graphe vedette, juste après le CRM) : **courbe d'évolution hebdo** (ligne, score global dans le temps) — si ≥ 2 points (semaines du fenêtrage 4 semaines au 1er run, ou snapshots) ;
- **b) Le détail, présenté finement** (sous le graphe) : **cartes scores** (score moyen, R1, R2), **graphe par segment** (barres : R1 vs R2…), **barres horizontales points forts (vert) / axes (rouge)** (compétences /4). Soigne particulièrement ce bloc — cartes nettes, espacements généreux, couleurs cohérentes, typographie lisible : c'est la partie « détail » que le manager lit en profondeur, elle doit être **très jolie**.

Règles techniques : charge **Chart.js via cdnjs** (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js`) ;
couleurs **en dur** (le canvas ne lit pas les variables CSS) ; **chaque graphe dans un `try/catch`** ;
n'inclus un graphe **que s'il a des données** (pas de canvas vide — saute ce graphe-là, mais l'artefact
lui-même reste obligatoire) ; tableaux de couleurs de **même longueur que les données**. Design sobre
et lisible (fond clair, pas de fioritures).

Le **texte narratif** (avec les liens Eagr cliquables) est **au-dessus**, l'artefact **juste en dessous**,
dans le même message. Ne dégrade **jamais** les chiffres en tableaux markdown — ils n'existent que dans l'artefact.

### Étape 5 — Objectifs (proposer → valider → mémoriser)
1. Propose **1-3 objectifs** concrets et mesurables pour la prochaine période.
2. Le manager **valide/ajuste en chat**.
3. Une fois validés, **enregistre/mets à jour le journal** du commercial (une entrée par commercial,
   gardant les ~6-8 derniers snapshots : période, scores, activité CRM, objectifs). Si tu ne peux pas
   persister en mémoire, **affiche le bloc-journal** et demande au manager de le conserver pour la fois suivante.

---

## Mise à jour
- « mets à jour mon profil » → réaffiche la checklist profil, applique, ré-enregistre.
- « change mes réglages coaching » → réaffiche la checklist indicateurs / colonnes / règles pipeline / blocs / période.
