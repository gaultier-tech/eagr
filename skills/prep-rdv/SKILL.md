---
name: prep-rdv
description: Prépare le prochain rendez-vous commercial à partir de l'email d'un prospect (ou du prochain RDV de l'agenda), en s'adaptant au CRM. Pas de deal → prépa de découverte (R1) personnalisée + clients gagnés similaires (références à citer, douleurs probables). Deal(s) trouvé(s) → synthèse consolidée (phase du pipeline + appels Eagr), analyse du prospect, actu du compte, plan et points clés, conseils tirés du playbook Eagr. Utilise cette skill dès qu'un commercial prépare un RDV, un call ou une démo, même sans dire « prépa RDV ». Commandes : `install RDV` configure ; `prépa RDV [email]` génère (sans email : prochain RDV externe de l'agenda). Gère aussi `install eagr`, le réglage du profil partagé par toutes les skills Eagr (entreprise, offre, ton, CRM).
---

# Prépa RDV

Tu prépares le prochain RDV commercial selon l'état du compte dans le CRM, pour l'entreprise et dans
le ton du profil. **Outils** : Eagr (obligatoire), CRM, recherche web, Google Calendar (optionnel).
Choix en chat ; visuel éventuel en artefact.

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

## MODE 1 · Setup (`install RDV`, ou au premier `prépa RDV`)
⛔ Pas de prépa sans config confirmée : affiche la checklist et **attends la réponse**.

Lis le playbook Eagr (`list_segments_by_team`) pour repérer ses segments et son framework. Fais une
recherche web sur le site de l'entreprise pour **pré-remplir** l'offre et les axes de valeur.

> **Profil Eagr** _(seulement s'il manque)_ : Entreprise _(nom)_ · Offre et valeur _(proposée depuis
> votre site, à valider)_ · 2-3 axes de valeur _(idem)_ · Ton ☑ tu ☐ vous · CRM _(détecté)_
> **Prépa RDV** : Framework ☑ _[détecté dans ton playbook]_ ☐ SPICED ☐ MEDDIC ☐ BANT ·
> Client similaire = ☑ même secteur ☑ taille proche ☐ même produit

Enregistre, puis : « C'est prêt. `prépa RDV` + email, ou juste `prépa RDV` pour ton prochain RDV. »

## MODE 2 · `prépa RDV [email]`
Aussi : « prépare mon RDV avec … », « prépa [société] », « prépare ma démo chez … ».
**Sans email** : prochain RDV de l'agenda avec un participant d'un autre domaine ; annonce-le
(« Je prépare ton RDV de [heure] avec [nom], [société] »). Pas d'agenda → demande l'email.

**Aiguillage** : deals CRM de la société (domaine, puis nom). Aucun → **A**. Un ou plusieurs → **B** (consolidés).

### A · Découverte (pas de deal) · A1-A4 en parallèle
- **A1 Prospect** (web) : poste, ancienneté, parcours, LinkedIn.
- **A2 Société** (web) : business model, orga commerciale, cycle de vente, chiffres.
- **A3 Actus** (web, 6 mois) : recrutements sales, expansion, levées, réorganisations.
- **A4 Clients similaires** (CRM, gagnés) : 2-3 proof points + douleurs et objections probables.
  Secteur vide au CRM → taille, puis produit acheté ; dis quel critère tu as pris.
- **A5 Angles** : 2-3 hypothèses (offre + axes de valeur + douleurs A4) et une question d'ouverture.
- **A6 Questions de découverte** selon le framework, avec relances, impact chiffré, « pourquoi
  maintenant », processus de décision.
- **A7 Conseils pour gagner** : les 2-3 compétences clés du segment découverte du playbook, appliquées
  à ce prospect ; plus ce qui a marché sur les comptes de A4 (3 appels Eagr max). Rien de visible
  dans Eagr → déduis du CRM et dis que c'est plus général.

**Sortie A** : 👤 Prospect · 🏢 Société · 🔥 Actus · 🏆 Clients similaires · 🎯 Angles · 🔍 Questions · 🎓 Conseils.

### B · Deal en cours
- **B1 État du deal** (CRM) : phase, montant, dates, propriétaire ; le deal le plus actif en tête.
- **B2 Échanges** (Eagr) : liste tous les appels, lis les **5 plus utiles** (le dernier + découverte,
  démo, négo) → douleurs citées, engagements, objections traitées ou non, risques. « N trouvés, 5 lus ».
- **B3 Prospect** (web) : levier de décision réel, angle à adapter.
- **B4 Actu du compte** (web, 6 mois).
- **B5 Plan du RDV** : objectif (l'étape à franchir), risques à lever, next steps qui / quoi / quand.
- **B6 Points clés** : checklist priorisée.
- **B7 Conseils pour gagner** : compétences clés du segment qui correspond à l'étape du deal ; la plus
  faible sur ce deal si les appels ont des scores ; plus les comptes similaires, comme A7.

**Sortie B** : 👤 Prospect · 🔥 Actu · 📊 Deal · 🧠 Échanges · 🎯 Plan · 🗣️ Points clés · 🎓 Conseils.

Le texte est la sortie principale. Artefact seulement en bonus et s'il y a des données. Factuel, concis.

**Mise à jour** : `install eagr` → profil ; « change mon framework RDV » → framework et critère similaire.
