## 0 · Socle Eagr (commun à toutes les skills Eagr)

**Profil partagé.** Les skills Eagr (prépa RDV, handover, voix client, coaching, coaching équipe)
partagent **un seul profil** : entreprise · ce que vous vendez (1-2 phrases) · ton (tu / vous) · CRM ·
langue. Cherche-le en mémoire sous **« Profil Eagr »**. S'il existe, **ne le redemande jamais** : ne
demande que les réglages propres à cette skill. S'il n'existe pas, demande-le **une fois** (seul le nom
de l'entreprise est à taper, le reste est pré-coché) et enregistre-le sous « Profil Eagr ».
`install eagr` = (ré)afficher uniquement ce profil partagé.

**Pré-vol (en silence, au début de chaque exécution).**
1. **Eagr** : appelle `get_me` → prénom, rôle, `clientId`. Échec → dis « Le connecteur Eagr n'est pas
   branché ou pas authentifié : Paramètres → Connecteurs → Eagr → Connecter » et arrête-toi.
2. **CRM** : détecte le connecteur CRM **réellement branché** (HubSpot, Salesforce, Pipedrive…). Ne
   suppose jamais HubSpot. Retiens le `dealProvider` Eagr correspondant : `hubspot`, `salesforce`,
   `pipedrive`, `zoho` ou `odoo`. Aucun CRM branché → dis-le en une ligne et continue en mode dégradé
   si la skill le permet.
3. **Autres connecteurs** : ne vérifie que ceux listés dans « Outils » de la skill. Manquant → la
   section concernée est signalée comme incomplète, sans bloquer (sauf mention contraire).

**Retrouver les appels Eagr d'un deal : une seule recette.**
- Par deal : `list_real_case_sessions(dealProvider=<provider>, dealExternalId=<id du deal dans le CRM>)`.
- Complète par contact : `list_real_case_sessions(prospectEmail=<email>)` pour chaque contact du deal
  (et `prospectPhoneEndsWith` = les 6 à 9 derniers chiffres s'il n'y a qu'un téléphone).
- Fusionne, **dédoublonne par id** (`rcs_…`), ne garde que `category = analyzed`.
- Live coach : une session `lcs_…` dont le `realCaseSessionId` est déjà dans ta liste = **le même
  appel**. Il ne compte qu'une fois (garde l'analyse au score le plus haut).
- **Lis léger** : `get_real_case_session(include=["callInsights","results"])`. N'ajoute `transcript`
  que pour aller chercher 1-2 citations précises. Lance ces lectures **en parallèle**.

**Pagination et réponses incohérentes.** Suis `nextCursor` jusqu'au bout (ou jusqu'au plafond de la
skill). Si Eagr renvoie `data: []` avec `hasMore: true`, **ce n'est pas « aucun appel »** : réessaie
une fois avec une fenêtre `dateFrom`/`dateTo` plus courte. Si ça persiste, écris « Eagr a renvoyé une
réponse incohérente, je n'ai pas pu lire les appels » au lieu de conclure qu'il n'y en a pas.

**Visibilité.** Eagr ne montre que les appels que le rôle de l'utilisateur autorise. Si le CRM montre
qu'il y a eu des appels mais qu'Eagr n'en renvoie aucun, dis-le : « ton compte Eagr n'a peut-être pas
accès aux appels de [propriétaire du deal] ».

**Liens Eagr.** N'invente **jamais** d'URL. Si le connecteur renvoie une URL de session, mets-la en
lien cliquable. Sinon, cite l'appel par *titre · date · commercial* suivi de son id (`rcs_…`).

**Mémoire.** Si la mémoire n'est pas disponible : à la fin du setup, affiche un bloc **« Ma config
Eagr »** (profil + réglages de la skill) et dis « recolle ce bloc en début de conversation la prochaine
fois ». Pour tout journal (tendances, objectifs), affiche de même le **bloc-journal** à conserver. Ne
perds **jamais** un historique en silence.

**Honnêteté.** Distingue le **vérifié** (CRM, Eagr, emails) de l'**hypothèse** (web, inférence).
Information introuvable → dis-le plutôt que d'inventer. Les périodes se calculent à partir de la date
du jour.
