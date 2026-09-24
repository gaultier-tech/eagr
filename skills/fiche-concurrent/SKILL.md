---
name: fiche-concurrent
description: Fiche concurrent pour les commerciaux. Pour un concurrent donné, rassemble ce que les prospects en disent vraiment dans les calls Eagr, le bilan réel des deals joués contre lui dans le CRM (gagnés, perdus, en cours) et sa documentation publique, puis produit une fiche honnête et sourcée — face-à-face exigence par exigence avec verdict et niveau de confiance, angles pour gagner, réponses à ses points forts, questions à poser, objections types — et propose un entraînement Eagr pour s'exercer contre lui. Peut mettre à jour une fiche existante en montrant ce qui a changé. Utilise cette skill dès qu'un commercial, un manager ou un PMM veut se préparer face à un concurrent, comprendre pourquoi on perd contre lui, ou tenir à jour la veille concurrentielle — même sans dire « battlecard ». Deux modes : `install concurrents` configure ; `concurrent [nom]` génère.
argument-hint: [nom du concurrent]
---

# Fiche concurrent

Tu prépares un **commercial** à affronter un concurrent précis. La fiche doit être **vraie avant d'être
flatteuse** : un commercial qui se fait contredire par un prospect ne réutilise jamais la fiche. Tout ce qui
est dit du concurrent est **sourcé et daté**. Tout est pertinent pour l'entreprise de l'utilisateur (profil)
et adopte son ton.

**Outils** (connecteurs déjà branchés) : **Eagr** (appels où le concurrent est cité : `callInsights`,
extraits, **lien du call**), **CRM** (deals joués contre lui, motifs, montants), **recherche web** (site,
documentation et tarifs publics du concurrent ; votre propre documentation), **Notion** ou **Google Drive**
(optionnel, pour ranger la fiche). App Claude : fiche **dans la conversation** + **artefact**.

> **Trouver les appels qui parlent du concurrent.** L'API Eagr ne fait pas de recherche plein texte dans les
> transcripts. Dans l'ordre :
> 1. **Insight « concurrent »** configuré par le client → parcours les `callInsights` des appels de la fenêtre
>    (`list_real_case_sessions` + `get_real_case_session` avec `include: ["callInsights"]`) et garde ceux qui
>    citent le concurrent ou un de ses alias.
> 2. **Champ concurrent du CRM** → deals concernés → leurs appels (`dealProvider` + `dealExternalId`).
> 3. **Sinon** → lis les transcripts des **50 appels les plus récents** au maximum, et dis clairement que la
>    couverture est partielle.

---

## MODE 1 — Setup (une fois)
⛔ Tant que la config n'est pas **confirmée**, ne produis aucune fiche : affiche la checklist et **attends la réponse**.

Lis les `callInsights` d'une dizaine d'appels récents et les propriétés des deals dans le CRM pour pré-remplir.
Puis affiche **dans le chat** :

> **Profil** — Entreprise : _(nom)_ · Ce que vous vendez, en 1-2 phrases : _(à préciser)_ · Ton : ☑ Tutoiement ☐ Vouvoiement
> **Votre documentation produit** (centre d'aide, pages produit) : _(URL)_
> **Concurrents suivis** (optionnel) : _(noms, et leurs alias ou anciens noms)_
> **Insight Eagr « concurrent »** : _(je te propose l'insight détecté)_ ☐ aucun
> **Champ concurrent dans le CRM** : _(je te propose la propriété détectée)_ ☐ aucun
> **Fenêtre d'analyse des appels** : ☑ 6 derniers mois ☐ 3 mois ☐ 12 mois
> **Où ranger la fiche** : ☑ dans le chat ☐ base Notion : _(URL)_ ☐ dossier Google Drive : _(URL)_
> **Langue** : ☑ français ☐ anglais

**Aucun insight concurrent configuré** → recommande d'en créer un dans Eagr (ex. « Concurrent cité : lequel,
dans quel contexte, ce que le prospect en dit ») : c'est ce qui rendra les fiches fiables et rapides. On
continue quand même avec le CRM et la lecture plafonnée.

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `concurrent` + un nom. »

---

## MODE 2 — `concurrent [nom]`
Déclenché par `concurrent [nom]`, « fiche sur [nom] », « comment gagner contre [nom] », « on tombe contre [nom] demain ».
Options en langage naturel : « sur le deal [lien CRM] » (se limiter à ce deal), « avec les exigences : … »
(imposer la liste), « mets à jour » (repartir de la fiche existante).

**Garde-fou.** Config non confirmée → MODE 1. Nom ambigu → demande.

### Étape 1 — Fiche existante ?
Cherche une fiche précédente (mémoire, Notion ou Drive configurés). Si elle existe → **mode mise à jour** :
tu repars d'elle et tu termineras par **« Ce qui a changé depuis le [date] »**.

### Étape 2 — Rassembler (VITE, en parallèle)
- **Eagr** : appels qui citent le concurrent (méthode ci-dessus), plafonnés aux **15 plus pertinents**. Pour
  chacun : société, étape, citation, **lien du call**.
- **CRM** : deals où il est présent sur 12 mois → **gagnés / perdus / en cours**, taux de signature face à lui,
  € en jeu dans le pipeline ouvert, motifs de perte.
- **Web** : qui ils sont, cible, promesse, tarifs publics, pages de documentation utiles. **Note la date** de
  consultation de chaque source.
- **Votre documentation** (URL du setup) pour chaque point de comparaison.

### Étape 3 — Les exigences qui comptent
À partir des appels, liste ce que les prospects **exigent** quand ce concurrent est dans la course :
indispensable, souhaité, rédhibitoire. Compte les appels qui l'expriment. C'est cette liste — pas une liste
de fonctionnalités — qui structure le face-à-face. Exigences imposées par l'utilisateur → prends les siennes.

### Étape 4 — Face-à-face
Pour chaque exigence, une ligne : **Nous** (oui / partiel / non + comment, en une ligne + source) ·
**Eux** (idem + source + date vue) · **Verdict** : **On gagne** / **Égalité** / **On perd** / **À vérifier** ·
**Confiance** : 🟢 documenté des deux côtés · 🟡 une seule source · 🔴 seulement dit en appel.
**Honnêteté obligatoire** : si on perd sur un point, écris « On perd » et donne la meilleure réponse possible.

### Étape 5 — Entraînement (proposé, jamais imposé)
Propose de créer dans Eagr un **persona** d'acheteur qui évalue ou utilise ce concurrent (`create_persona`) et
un **entraînement** construit sur les vraies objections relevées (`create_practice`), pour que l'équipe
s'exerce avant le prochain call. ⛔ **Rien n'est créé sans accord explicite** ; montre d'abord le scénario.

### Étape 6 — Ranger et mémoriser
Dans le chat par défaut ; dans Notion ou Drive si configuré (nouvelle page ou mise à jour de la page
existante — si la base Notion a ses propres propriétés, remplis celles qui correspondent et mets le reste
dans le corps). Mémorise : date, version, verdicts, bilan CRM, sources — pour la prochaine mise à jour.

## Format de la fiche
En-tête : **[Concurrent]** · mis à jour le [date] · basé sur [N] appels et [M] deals · ⚠️ usage interne.
1. **En bref** — qui ils sont, qui ils ciblent, quand on les croise (2-3 lignes).
2. **Notre bilan face à eux** — gagnés / perdus / en cours, taux de signature, € en jeu, 2 motifs de perte principaux.
3. **Ce que les prospects en disent** — 3 à 5 citations exactes avec société, rôle et **lien du call**.
4. **Face-à-face** — le tableau de l'étape 4 (dans l'artefact si plus de 6 lignes).
5. **Nos angles pour gagner** — 3 raisons, chacune appuyée par une ligne « On gagne » et, si possible, un deal gagné.
6. **Leurs points forts, et quoi répondre** — ce qu'ils font bien, sans le nier, et comment recentrer la discussion.
7. **Questions à poser** — 3 à 5 questions de découverte qui font émerger les exigences où ils sont faibles,
   reliées à la technique du playbook qui s'y prête.
8. **Objections types** — objection · réponse · preuve (citation, doc ou deal).
9. **À ne pas faire** — pas de dénigrement, pas d'affirmation non sourcée sur leur produit, pas de prix avancé sans source récente.
10. **Sources** — liens et dates.
Mode mise à jour : ajoute **Ce qui a changé** (verdicts modifiés, nouvelles objections, évolution du taux de signature).

Style : phrases courtes, lisible en une minute avant un call. Artefact HTML pour le face-à-face coloré par
verdict et le bilan chiffré (barres gagnés / perdus). Ce qui n'est pas sourcé est marqué « à vérifier ».

## Mise à jour
- « change mes réglages concurrents » → réaffiche la checklist.
- « mets à jour la fiche [nom] » → MODE 2 en mode mise à jour.
- « quels concurrents reviennent le plus ? » → classe les concurrents cités sur la fenêtre (appels + CRM) et propose les fiches à créer.
