---
name: deck-prospect
description: Deck de suivi sur mesure après un rendez-vous commercial. À partir de tous les appels Eagr avec un prospect (découverte, démo, négociation) et du CRM, construit un deck aux couleurs de l'entreprise qui reprend SA situation, SES enjeux avec ses propres mots, ses outils actuels, le coût de ne rien changer calculé uniquement sur les chiffres qu'il a donnés, la réponse point par point, l'offre adaptée à partir de votre grille tarifaire et les prochaines étapes. Vérifie d'abord ce que la découverte a vraiment couvert (selon le playbook) : ce qui manque n'est pas inventé, il devient une question pour le prochain rendez-vous. Livre un .pptx (ou Google Slides si Drive est branché). Utilise cette skill dès qu'un commercial veut envoyer une présentation personnalisée, un business case ou une proposition après un call — même sans dire « deck ». Deux modes : `install deck` configure ; `deck [société ou email]` génère.
argument-hint: [société ou email du prospect]
---

# Deck prospect

Tu construis la présentation qu'un **commercial** envoie après un rendez-vous, **tant que la conversation
est chaude**. Le prospect doit s'y reconnaître : ses mots, ses chiffres, ses priorités — pas un modèle avec
son logo collé dessus. Et rien n'y est inventé : **ce que la découverte n'a pas établi devient une question,
pas une slide**. Tout est pertinent pour l'entreprise de l'utilisateur (profil) et adopte son ton.

**Outils** (connecteurs déjà branchés) : **Eagr** (appels avec le prospect : transcripts, insights, **scores
du playbook** qui disent ce que la découverte a couvert, **lien du call**), **CRM** (deal, étape, contacts,
montant visé), **recherche web** (présentation de la société), **Google Drive** (optionnel : dépôt et
conversion en Google Slides), skill **pptx** pour générer le fichier.

> **Recette Eagr.** `list_real_case_sessions` avec `prospectEmail` (chaque contact) ou `dealProvider` +
> `dealExternalId` ; puis `get_real_case_session` avec `include: ["transcript", "callInsights", "results",
> "speakers"]`. Ici le transcript est nécessaire : les citations doivent être exactes.

> Pour le compte-rendu HTML propre à Eagr, voir `compte-rendu-eagr`. Cette skill-ci sert à toute entreprise, à ses couleurs.

---

## MODE 1 — Setup (une fois)
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun deck : affiche la checklist et **attends la réponse**.

> **Profil** — Entreprise : _(nom)_ · Ce que vous vendez et pour qui (1-2 phrases) : _(à préciser)_ · Ton : ☑ Vouvoiement dans le deck
> **Vos 3-5 capacités clés** (ce que le produit résout) : _(à préciser, ou URL de vos pages produit)_
> **Charte** : ☑ à partir d'un de vos decks existants (.pptx à m'envoyer — je reprends masques, couleurs, polices) ☐ à partir de votre site : _(URL)_ ☐ neutre
> **Grille tarifaire** : _(à m'envoyer : offres, prix, paliers, règles de remise)_ ☐ pas de slide prix
> **Preuves réutilisables** (optionnel) : cas clients, chiffres publics, logos autorisés
> **Structure** : ☑ structure par défaut (ci-dessous) ☐ ma propre structure : _(à m'envoyer)_
> **Livraison** : ☑ fichier .pptx ☐ Google Slides dans le dossier Drive : _(URL)_
> **Langue** : ☑ langue du prospect (celle des appels) ☐ toujours français

Charte depuis un .pptx → utilise la skill **pptx** pour en extraire masques, thème de couleurs, polices, logo ;
depuis le site → relève couleurs (hex), polices, logo. Résume en 5 lignes et fais valider.

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `deck` + la société ou l'email du prospect. »

---

## MODE 2 — `deck [société ou email]`
Déclenché par `deck [x]`, « prépare la présentation pour [x] », « business case [x] », « proposition pour [x] ».

**Garde-fou.** Config non confirmée → MODE 1. Aucun appel trouvé dans Eagr → dis-le et demande si l'on part
des notes du commercial (collées dans le chat).

### Étape 1 — Rassembler (en parallèle)
- **Eagr** : tous les appels avec le prospect, du plus ancien au plus récent (5 max en lecture complète ; au-delà, insights seulement).
- **CRM** : deal, étape, contacts et rôles, montant visé, date de closing.
- **Web** (1 recherche) : activité, taille, actualité.

### Étape 2 — Ce que la découverte a établi (et ce qui manque)
Extrais, avec **citation + lien du call** pour chaque élément :
contexte (taille, organisation, outils actuels) · **enjeux** dans leurs mots · **chiffres donnés par le
prospect** (volumes, temps passé, coûts, effectifs) · critères de décision · qui décide et comment ·
calendrier · réactions au prix · concurrents évoqués · prochaines étapes convenues.
Puis lis les **scores du playbook** sur les compétences de découverte : chaque élément **absent ou flou**
(budget non abordé, décideur inconnu, douleur non chiffrée…) passe dans la liste **« À obtenir au prochain
rendez-vous »**, avec la question à poser.
Montre ce bilan au commercial **avant** de générer, en 10 lignes maximum, et demande s'il veut compléter.

### Étape 3 — Le deck (structure par défaut, adaptable)
1. **Couverture** — société du prospect, date, et leur enjeu principal en une phrase, dans leurs mots.
2. **Ce que nous avons compris** — 3 points sur leur situation. Termine par « Avons-nous bien compris ? ».
3. **Vos enjeux** — 2 à 4 enjeux, **chacun avec une citation exacte** (prénom et rôle si le prospect l'accepte, sinon le rôle seul).
4. **Aujourd'hui** — leurs outils et façon de faire, là où ça coince.
5. **Ce que coûte le statu quo** — **uniquement** calculé sur leurs chiffres. Formule complète dans les notes
   de l'orateur. Pas de chiffres donnés → la slide est **retirée** et la question passe dans « À obtenir ».
6. **Notre réponse** — une ligne par enjeu de la slide 3 : l'enjeu → ce qui y répond → comment, concrètement.
7. **Ce qui change** — avant / après sur leurs indicateurs ; tout chiffre projeté est étiqueté « estimation » avec
   son hypothèse ; une preuve (cas client, chiffre public) si le setup en fournit.
8. **Proposition** — offre et prix tirés **de la grille tarifaire**, dimensionnés sur leur taille, logique de remise
   explicite. Pas de grille, ou budget jamais abordé → slide remplacée par « Construisons l'offre ensemble » avec les questions.
9. **Prochaines étapes** — dates, et qui fait quoi des deux côtés, à partir de ce qui a été convenu en appel.

Règles de rédaction : titres de slide qui affirment quelque chose (« Vos équipes perdent 6 h par semaine en
ressaisie », pas « Enjeux ») ; 3 à 5 lignes par slide ; citations **mot pour mot**, coupes signalées `[…]` ;
aucune information interne (notes de scoring, commentaires sur les interlocuteurs, montant visé du CRM).

### Étape 4 — Générer et livrer
Génère le **.pptx** avec la skill **pptx**, en appliquant la charte (masques du deck modèle si fourni).
Drive configuré → dépose le fichier dans le dossier et, si la conversion en Google Slides est possible, renvoie
ce lien ; sinon, le lien du .pptx. Relis le fichier généré (texte qui déborde, slide vide, citation tronquée) avant de livrer.

## Format de sortie (dans le chat)
1. **Bilan de découverte** — ce qui est établi / ce qui manque.
2. **Le deck** — fichier ou lien, plus le plan des slides en une ligne chacune.
3. **À obtenir au prochain rendez-vous** — les questions, reliées aux techniques du playbook.
4. **Sources** — les appels utilisés, avec leurs liens.
Pour modifier : « refais la slide 5 », « version plus courte pour le DG », « ajoute une slide intégration ».

## Mise à jour
- « change mes réglages deck » → réaffiche la checklist.
- « nouvelle grille tarifaire » / « nouveau modèle de deck » → remplace l'élément et reconfirme.
