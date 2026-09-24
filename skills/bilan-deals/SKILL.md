---
name: bilan-deals
description: Pourquoi on gagne, pourquoi on perd. Sur une période, reprend les deals signés, perdus et sans décision dans le CRM, lit les appels Eagr de chaque deal (insights, scores du playbook, extraits) et sort les vraies raisons de victoire et de défaite, entendues dans les calls et pas seulement saisies dans le CRM. Croise le résultat avec l'exécution du playbook (quelles techniques font la différence entre deals gagnés et perdus), suit la tendance d'une période à l'autre et propose 3 à 5 actions, chacune reliée à un entraînement Eagr. Utilise cette skill dès qu'un dirigeant commercial, un manager ou un RevOps veut comprendre ses résultats, préparer une revue de pipeline, une QBR ou un point d'équipe, ou savoir ce qui fait perdre des deals — même sans dire « win/loss ». Deux modes : `install bilan` configure ; `bilan [période]` génère.
argument-hint: [période, ex. 7 derniers jours, septembre, T3]
---

# Bilan deals — pourquoi on gagne, pourquoi on perd

Tu aides un **responsable commercial** à comprendre ses résultats à partir de ce qui s'est **réellement
dit** dans les calls, et pas seulement du motif sélectionné dans un menu déroulant du CRM. Ta valeur
ajoutée tient en une idée : **relier le résultat du deal à la façon dont le commercial a déroulé le
playbook**. Tout est pertinent pour l'entreprise de l'utilisateur (profil) et adopte son ton.

**Outils** (connecteurs déjà branchés) : **CRM** (HubSpot, Pipedrive, Salesforce… : deals clos, montants,
étapes, motifs, propriétaires), **Eagr** (appels réels du deal : `callInsights`, scores par compétence et
technique, extraits de transcript, **lien du call**), **Slack** (optionnel, pour diffuser). App Claude :
brief **dans la conversation** + **artefact graphique** (pas de fichier).

> **Recette Eagr.** Appels d'un deal : `list_real_case_sessions` avec `dealProvider` + `dealExternalId`
> (l'id du deal dans le CRM) ; à défaut, `prospectEmail` pour chaque contact du deal. Détail d'un appel :
> `get_real_case_session` avec `include: ["callInsights", "results", "contactInfo"]`. Ne demande le
> `transcript` que pour aller chercher une citation précise.

---

## MODE 1 — Setup (une fois)

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
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun bilan : affiche la checklist et **attends la réponse**.

Avant d'afficher la checklist, **lis les `callInsights` d'une dizaine d'appels récents** pour repérer les
insights que ce client a configurés dans Eagr (ils sont libres, chaque client a les siens), et **propose un
mapping**. Puis affiche **dans le chat** (pré-coché ; seul le nom d'entreprise est à taper) :

> **Profil** — Entreprise : _(nom)_ · Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct · CRM : _(détecté)_
> **Deals pris en compte** : ☑ tous les pipelines ☐ un pipeline précis : _(lequel)_ ☐ un segment / une équipe
> **Étapes** : _(je te propose les étapes détectées)_ → lesquelles valent **Gagné**, **Perdu**, et à partir de quand un deal est **sans décision** (☑ date de closing dépassée de 30 j sans mouvement)
> **Insights Eagr utilisés** (détectés) : objections → _(insight)_ · concurrents → _(insight)_ · raisons d'achat / déclencheurs → _(insight)_ · prochaines étapes → _(insight)_ — ☐ aucun, lis les extraits de transcript
> **Période par défaut** : ☑ 7 derniers jours ☐ 30 jours ☐ trimestre en cours
> **Seuil de tendance** : ☑ un thème compte s'il apparaît dans **≥ 3 deals distincts** (en dessous : « signaux faibles »)
> **Croiser avec le playbook** : ☑ oui (techniques gagnants vs perdants)
> **Diffusion** : ☑ dans le chat ☐ Slack, canal : _(nom)_ — ☐ masquer les noms des commerciaux dans la version diffusée
> **Planification** (optionnel) : ☐ chaque lundi 8h30 (heure de Paris)

Applique les ajustements, **marque la config confirmée**, enregistre-la (mémoire si disponible ; sinon
garde-la pour la session et préviens que tu la redemanderas), puis : « C'est prêt. Tape `bilan` (+ période) quand tu veux. »

**Planification demandée** → crée une tâche planifiée qui lance `bilan` à la cadence choisie. Les crons
sont en **UTC** : 8h30 à Paris = `30 6 * * 1` en été (CEST), `30 7 * * 1` en hiver (CET). Dis-le à
l'utilisateur et propose de régler le décalage au changement d'heure.

---

## MODE 2 — `bilan [période]`
Déclenché par `bilan`, « pourquoi on a perdu ces deals », « win/loss », « revue des deals clos », « qu'est-ce qui nous fait gagner ».

**Garde-fou.** Config non confirmée → MODE 1. Période : celle demandée, sinon la période par défaut.

### Étape 1 — Historique
Charge le **journal bilan** (mémoire) : les thèmes et taux des périodes précédentes, pour dire ce qui
**monte**, **baisse** ou **apparaît**. Sinon : « Premier bilan — pas encore de tendance. »

### Étape 2 — Les deals de la période (CRM)
Récupère les deals passés en **Gagné** ou **Perdu** sur la période, plus les **sans décision** (selon la
règle du setup). Pour chacun : nom, société, montant, propriétaire, date de création et de clôture
(→ **durée du cycle**), **dernière étape atteinte avant la perte**, motif saisi dans le CRM, concurrent
renseigné.

**Aucun deal clos** → réponds en une ligne (« Aucun deal clos sur la période ») + le pipeline en cours à
surveiller, et arrête-toi. Pas de remplissage.

### Étape 3 — Les appels de chaque deal (VITE)
> **Perf** : deals traités **en parallèle** ; par deal, **plafonne à 5 appels** (le premier, le dernier, et
> les plus longs) ; lis les **insights et scores**, pas les transcripts entiers. Garde le **lien du call** de
> chaque appel que tu cites.

Deal **sans aucun appel dans Eagr** → compte-le à part (« non couvert ») : il entre dans les chiffres CRM,
pas dans l'analyse des raisons. Affiche le **taux de couverture** (deals avec appels / deals clos).

### Étape 4 — Analyse
1. **Raison entendue, par deal.** En 1-2 phrases : pourquoi il a signé, ou pourquoi pas, **d'après les
   appels**, avec **une citation exacte + lien du call**. Pas de citation qui l'appuie → écris « non
   établi », ne comble pas.
2. **Écart CRM / terrain.** Signale chaque deal où le motif CRM ne colle pas à ce qu'on entend (ex. CRM
   « Prix », appels : « personne côté client n'a porté le projet en interne »). C'est souvent le constat le
   plus utile du bilan.
3. **Thèmes.** Regroupe les raisons en thèmes et compte les **deals distincts** (pas les mentions). Au seuil
   ou au-dessus : **thème**. En dessous : **signal faible**. Pour chaque thème : nb de deals, **€ concernés**,
   tendance vs journal (↑ → ↓ 🆕), 1 citation représentative.
4. **Playbook : ce qui sépare les gagnés des perdus.** Pour chaque technique ou compétence du playbook,
   compare le **taux d'exécution** (ou le score moyen) entre deals gagnés et perdus. Garde les **3 écarts les
   plus forts**, en affichant toujours **n** de chaque côté. Moins de 5 deals dans un groupe → étiquette
   « indicatif ». Rappelle que c'est une **corrélation**, pas une preuve de cause.
5. **Où ça casse.** Répartition des pertes par dernière étape atteinte : on perd surtout en découverte, après
   la démo, en négociation ?
6. **Concurrents.** Deals perdus ou gagnés face à chaque concurrent cité (CRM + insight), et ce qui a fait la décision.

### Étape 5 — Actions (3 à 5)
Chaque action tient en **trois lignes** : **le constat** (chiffré, n inclus) → **la preuve** (deals + citation
+ lien) → **le geste** concret pour la semaine qui vient (message, question de découverte, étape de
qualification, déroulé de démo, positionnement prix…).
Quand l'action porte sur une compétence : cherche un **entraînement Eagr existant** qui la travaille
(`list_practices`) et propose de l'affecter aux commerciaux concernés ; s'il n'y en a pas, propose d'en créer
un à partir des vraies objections entendues. ⛔ **Ne crée ni n'affecte rien sans accord explicite.**

### Étape 6 — Artefact (dans la conversation, après le texte)
Artefact **HTML + Chart.js** (via cdnjs), rendu inline — pas de fichier, pas de tableau ASCII :
- cartes : deals clos · gagnés · perdus · sans décision · taux de signature · € signés · cycle moyen · couverture Eagr ;
- thèmes de perte et de gain (barres horizontales, en nb de deals) ;
- **playbook gagnés vs perdus** (barres groupées sur les 3-5 techniques les plus discriminantes, n affiché) ;
- pertes par étape (barres) ;
- si journal : taux de signature et top thème dans le temps (ligne).
Couleurs en dur, chaque graphe dans un `try/catch`, pas de graphe sans données.

### Étape 7 — Diffusion (si activée)
Version courte pour Slack : chiffres clés, top 3 thèmes gagnés / perdus, actions. Noms des commerciaux
masqués si l'option est cochée. **Premier envoi** : montre l'aperçu et attends l'accord. En planifié, poste
directement dans le canal configuré.

### Étape 8 — Mémoriser
Mets à jour le **journal bilan** (une entrée, ~8 derniers snapshots) : période, nb deals, taux de
signature, thèmes avec compteurs, 3 écarts playbook, actions proposées. Au bilan suivant, commence par un
**suivi des actions** : le thème visé a-t-il reculé ?

## Format de sortie (texte, sortie principale)
En-tête : période · deals clos (gagnés / perdus / sans décision) · taux de signature · couverture Eagr.
- 📌 **Ce qu'il faut retenir** — 3 phrases maximum.
- ✅ **Pourquoi on a signé** — un bloc par deal gagné (société, montant, commercial, raison + citation + lien du call).
- ❌ **Pourquoi on a perdu** — un bloc par deal perdu ou sans décision, même format, **écart CRM / terrain** signalé.
- 🧭 **Thèmes** — gains puis pertes, triés par nb de deals, tendance, signaux faibles à part.
- 🎓 **Ce que le playbook révèle** — les 3 écarts gagnés / perdus, n affiché.
- 🛠️ **Actions de la semaine** — 3 à 5, avec l'entraînement proposé.

Factuel, chiffré, sourcé. Sépare le **vérifié** (CRM, appels) de l'**interprétation**. Une donnée manque → dis-le.

## Mise à jour
- « change mes réglages bilan » → réaffiche la checklist (deals, étapes, insights, période, seuil, diffusion, planification).
- « rafraîchis le mapping des insights » → relis les `callInsights` récents et repropose le mapping.
