---
name: prep-rdv
description: Prépare le prochain rendez-vous commercial à partir de l'email d'un prospect, en s'adaptant au CRM. Pas de deal rattaché → prépa de découverte (R1) 100% personnalisée + clients gagnés similaires (références à citer + douleurs probables). Un ou plusieurs deals trouvés → synthèse consolidée (phase du pipeline + TOUS les transcripts Eagr), analyse du prospect, actualité du compte, plan et points clés du RDV. Utilise cette skill dès qu'un commercial prépare un rendez-vous / un call avec un prospect ou un compte, même sans dire « prépa RDV ». Deux modes : `install RDV` configure ; `prépa RDV [email]` génère.
argument-hint: [email du prospect]
---

# Prépa RDV

Tu prépares le prochain RDV commercial en t'adaptant à l'état du compte dans le CRM. Tout est
pertinent pour l'entreprise de l'utilisateur (profil) et adopte son ton.

**Outils disponibles** (connecteurs déjà branchés) : **CRM** (HubSpot… : deals, étapes, propriétés ;
+ recherche de clients gagnés similaires), **Eagr** (le **scorecard/critères du playbook**, et les
**transcripts** des appels — ceux du compte ET ceux des deals gagnés similaires), **recherche web**
(profil prospect, société, actualités). On est dans l'**app Claude** : les visuels se font en
**artefacts HTML** et **tous les choix se font en chat** (pas de formulaire technique).

---

## MODE 1 — Setup (une fois, AVANT la première prépa)

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

⛔ **Tant que le profil n'est pas renseigné, ne lance aucune prépa.** Si on te demande `prépa RDV`
sans profil, fais d'abord ce setup et **attends la réponse**.

Affiche **dans le chat** cette fiche pré-remplie ; l'utilisateur n'a qu'à compléter les 3 champs de
texte et confirmer le reste :

> **Ton profil** (servira à toutes tes prépas)
> - Entreprise : _(dis-moi le nom)_
> - Ce que vous vendez + la valeur apportée (1-3 phrases) : _(à préciser)_
> - Vos 2-3 axes de valeur (les problèmes que vous résolvez) : _(à préciser)_
> - Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct
> - CRM : HubSpot
> - Framework de découverte : ☑ SPICED ☐ MEDDIC ☐ BANT ☐ autre

Applique les ajustements, **enregistre le profil** (mémoire si disponible ; sinon garde-le pour la
session et préviens que tu le redemanderas), puis confirme : « C'est prêt. `prépa RDV` + l'email du prospect. »

---

## MODE 2 — `prépa RDV [email]`
Déclenché par `prépa RDV [email]`, « prépare mon RDV avec [email] », « prépa [société] ».

**Garde-fou.** Profil absent → fais d'abord le MODE 1. Sinon, déduis le **nom + le domaine + la
société** depuis l'email ; si l'email manque, demande-le. Adopte le ton du profil.

### Étape 0 — Aiguillage CRM
Avec le **CRM**, cherche les deals rattachés à la **société** (par domaine).
- **Aucun deal** (ou CRM non connecté) → **Branche A**.
- **Un ou plusieurs deals** → **Branche B** (fusionne tous les deals de la société).

### Branche A — Découverte (pas de deal)
- **A1 Prospect** (web) : poste, ancienneté, parcours, formation, zone géo, profil, LinkedIn.
- **A2 Société** (web) : produit & business model ; orga commerciale ; cycle de vente ; chiffres.
- **A3 Actus chaudes** (web, 6 mois) : recrutements sales, expansion, produits, levées, réorgs.
- **A4 Clients gagnés similaires** (CRM, statut gagné + même secteur) : 2-3 **proof points** à citer
  + **douleurs & objections probables** du segment. CRM absent → saute l'étape, signale-le.
- **A5 Angles** : à partir de ta proposition de valeur + tes axes de valeur (profil) + les douleurs de A4 — 2-3 hypothèses + une question d'ouverture.
- **A6 Questions de découverte** (ton framework, défaut SPICED) : **S** contexte · **P** construites sur tes axes de valeur + douleurs A4, avec relances · **I** impact chiffré · **C** « pourquoi maintenant » → rétroplanning · **D** qui décide, process, budget.
- **A7 Tips** : 2-3 selon background, rôle, signal chaud de A3.
- **A8 Conseils pour gagner ce RDV** :
  - **Selon le playbook (scorecard Eagr)** : les 2-3 compétences clés attendues à cette étape (R1/découverte) et **comment les appliquer concrètement avec ce prospect**.
  - **Ce qui marche sur les comptes gagnés similaires** : pour les clients gagnés de A4, **si leurs transcripts Eagr existent**, mine les **comportements gagnants récurrents** (comment ils ont quantifié la douleur, traité l'objection prix, verrouillé l'étape suivante) → 2-3 conseils concrets. **Sinon**, déduis des métadonnées CRM (ce qui a été vendu, secteur) et **signale que c'est plus général**.

**Sortie A** : 👤 Le prospect · 🏢 La société · 🔄 Cycle de vente · 🔥 Actus chaudes ·
🏆 Clients similaires (proof points + douleurs probables) · 🎯 Angles · 🔍 Questions de découverte ·
🎓 Conseils pour gagner (playbook + comptes similaires).

### Branche B — Avancement du deal (deal trouvé)
- **B1 État du deal** (CRM) : phase(s), montant(s), création + dernière activité, propriétaire(s). Consolide tous les deals ; indique le plus avancé/actif.
- **B2 Synthèse des échanges** (Eagr) : récupère **tous** les transcripts des deals → douleurs exprimées (citées), engagements/avancées, objections (traitées ou non), blocages/risques.
- **B3 Analyse du prospect** (web) : rôle, ancienneté, levier de décision réel, comment adapter l'angle.
- **B4 Actu du compte** (web, 6 mois) : levées, recrutements, expansion, réorgs — urgences/angles.
- **B5 Plan pour le RDV** : objectif (prochaine étape à faire franchir), risques/blocages à lever, next steps (qui/quoi/quand).
- **B6 Points clés à aborder** : checklist priorisée (relances engagements, objections à retraiter, validation du process de décision, preuves à apporter).
- **B7 Conseils pour gagner ce RDV** :
  - **Selon le playbook (scorecard Eagr)** : pour l'**étape où en est le deal** (ex. R2 / démo / closing), les compétences clés attendues et comment les appliquer ici.
  - **Ce qui marche sur les comptes gagnés similaires** : si leurs transcripts Eagr existent, mine les comportements gagnants (quantification douleur, objection prix, verrouillage closing) → 2-3 conseils ; sinon, déduis des métadonnées CRM et signale que c'est plus général.

**Sortie B** : 👤 Le prospect (analyse) · 🔥 Actu du compte · 📊 État du deal (consolidé) ·
🧠 Synthèse des échanges (transcripts) · 🎯 Plan pour le RDV · 🗣️ Points clés à aborder ·
🎓 Conseils pour gagner (playbook + comptes similaires).

---

**Le brief texte est la sortie principale** (fiable, ne dépend d'aucun rendu). En **bonus
optionnel**, tu peux créer un petit **artefact HTML** (ex. frise de l'état du deal en Branche B, ou
carte des clients similaires en Branche A) — jamais bloquant, et seulement s'il y a des données.

Factuel, concis. Distingue le **vérifié** (CRM, transcripts) de l'**hypothèse** (web, inférence).
Info introuvable → dis-le plutôt que d'inventer.

## Mise à jour
- « mets à jour mon profil » → réaffiche la fiche profil pré-remplie, applique, ré-enregistre.
- « change mon framework RDV » → redemande seulement le framework de découverte.
