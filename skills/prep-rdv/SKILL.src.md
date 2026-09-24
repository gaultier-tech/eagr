---
name: prep-rdv
description: Prépare le prochain rendez-vous commercial à partir de l'email d'un prospect (ou du prochain RDV de l'agenda), en s'adaptant au CRM. Pas de deal rattaché → prépa de découverte (R1) personnalisée + clients gagnés similaires (références à citer + douleurs probables). Un ou plusieurs deals trouvés → synthèse consolidée (phase du pipeline + appels Eagr du deal), analyse du prospect, actualité du compte, plan et points clés du RDV, conseils tirés du playbook Eagr. Utilise cette skill dès qu'un commercial prépare un rendez-vous, un call ou une démo avec un prospect ou un compte, même sans dire « prépa RDV ». Commandes : `install RDV` configure ; `prépa RDV [email]` génère (sans email : prend le prochain RDV externe de l'agenda).
---

# Prépa RDV

Tu prépares le prochain RDV commercial en t'adaptant à l'état du compte dans le CRM. Tout est
pertinent pour l'entreprise de l'utilisateur (profil) et adopte son ton.

**Outils** : **Eagr** (obligatoire : playbook, appels du compte et des deals gagnés similaires),
**CRM** (deals, étapes, clients gagnés), **recherche web** (prospect, société, actualités),
**Google Calendar** (optionnel : trouver le prochain RDV). On est dans l'**app Claude** : tous les
choix se font **en chat**, les visuels éventuels en **artefact**.

<!-- SOCLE -->

---

## MODE 1 · Setup (une fois, AVANT la première prépa)
Déclenché par `install RDV`, ou automatiquement si `prépa RDV` est demandé sans config.

⛔ Tant que la config n'est pas confirmée, ne lance aucune prépa : affiche la checklist et **attends la réponse**.

1. Pré-vol (§0). Lis le **playbook Eagr** (`list_segments_by_team`) : repère les segments (R1,
   démo, closing…) et le framework qu'ils suivent (SPICED, MEDDIC, BANT, maison).
2. Si le **Profil Eagr** existe, ne redemande que ce qui manque. Sinon, affiche dans le chat :

> **Ton profil Eagr** (partagé avec les autres skills Eagr)
> - Entreprise : _(dis-moi le nom)_
> - Ce que vous vendez + la valeur apportée : _(je te propose une version tirée de votre site : corrige ou valide)_
> - Vos 2-3 axes de valeur : _(idem, pré-rempli depuis le site)_
> - Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct
> - CRM : _(détecté : [nom du connecteur])_
>
> **Réglages prépa RDV**
> - Framework de découverte : ☑ _[celui détecté dans ton playbook Eagr]_ ☐ SPICED ☐ MEDDIC ☐ BANT
> - Critère « client similaire » : ☑ même secteur ☑ taille proche ☐ même produit acheté

Pour pré-remplir l'offre et les axes de valeur, fais **une** recherche web sur le site de l'entreprise :
l'utilisateur n'a qu'à valider.

3. Applique, enregistre (mémoire, ou bloc « Ma config Eagr », §0), puis : « C'est prêt. `prépa RDV`
   + l'email du prospect, ou juste `prépa RDV` pour ton prochain RDV. »

---

## MODE 2 · `prépa RDV [email]`
Déclenché par `prépa RDV [email]`, « prépare mon RDV avec [email] », « prépa [société] », « prépare ma démo chez… ».

**Garde-fou.** Config absente → MODE 1 d'abord.
**Sans email** : si Google Calendar est branché, prends le **prochain RDV avec un participant externe**
(domaine différent de celui de l'utilisateur), annonce-le (« Je prépare ton RDV de [heure] avec
[nom], [société] ») et continue. Sinon, demande l'email.
Déduis **nom + domaine + société** depuis l'email.

### Étape 0 · Aiguillage CRM
Cherche dans le CRM les deals rattachés à la **société** (par domaine, puis par nom si rien).
- **Aucun deal** (ou pas de CRM) → **Branche A**.
- **Un ou plusieurs deals** → **Branche B** (consolide tous les deals de la société).

### Branche A · Découverte (pas de deal)
Lance A1-A4 **en parallèle**.
- **A1 Prospect** (web) : poste, ancienneté, parcours, formation, zone, LinkedIn.
- **A2 Société** (web) : produit et business model, organisation commerciale, cycle de vente, chiffres.
- **A3 Actus chaudes** (web, 6 mois) : recrutements sales, expansion, produits, levées, réorganisations.
- **A4 Clients gagnés similaires** (CRM, statut gagné + critère « similaire » de la config) : 2-3
  **proof points** à citer + **douleurs et objections probables** du segment. Si la propriété secteur
  est vide dans le CRM, rabats-toi sur la taille, puis sur le produit acheté, et dis quel critère tu
  as utilisé. Pas de CRM → étape sautée, signalée.
- **A5 Angles** : proposition de valeur + axes de valeur (profil) + douleurs A4 → 2-3 hypothèses et
  une question d'ouverture.
- **A6 Questions de découverte** selon le framework de la config, construites sur les axes de valeur
  et les douleurs A4, avec relances ; impact chiffré ; « pourquoi maintenant » ; processus de décision.
- **A7 Tips** : 2-3 selon le parcours, le rôle et le signal chaud de A3.
- **A8 Conseils pour gagner ce RDV** :
  - **Selon le playbook Eagr** : les 2-3 compétences clés du segment R1 / découverte et comment les
    appliquer avec ce prospect.
  - **Ce qui marche sur les comptes similaires** : pour les clients de A4, cherche leurs appels (recette
    §0, **3 appels maximum au total**, analyses légères). Mine les comportements gagnants récurrents
    (quantification de la douleur, objection prix, verrouillage de l'étape suivante) → 2-3 conseils.
    Si Eagr ne renvoie rien (souvent : ces deals appartiennent à d'autres commerciaux, §0 Visibilité),
    déduis des métadonnées CRM et **signale que c'est plus général**.

**Sortie A** : 👤 Le prospect · 🏢 La société · 🔄 Cycle de vente · 🔥 Actus chaudes ·
🏆 Clients similaires · 🎯 Angles · 🔍 Questions de découverte · 🎓 Conseils pour gagner.

### Branche B · Avancement du deal (deal trouvé)
- **B1 État du deal** (CRM) : phase(s), montant(s), création, dernière activité, propriétaire(s).
  Consolide ; indique le deal le plus avancé ou actif.
- **B2 Synthèse des échanges** (Eagr, recette §0) : tous les appels du deal sont **listés**, mais seuls
  les **5 plus pertinents** (le plus récent + les appels clés : découverte, démo, négociation) sont lus,
  en analyse légère. Sors-en : douleurs exprimées (citées), engagements et avancées, objections
  (traitées ou non), blocages et risques. Indique « N appels trouvés, 5 lus ».
- **B3 Analyse du prospect** (web) : rôle, ancienneté, levier de décision réel, comment adapter l'angle.
- **B4 Actu du compte** (web, 6 mois) : levées, recrutements, expansion, réorganisations.
- **B5 Plan pour le RDV** : objectif (l'étape suivante à faire franchir), risques à lever, next steps (qui / quoi / quand).
- **B6 Points clés à aborder** : checklist priorisée (engagements à relancer, objections à retraiter,
  processus de décision à valider, preuves à apporter).
- **B7 Conseils pour gagner ce RDV** :
  - **Selon le playbook Eagr** : pour le segment qui correspond à l'étape du deal, les compétences
    clés et comment les appliquer ici. Si les appels lus en B2 ont des scores par compétence, pointe
    la compétence la plus faible sur ce deal.
  - **Ce qui marche sur les comptes gagnés similaires** : comme A8.

**Sortie B** : 👤 Le prospect · 🔥 Actu du compte · 📊 État du deal · 🧠 Synthèse des échanges ·
🎯 Plan pour le RDV · 🗣️ Points clés · 🎓 Conseils pour gagner.

---

**Le brief texte est la sortie principale.** En bonus, et seulement s'il y a des données, un petit
**artefact** (frise de l'état du deal en B, carte des clients similaires en A), jamais bloquant.
Factuel et concis.

## Mise à jour
- « mets à jour mon profil » / `install eagr` → réaffiche le profil partagé.
- « change mon framework RDV » → ne redemande que le framework et le critère « similaire ».
