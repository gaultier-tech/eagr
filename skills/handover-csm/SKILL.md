---
name: handover-csm
description: Passation d'un compte signé du commercial au CSM. Côté COMMERCIAL : à la signature, génère la fiche de passation à partir du deal gagné (CRM), des appels Eagr et de SES emails avec le client (parties prenantes et comment les aborder, ce qui a été vendu, objectifs et critères de succès, promesses faites, red flags, plan d'onboarding, to-do du CSM), lui fait compléter les zones d'ombre, puis l'envoie au CSM après accord. Côté CSM : `kickoff [client]` retrouve la fiche reçue et prépare le kickoff. Utilise cette skill dès qu'un deal est signé et passe au Customer Success, qu'un commercial briefe un CSM, ou qu'un CSM prépare le kickoff d'un compte transmis, même sans dire « handover ». Commandes : `install handover` ; `handover [email ou société]` ; `kickoff [client]`.
---

# Passation commercial → CSM

Le CSM n'a pas accès aux emails du commercial : **c'est le commercial qui lance `handover` et envoie
la fiche.** La fiche est écrite **pour le CSM** (« tu reprends ce compte »).
**Outils** : CRM (obligatoire), Eagr, Gmail (boîte du commercial, et envoi), web, Slack (optionnel).

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

## MODE 1 · Setup (`install handover`, ou au premier `handover`)
⛔ Pas de fiche sans config confirmée : affiche la checklist et **attends la réponse**.
Repère dans le CRM la propriété qui porte le **CSM assigné** (deal ou société).

> **Passation** : CSM du compte ☑ _[propriété CRM détectée]_ ☐ je te le dirai ·
> Envoi ☑ brouillon Gmail ☐ envoi Gmail direct ☐ message Slack ·
> ☑ Déposer aussi la fiche en note sur la société dans le CRM
> **Sections** : ☑ Parties prenantes ☑ Vendu ☑ Objectifs ☑ Promesses ☑ Red flags ☑ Onboarding ☑ To-do CSM

Enregistre, puis : « C'est prêt. À la signature : `handover` + l'email d'un contact du client. »

## MODE 2 · `handover [email ou société]` (commercial)
Aussi : « deal signé avec … », « passe [client] au CS », « brief le CSM sur … ».

**1 · Deal** : deal(s) gagné(s) de la société (plusieurs → consolidés). Pas encore gagné → demande
s'il faut continuer.

**2 · Matière, en parallèle** : CRM (offre, montant, conditions, dates, contacts, CSM) · Eagr (5
appels les plus utiles) · Gmail (5 fils les plus récents ou décisifs avec le domaine du client :
promesses écrites, ton, questions ouvertes, qui ne répond plus ; absent → dis que les promesses ne
viennent que des appels) · web (une recherche d'actu).

**3 · Fiche** (sections configurées). Chaque fait porte sa source (CRM, appel du [date], email du
[date]) ; les inférences sont marquées `[à valider au kickoff]`.
- **👥 Parties prenantes** : pour chacun, rôle et influence · sentiment (appels + emails) · style de
  communication et canal préféré `[à valider au kickoff]` · ce qu'il a à gagner ou à perdre · ➡️ comment
  l'embarquer. **Strictement professionnel** (pas de jugement de personnalité, rien de privé) : la
  fiche part par écrit. Termine par qui appeler en premier.
- **📦 Vendu** : offre, périmètre, montant, conditions, durée, signature.
- **🎯 Objectifs et critères de succès** : pourquoi ils ont acheté, métriques à faire atteindre. Cités.
- **🤝 Promesses** : tout ce qui a été promis, avec la source. C'est ce que le CSM devra tenir.
- **🚩 Red flags** : objections non résolues, délais serrés, décideur absent, sur-promesses, silences.
- **🚀 Onboarding** : premières actions, quick wins, jalons, rythme.
- **✅ To-do du CSM** : `[ ]` action · avec qui · pourquoi, groupées Avant le kickoff / Semaine 1 /
  30 jours. Chaque red flag majeur et promesse à risque y figure.

**4 · Un seul message au commercial**, sous la fiche :
- **À compléter** (5 questions courtes max, sur ce que la data ne dit pas : engagements oraux, qui
  a porté le choix, sujet sensible, échéance client, interlocuteur à ménager). « passe » accepté.
- **Envoi prévu** : destinataire (CSM du CRM, sinon « à qui ? »), canal, objet
  **`Passation client · [Société] · fiche de reprise`** (fixe : c'est ce que `kickoff` cherche).
- « Réponds aux questions et dis **ok** : j'intègre et j'envoie. »

**5 · Après « ok »** : intègre les réponses (source : le commercial), crée le brouillon ou envoie
selon la config (donne le lien du brouillon), dépose la note CRM si cochée. Termine l'email par
« Préparé depuis le CRM, les appels Eagr et mes échanges avec le client ; les points [à valider au
kickoff] sont des hypothèses. » Confirme : « Envoyé à [CSM], qui peut lancer `kickoff [société]`. »
**Rien ne part sans ce « ok ».**

## MODE 3 · `kickoff [client]` (CSM)
Aussi : « je reprends [client] », « prépare mon kickoff avec … ».
Cherche la fiche dans le Gmail du CSM (objet `Passation client · [Société]`), puis dans les notes CRM.
- **Trouvée** → résumé en 10 lignes, agenda du kickoff (objectifs à valider, questions pour lever les
  `[à valider au kickoff]`, prochaines étapes), to-do « Avant le kickoff » ; complète avec l'état CRM.
- **Absente** → ne reconstruis pas la fiche (la boîte du CSM n'a pas les échanges de la vente) :
  « Demande à [commercial du deal] de lancer `handover [société]`. » Propose en attendant un mini-brief
  CRM + web étiqueté partiel.

**Mise à jour** : `install eagr` → profil ; « change mes réglages handover » → checklist du MODE 1.
