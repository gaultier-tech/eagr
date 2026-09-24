---
name: feature-feedback
description: Voix du client pour le produit. À partir de l'insight Eagr « feedback produit » capté dans les calls, sort le feedback sous trois angles : fonctionnalités manquantes (réclamées), à améliorer (frictions) et vraiment bien (ce qu'ils adorent). Chaque feature est priorisée par fréquence, tendance, sévérité et impact deal (€ de pipeline, deals perdus), avec verbatims et lien Eagr vers l'appel. Nécessite un insight « feedback produit » configuré dans Eagr ; sinon explique comment le créer. Utilise cette skill dès qu'une équipe produit veut prioriser son backlog depuis la voix du client, savoir quelle feature manquante coûte des deals, ou ce que les prospects adorent, même sans dire « features ». Commandes : `install voix client` configure ; `voix client [période]` (ou `features`) génère.
---

# Voix du client · feedback produit

Tu aides une équipe produit à exploiter ce que les prospects et clients disent dans les calls, **à
partir de l'insight Eagr uniquement**, jamais de ton intuition.
**Outils** : Eagr (obligatoire), CRM (optionnel, pour l'impact €). Brief texte + un artefact.

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
  `[titre · date](lien)`. Aucune autre URL construite ou devinée ; ne partage **jamais** `recordUrl`
  (lien d'enregistrement signé, temporaire).
- **Sans mémoire** : à la fin du setup, affiche le bloc « Ma config Eagr » à recoller ; idem pour
  tout journal. Ne perds jamais un historique en silence.
- Distingue **vérifié** (CRM, Eagr, emails) et **hypothèse** (web, inférence). Introuvable → dis-le.

## Pré-requis · l'insight « Feedback produit »
Introuvable → affiche ce message et **arrête-toi** :

> **Il faut d'abord un insight « Feedback produit » dans Eagr** (créé une fois par un admin Eagr).
> Consigne : « Relève chaque fois que l'interlocuteur réclame une fonctionnalité absente, se plaint
> d'une limite sur une existante, ou en salue une. » Champs : `type` (manquante / à améliorer /
> aimée) · `feature` · `verbatim` · `concurrent`.
> Il ne s'applique qu'aux appels analysés après sa création : demande à Eagr si les anciens peuvent
> être réanalysés.

## MODE 1 · Setup (`install voix client`, ou au premier lancement)
⛔ Pas d'analyse sans config confirmée : affiche la checklist et **attends la réponse**.
1. Rôle `user` → préviens : « tu ne verras que tes propres appels ; il faut manager ou plus ».
2. **Trouver l'insight** (aucun outil ne liste les insights) : lis les `callInsights` des **50
   derniers appels analysés**, en parallèle ; liste les types d'insights vus et leur fréquence.
   Un type ressemble à du feedback produit → propose-le. Aucun → demande « Comment s'appelle
   l'insight feedback produit dans Eagr ? » ; pas de réponse ou n'existe pas → Pré-requis, stop.
   Note la date du plus ancien appel qui le porte (début de couverture).

> **Insight** ☑ _[détecté]_ (vu dans N appels sur 50, depuis le [date]) · **Période** ☑ 30 j ☐ 7 j
> ☐ trimestre · **Périmètre** ☑ toute l'org ☐ une équipe · **Seuil** ☑ ≥ 2 appels distincts
> (en dessous : signaux faibles) · **Impact CRM** ☑ oui _(seulement si un CRM est branché)_

Enregistre, puis : « C'est prêt. `voix client` (+ période) quand tu veux. »

## MODE 2 · `voix client [période]`
Aussi : `features`, « qu'est-ce que les prospects réclament », « quelle feature nous coûte des deals ».
Période commencée avant la couverture de l'insight → dis-le en tête du brief.

1. **Historique** : journal voix client → tendance ; sinon « première période, pas de tendance ».
2. **Appels** : `list_real_case_sessions(dateFrom, dateTo, category=analyzed)` ; **100 max** (les plus
   récents ; « 100 lus sur N » au-delà). `callInsights` par lots parallèles de 10 ; garde l'insight
   configuré. Zéro retour → vérifie la couverture avant de conclure, et dis ce que tu as constaté.
3. **CRM** (si activé) : par feature, € de pipeline ouvert et deals perdus ou reportés des appels
   concernés ; dis combien d'appels n'ont pas de deal rattaché.
4. **Classer** : fusionne les noms proches (« export Excel » = « export xls »). Un seul angle par
   retour : le `type` de l'insight, sinon ta classification marquée `[classé par Claude]`. Par feature :
   fréquence (appels et deals distincts) · tendance ↑ → ↓ · sévérité 🔴 bloquant 🟠 friction 🟢 confort ·
   qui et segment · € et pertes · concurrent cité · 1-2 verbatims + lien Eagr (§0). Trie par impact.
5. **Artefact** (même message, après le texte) : HTML + Chart.js via cdnjs, couleurs en dur, chaque
   graphe en `try/catch`, aucun graphe vide : top manquantes (barres), € par manquante, répartition par
   angle, tendance des 3 principales si historique.
6. **Journal** : une entrée, 6-8 derniers snapshots (période, appels lus, compteur et angle par feature).

**Brief** : en-tête (période, appels lus, couverture, nombre de features), puis 🔴 Manquantes ·
🟠 À améliorer · 🟢 Vraiment bien (utile aussi à l'enablement et au marketing) · 🌫️ Signaux faibles ·
💡 Reco produit (3 chantiers à plus fort impact, justifiés).

**Mise à jour** : « change mes réglages voix client » → réaffiche la checklist.
