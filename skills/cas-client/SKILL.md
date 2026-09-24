---
name: cas-client
description: Transforme un client signé en cas client publiable. Reprend le deal gagné dans le CRM et tous les appels Eagr du compte — avant ET après signature (onboarding, points de suivi) — pour reconstituer l'histoire avec les mots du client : situation de départ, déclencheur, alternatives étudiées, moment décisif, mise en place, résultats. Ne publie que ce que le client a réellement dit, liste ce qui manque avec les questions d'interview à poser, et prépare la validation par le client avant toute diffusion. Produit la page du cas client aux couleurs de l'entreprise, un post LinkedIn et un one-pager pour les commerciaux. Utilise cette skill dès qu'un marketeur, un commercial ou un CSM veut écrire un cas client, un témoignage, une référence ou une success story — même sans dire « cas client ». Deux modes : `install cas client` configure ; `cas client [société ou email]` génère.
argument-hint: [société ou email d'un contact du client]
---

# Cas client

Tu écris un **cas client** à partir de ce que le client a **réellement dit** dans ses appels. Deux règles
ne se négocient pas : **aucun chiffre ni aucune citation inventés**, et **rien ne sort sans l'accord du
client**. Tout est pertinent pour l'entreprise de l'utilisateur (profil) et adopte son ton de marque.

**Outils** (connecteurs déjà branchés) : **CRM** (deal gagné, date de signature, contacts et rôles),
**Eagr** (appels du compte : insights, extraits de transcript, **lien du call**), **Gmail** (optionnel :
échanges avec le client, et brouillon de la demande de validation), **recherche web** (présentation du client
et charte graphique de l'entreprise). App Claude : textes **dans la conversation** + page en **artefact**.

> **Recette Eagr.** Appels du deal : `list_real_case_sessions` avec `dealProvider` + `dealExternalId`. Appels
> **après signature** (souvent non rattachés au deal) : `prospectEmail` pour chaque contact du client, avec
> `dateFrom` = date de signature. Détail : `get_real_case_session` avec `include: ["callInsights",
> "transcript", "speakers"]` — ici le transcript est utile : les citations doivent être exactes.

---

## MODE 1 — Setup (une fois)
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun cas client : affiche la checklist et **attends la réponse**.

> **Profil** — Entreprise : _(nom)_ · Ce que vous vendez, en une phrase : _(à préciser)_
> **Ton de marque** : ☑ Sobre et factuel ☐ Chaleureux ☐ Expert · ☑ Vouvoiement dans les textes publiés
> **Charte graphique** : ☑ je la récupère depuis votre site : _(URL)_ ☐ je vous envoie logo et couleurs ☐ neutre
> **Formats** : ☑ Page cas client ☑ Post LinkedIn ☑ One-pager commercial ☐ Slide de référence
> **Anonymisation** : ☐ par défaut (secteur + taille à la place du nom, pas de noms de personnes)
> **Informations jamais publiées** : ☑ montant du deal ☑ conditions commerciales ☑ noms des concurrents évincés
> **Langue** : ☑ français ☐ anglais

Charte depuis le site → consulte la page d'accueil et une page produit ; relève couleurs (hex), typographies,
logo (URL), style des boutons et des cartes. Montre le résultat en quelques lignes et fais-le valider. **La
validation client avant publication n'est pas une option** : ne la propose pas en case à cocher.

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `cas client` + une société ou un email. »

---

## MODE 2 — `cas client [société ou email]`
Déclenché par `cas client [x]`, « écris le témoignage de [x] », « success story [x] », « fais une référence de [x] ».

**Garde-fou.** Config non confirmée → MODE 1.

### Étape 1 — Le deal
Retrouve le deal **gagné** dans le CRM : date de signature, durée du cycle, contacts et rôles (champion,
décideur, utilisateurs). Pas de deal gagné → dis-le et demande confirmation avant d'aller plus loin. Signé il
y a moins de 2 mois → préviens que les résultats risquent d'être minces, et propose soit un cas « pourquoi ils
nous ont choisis », soit d'attendre.

### Étape 2 — Rassembler (en parallèle)
- **Eagr, avant signature** : 5 appels maximum (découverte, démo, dernier appel avant signature).
- **Eagr, après signature** : tous les appels d'onboarding et de suivi — **c'est là que vivent les résultats**.
- **Fiche de reprise** du compte si elle a été faite avec la skill `handover-csm` (objectifs et critères de succès).
- **Gmail** (si branché) : messages du client qui mentionnent un résultat ou un retour spontané.
- **Web** : secteur, taille, activité du client (1 recherche).
Garde le **lien du call** et le **locuteur** (nom, rôle) de chaque extrait.

### Étape 3 — Reconstituer l'histoire
Pour chaque temps du récit, les éléments trouvés **avec leur source** :
- **Avant** — la situation et la douleur, dans leurs mots.
- **Le déclencheur** — pourquoi ils ont cherché maintenant.
- **Les options** — ce qu'ils ont envisagé (sans nommer les concurrents si le setup l'interdit).
- **Le moment décisif** — ce qui a fait basculer, avec le lien du call où ça se voit.
- **La mise en place** — délai, ce qui a bien marché, l'effort demandé.
- **Les résultats** — **uniquement ceux énoncés par le client**, avec qui, quand, et le lien. Sépare
  **constaté** (« on est passés de X à Y ») et **attendu** (« on espère… ») ; l'attendu ne va jamais dans les chiffres clés.

### Étape 4 — Ce qui manque
Liste les trous (pas de chiffre de résultat, pas de citation du décideur, mise en place non documentée…) et
propose **5 questions d'interview** courtes pour les combler, à poser au champion en 15 minutes. Trous
critiques (aucun résultat constaté) → recommande l'interview **avant** de rédiger ; génère quand même un
brouillon si l'utilisateur insiste, avec des emplacements visibles `[à compléter après interview]`.

### Étape 5 — Choisir l'angle
Propose 2-3 angles possibles selon la matière (ex. gain de temps, montée en compétence, remplacement d'un
outil, déploiement rapide), avec pour chacun la citation qui le porte. L'utilisateur choisit, sinon prends le mieux sourcé.

### Étape 6 — Rédiger les formats configurés
- **Page cas client** (artefact HTML, charte du setup, responsive) : titre centré sur le résultat · le client en
  3 lignes (secteur, taille, équipe concernée) · le défi · pourquoi eux ont choisi · la mise en place · les
  résultats (3 chiffres clés maximum, tous constatés) · 2-3 citations mises en avant · appel à l'action. Pas
  d'animation superflue, lisible sur mobile.
- **Post LinkedIn** : 900 à 1 300 caractères, accroche sur le résultat, une citation, pas de jargon.
- **One-pager commercial** : contexte, problème, solution, résultats, « quand citer cette référence » (profil
  de prospect similaire), contact interne.
- **Slide de référence** (si coché) : logo, un chiffre, une citation.
**Citations** : mot pour mot. Seules des coupes signalées par `[…]` et le retrait des hésitations orales sont
permis ; aucune reformulation mise entre guillemets.

### Étape 7 — Validation client
Prépare le **message de validation** au champion : le lien ou le texte du cas, la **liste des citations
utilisées** avec l'auteur de chacune, les chiffres publiés, et la question de l'accord pour le nom et le logo.
Gmail branché → crée un **brouillon**, ⛔ **n'envoie jamais**. Tant que l'accord n'est pas confirmé, chaque
format porte la mention **« Brouillon — non validé par le client »**. Refus du nom → génère la version anonymisée.

## Format de sortie
1. **Matière trouvée** — tableau récit × sources (avec liens du call), trous signalés.
2. **Questions d'interview** si nécessaire.
3. **Angle retenu**.
4. **Les formats** — page en artefact, textes dans le chat.
5. **Message de validation**.

Authentique, précis, sans superlatifs. Le client parle, l'entreprise s'efface. Info manquante → emplacement visible, jamais comblé.

## Mise à jour
- « change mes réglages cas client » → réaffiche la checklist.
- « le client a validé » → retire la mention brouillon, applique ses corrections, livre les versions finales.
- « version anonyme » → remplace nom, logo et noms de personnes par secteur, taille et fonction.
