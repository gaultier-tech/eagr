---
name: feature-feedback
description: Voix du client pour le produit. À partir de l'insight Eagr « feedback produit » capté dans les calls, sort le feedback sous trois angles : fonctionnalités manquantes (réclamées), à améliorer (frictions) et vraiment bien (ce qu'ils adorent). Chaque feature est priorisée par fréquence, tendance, sévérité et impact deal (€ de pipeline concerné, deals perdus), avec verbatims et référence de l'appel. Nécessite qu'un insight « feedback produit » soit configuré dans Eagr ; sinon la skill explique comment le créer. Utilise cette skill dès qu'une équipe produit veut prioriser son backlog depuis la voix du client, savoir quelle feature manquante coûte des deals, ou ce que les prospects adorent, même sans dire « features ». Commandes : `install voix client` configure ; `voix client [période]` génère.
---

# Voix du client · feedback produit

Tu aides une **équipe produit** à exploiter ce que les **prospects et clients disent dans les calls** :
fonctionnalités **manquantes**, **à améliorer**, **vraiment bien**. Tu t'appuies **uniquement sur
l'insight Eagr** configuré pour ça, jamais sur ton intuition.

**Outils** : **Eagr** (obligatoire : insights des appels), **CRM** (optionnel : impact en € et deals
perdus). App Claude : brief texte dans la conversation + un **artefact** graphique.

<!-- SOCLE -->

---

## Pré-requis · l'insight « feedback produit » dans Eagr

Cette skill lit un **insight Eagr** (les `callInsights` de chaque appel) qui capte le feedback
fonctionnel. Sans cet insight, **aucune analyse fiable n'est possible** : n'invente rien.

Si l'insight n'est pas trouvé, affiche ce message et **arrête-toi** :

> **Il faut d'abord configurer un insight « Feedback produit » dans Eagr.**
> Un administrateur Eagr de ton organisation le crée une fois ; ensuite chaque call analysé le remplit.
> Réglages conseillés :
> - **Nom** : Feedback produit
> - **Consigne** : « Relève chaque fois que l'interlocuteur parle d'une fonctionnalité : il en réclame
>   une qui n'existe pas, il se plaint d'une limite ou d'une friction sur une existante, ou il en
>   salue une. »
> - **Champs à extraire** : `type` (manquante / à améliorer / aimée) · `feature` (nom court) ·
>   `verbatim` (citation exacte) · `concurrent` (si la demande est faite en comparaison d'un
>   concurrent, lequel)
>
> ⚠️ L'insight s'applique aux appels analysés **après** sa création. Demande à Eagr si les appels
> passés peuvent être réanalysés ; sinon, compte quelques semaines de calls avant une première analyse utile.

---

## MODE 1 · Setup (une fois)
Déclenché par `install voix client` (alias : `install features`), ou automatiquement au premier lancement.
⛔ Sans config confirmée, pas d'analyse : affiche la checklist et **attends la réponse**.

1. Pré-vol (§0). **Rôle** : si `get_me` renvoie le rôle `user`, préviens : « Ton compte Eagr ne voit
   probablement que tes propres appels. Pour une voix client de toute l'équipe, il faut un rôle
   manager, director ou admin. »
2. **Détecter l'insight.** Le connecteur n'a pas d'outil pour lister les types d'insights : échantillonne.
   Prends les **20 derniers appels analysés** des 30 derniers jours (`list_real_case_sessions`,
   `category=analyzed`), lis-les en parallèle avec `include=["callInsights"]`, et liste les **types
   ou noms d'insights distincts** avec leur nombre d'occurrences.
   - Un insight ressemble clairement à du feedback produit → propose-le.
   - Aucun → **message du Pré-requis**, stop.
   - Note la **date du plus ancien appel** qui porte cet insight : c'est le début de la couverture.
3. Checklist (profil partagé seulement s'il manque) :

> **Insight Eagr utilisé** : ☑ _[nom détecté]_ (vu dans N appels sur 20, présent depuis le [date])
> **Période par défaut** : ☑ 30 derniers jours ☐ 7 jours ☐ trimestre
> **Périmètre** : ☑ Toute l'organisation ☐ Une équipe _(équipes Eagr détectées)_
> **Seuil d'affichage** : ☑ features citées dans ≥ 2 appels distincts (en dessous : « signaux faibles »)
> **Croiser l'impact deal (CRM)** : ☑ oui _(coché seulement si un CRM est branché ; sinon ☐ et grisé)_

4. Applique, **marque la config confirmée**, enregistre, puis : « C'est prêt. `voix client` (+ période) quand tu veux. »

---

## MODE 2 · `voix client [période]`
Déclenché par `voix client`, `features [période]`, « qu'est-ce que les prospects réclament »,
« quelle feature nous coûte des deals », « ce que les clients adorent ».

**Garde-fou.** Config non confirmée → MODE 1. Période : celle demandée, sinon celle par défaut.
Si la période commence **avant** le début de couverture de l'insight, dis-le en tête de brief
(« l'insight n'existe que depuis le [date] : la période est couverte à X % »).

### Étape 1 · Historique
Charge le **journal voix client** (mémoire ou bloc-journal recollé) : compteurs par feature des
périodes précédentes → tendance. Sinon : « Première période suivie, pas encore de tendance. »

### Étape 2 · Rassembler (vite, plafonné)
- **Appels** : `list_real_case_sessions(dateFrom, dateTo, category=analyzed)` sur le périmètre, en
  suivant la pagination. **Plafond : 200 appels.** Au-delà, prends les 200 plus récents et dis-le
  (« 200 appels lus sur N »).
- **Insights** : lis-les par **lots parallèles de 10** avec `include=["callInsights"]`. Ne garde que
  l'insight configuré. Pour chaque retour : feature, type, verbatim, appel (titre · date · id), le
  commercial et, s'il y en a un, le deal.
- Si **aucun** retour sur la période → ne conclus pas « pas de feedback » à la légère : vérifie la
  couverture (l'insight existait-il sur la période ? les appels ont-ils été lus ?) et dis ce que tu as
  constaté. Si l'insight a disparu des appels récents → message du Pré-requis.
- **CRM** (si croisement activé) : pour chaque feature, retrouve les deals des appels concernés →
  **€ de pipeline ouvert** et **deals perdus ou reportés** où elle apparaît. Pas de deal rattaché à un
  appel → cet appel ne compte pas dans l'impact €, et dis combien d'appels sont dans ce cas.

### Étape 3 · Classer et prioriser
**Normalise les noms** de features (« export Excel », « export xls » → une seule). Range chaque retour
dans **un seul** angle : le `type` de l'insight s'il existe ; sinon, classe toi-même et marque
`[classé par Claude]`.
Pour **chaque feature** :
- **Fréquence** : nombre de mentions / nombre d'appels et de deals distincts.
- **Tendance** vs journal : ↑ / → / ↓.
- **Sévérité** : 🔴 bloquant d'achat · 🟠 friction · 🟢 confort (d'après la formulation et le lien aux pertes).
- **Qui et segment** : rôle de l'interlocuteur, segment ou taille de deal.
- **Impact deal** (si CRM) : € de pipeline concerné + nombre de deals perdus.
- **Concurrent** : cité si la demande est faite en comparaison (« X le fait »).
- **Verbatims** : 1-2 citations exactes + référence de l'appel (lien seulement si Eagr fournit une URL, §0).

Trie chaque angle par **impact** (fréquence × € et pertes).

### Étape 4 · Dashboard (artefact, même message)
Après le brief texte, crée un **artefact HTML + Chart.js** (Chart.js via cdnjs, couleurs en dur,
chaque graphe dans un `try/catch`, aucun graphe sans données, pas de fichier ni de tableau ASCII) :
- top features **manquantes** par fréquence (barres) ;
- **€ de pipeline concerné** par feature manquante (barres, si CRM) ;
- répartition des mentions par angle ;
- si historique : **tendance** des 3 features principales (lignes).

### Étape 5 · Mémoriser
Mets à jour le **journal voix client** (une seule entrée, les 6-8 derniers snapshots) : période,
nombre d'appels lus, et par feature son compteur et son angle. Sans mémoire → affiche le bloc-journal (§0).

## Format du brief texte
En-tête : période, appels lus, couverture de l'insight, nombre de features remontées. Puis :
- 🔴 **Fonctionnalités manquantes** : la plus réclamée d'abord ; fréquence, tendance, € et pertes, qui et segment, verbatim + référence.
- 🟠 **À améliorer** : même format.
- 🟢 **Vraiment bien** : points forts cités (utile aussi pour l'enablement et le marketing).
- 🌫️ **Signaux faibles** : sous le seuil, une ligne chacun.
- 💡 **Reco produit** : les 3 chantiers à plus fort impact, justifiés par la data.

## Mise à jour
- « change mes réglages voix client » → réaffiche la checklist (insight, période, périmètre, seuil, CRM).
