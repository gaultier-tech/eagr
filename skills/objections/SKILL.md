---
name: objections
description: Tableau de bord des objections. Sur une période, rassemble toutes les objections soulevées par les prospects et clients dans les appels Eagr, les classe par thème, mesure leur fréquence, leur tendance et leur impact sur les deals (CRM), et surtout évalue COMMENT l'équipe y répond — score de la compétence de traitement des objections du playbook, meilleure réponse réellement donnée par un commercial (extrait + lien du call), erreurs fréquentes. Produit un tableau de bord visuel et propose des entraînements Eagr sur les objections les plus coûteuses. Utilise cette skill dès qu'un manager, un responsable enablement ou un dirigeant veut savoir quelles objections reviennent, lesquelles font perdre des deals, ou comment son équipe les traite — même sans dire « objections ». Deux modes : `install objections` configure ; `objections [période]` génère.
argument-hint: [période, ex. septembre, 30 derniers jours, T3]
---

# Tableau de bord des objections

Tu aides un **manager** ou un **responsable enablement** à passer de « on entend souvent que c'est trop
cher » à une vision chiffrée : **quelles objections, combien, où dans le cycle, avec quel impact, et
surtout comment l'équipe y répond**. Les meilleures réponses viennent **de l'équipe elle-même** (ce qui a
marché en vrai), pas d'un argumentaire inventé. Tout est pertinent pour l'entreprise de l'utilisateur
(profil) et adopte son ton.

**Outils** (connecteurs déjà branchés) : **Eagr** (appels de la période : insight objections, scores du
playbook dont la compétence de traitement des objections, extraits, **lien du call**), **CRM** (optionnel :
issue et montant des deals concernés), **Notion** / **Slack** (optionnel, pour archiver ou diffuser). App
Claude : synthèse **dans la conversation** + **tableau de bord en artefact**.

> **Recette Eagr.** `list_real_case_sessions` avec `dateFrom` / `dateTo` et `category: "analyzed"` (pagination
> par `nextCursor`), puis `get_real_case_session` avec `include: ["callInsights", "results", "speakers",
> "contactInfo"]`. Transcript seulement pour extraire la réponse du commercial autour d'une objection retenue.

> ⛔ **Pré-requis insight.** Idéalement, le client a configuré dans Eagr un insight qui capture les objections.
> Sans lui : dis-le, recommande de le créer (ex. « Objection : ce que le prospect oppose, en ses mots, et la
> réponse apportée »), et propose en attendant une analyse **plafonnée aux 40 appels les plus récents** par lecture
> des transcripts, signalée comme partielle.

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
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun tableau de bord : affiche la checklist et **attends la réponse**.

Lis les `callInsights` d'une dizaine d'appels récents et les compétences du playbook, puis affiche **dans le chat** :

> **Profil** — Entreprise : _(nom)_ · Ton : ☑ Tutoiement ☐ Vouvoiement
> **Insight objections** : _(je te propose l'insight détecté)_ ☐ aucun
> **Compétence « traitement des objections » du playbook** : _(je te propose celle détectée)_ ☐ aucune
> **Thèmes de départ** : ☑ laisse-les émerger des appels ☐ impose ma liste : _(ex. prix, timing, concurrent, sécurité, adoption, « on a déjà un outil »)_
> **Périmètre** : ☑ toute l'équipe ☐ une équipe / un segment · ☑ prospects ☑ clients
> **Période par défaut** : ☑ mois précédent ☐ 30 derniers jours ☐ trimestre
> **Croiser avec les deals (CRM)** : ☑ oui (issue et € par objection)
> **Charte** : ☑ neutre ☐ couleurs de votre site : _(URL)_
> **Archiver / diffuser** : ☑ dans le chat ☐ page Notion datée : _(base)_ ☐ résumé Slack : _(canal)_

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `objections` (+ période). »

---

## MODE 2 — `objections [période]`
Déclenché par `objections`, « quelles objections reviennent », « sur quoi on bloque », « comment on répond au prix ».

**Garde-fou.** Config non confirmée → MODE 1. Période : celle demandée, sinon celle par défaut.

### Étape 1 — Historique
Charge le **journal objections** (mémoire) pour la tendance par thème. Sinon : « Première période suivie. »

### Étape 2 — Rassembler (VITE)
> **Perf** : appels en parallèle ; insights d'abord ; transcripts seulement pour les **2-3 exemples** retenus par thème.

Garde uniquement ce que disent **les prospects et clients** — jamais les phrases de l'équipe. Pour chaque
objection : citation, rôle de l'interlocuteur, société, **moment du cycle** (découverte, démo, négociation,
client), commercial, deal lié, **lien du call**.

### Étape 3 — Classer et mesurer
Regroupe en thèmes (émergents ou imposés ; renomme selon ce qui ressort vraiment). Par thème :
- **Volume** : nb d'objections · nb d'appels · nb de deals distincts · part du total.
- **Tendance** vs journal (↑ → ↓ 🆕).
- **Moment du cycle** où elle surgit le plus.
- **Impact deal** (si CRM) : € de pipeline ouvert concerné · taux de signature des deals où elle apparaît vs les autres (n affiché).

### Étape 4 — Qualité des réponses (le cœur)
Pour les **5 thèmes principaux** :
- **Score moyen** de la compétence de traitement des objections sur les appels concernés, vs le reste des appels.
- **La meilleure réponse de l'équipe** : l'extrait où un commercial a le mieux traité cette objection (score le plus
  haut, et idéalement deal qui a avancé) — qui, ce qu'il a dit, pourquoi ça marche, [lien du call].
- **L'erreur fréquente** : le réflexe qui revient quand ça se passe mal (justifier trop tôt, céder sur le prix,
  ne pas creuser), illustré par un extrait anonymisé.
- **Réponse recommandée** : construite à partir de la meilleure réponse réelle et de la technique du playbook ;
  marquée « proposition » si aucun bon exemple n'existe dans les appels.

### Étape 5 — Tableau de bord (artefact HTML + Chart.js via cdnjs)
Charte du setup, responsive, rendu inline — pas de fichier :
1. **Bandeau** : période · appels analysés · objections relevées · thème n°1 · score moyen de traitement.
2. **Top 3** : trois cartes (thème, volume, tendance, moment du cycle, meilleure réponse en une phrase).
3. **Volume par thème** : barres horizontales, avec la part et la tendance au survol.
4. **Où elles surgissent** : barres empilées thème × moment du cycle.
5. **Impact** (si CRM) : taux de signature avec / sans chaque objection (n affiché).
6. **Détail par thème** : sections repliables — citations (rôle, société, lien du call), meilleure réponse, erreur fréquente.
7. **Qualité de traitement** : score par thème et par commercial (masquable).
Couleurs en dur, chaque graphe dans un `try/catch`, pas de graphe sans données, sections repliables accessibles au clavier.

### Étape 6 — Recommandations et entraînements
3 recommandations maximum : le thème, le constat chiffré, le geste (message commun, question de découverte à
poser plus tôt, preuve à préparer). Pour les 1-2 objections les plus coûteuses : cherche un entraînement Eagr
existant (`list_practices`) ou propose d'en créer un avec un persona qui oppose exactement ces objections, avec
leurs mots (`create_persona`, `create_practice`). ⛔ **Rien n'est créé ni affecté sans accord explicite.**

### Étape 7 — Archiver, diffuser, mémoriser
Notion / Slack si configuré (premier envoi : aperçu et accord). Mets à jour le **journal objections**
(~8 périodes) : par thème, volume, deals, score moyen de traitement.

## Format de sortie (texte, au-dessus de l'artefact)
En-tête : période · appels · objections · couverture (insight ou lecture partielle).
- 📌 **À retenir** — 3 phrases.
- 🔝 **Les objections qui comptent** — top 5 avec volume, tendance, impact.
- 🗣️ **Comment on y répond** — pour chacune : meilleure réponse réelle + lien du call, erreur fréquente.
- 🛠️ **Recommandations** et entraînements proposés.
Aucune objection sans citation. Aucune réponse « modèle » présentée comme venant de l'équipe si elle n'en vient pas.

## Mise à jour
- « change mes réglages objections » → réaffiche la checklist.
- « exporte en JSON » → liste structurée (thème, citation, rôle, moment, deal, lien, date) pour un outil BI.
