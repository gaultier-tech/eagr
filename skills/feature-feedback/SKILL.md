---
name: feature-feedback
description: Voix du client pour le produit. À partir des insights Eagr et de ce que les prospects DISENT dans les calls, sort le feedback produit sous trois angles : fonctionnalités manquantes (ce qu'ils réclament), à améliorer (frictions), et vraiment bien (ce qu'ils adorent). Chaque feature est priorisée par fréquence, tendance, sévérité, et impact deal (€ de pipeline concerné + deals perdus à cause d'elle), avec les verbatims et le lien Eagr. Utilise cette skill dès qu'une équipe produit veut prioriser son backlog depuis la voix du client, savoir quelle feature manquante coûte des deals, ou ce que les prospects adorent — même sans dire « features ». Deux modes : `install features` configure ; `features [période]` génère.
argument-hint: [période, ex. 30 derniers jours]
---

# Voix du client — feedback produit

Tu aides une **équipe produit** à exploiter ce que les **prospects disent dans les calls** :
fonctionnalités **manquantes**, **à améliorer**, et **vraiment bien**. Tu t'appuies sur les
**insights Eagr** (pas sur ton intuition). Tout est pertinent pour l'entreprise (profil), ton du profil.

**Outils** (connecteurs déjà branchés) : **Eagr** (insights « feedback produit / features » + verbatims
+ liens des calls), **CRM** (pour croiser l'impact deal : pipeline €, deals perdus), **recherche web**
(optionnel). App Claude : le brief s'affiche **dans la conversation** + un **artefact graphique** (pas de fichier).

> ⛔ **Pré-requis insights.** Cette skill lit un insight Eagr qui **capture le feedback feature**. Si
> Eagr **ne renvoie aucun insight de ce type** sur la période, **n'invente rien** : dis à l'utilisateur
> qu'il faut **d'abord configurer un insight « feedback produit / features » dans Eagr** (pour que cette
> info soit trackée à chaque call), puis arrête-toi. Pas d'insight = pas d'analyse fiable.

---

## MODE 1 — Setup (une fois)

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
⛔ Tant que la config n'est pas confirmée, ne lance pas d'analyse : affiche la checklist et **attends la réponse**.

D'abord, **lis les types d'insights disponibles dans Eagr** pour proposer le bon mapping. Puis affiche
cette checklist **dans le chat** (pré-cochée ; un seul champ à taper, le nom d'entreprise) :

> **Profil** — Entreprise : _(nom)_ · Ton : ☑ Direct · CRM : HubSpot
> **Insight Eagr = feedback feature** : _(je te propose l'insight détecté ; confirme ou choisis-en un autre)_
> **Période par défaut** : ☑ 30 derniers jours ☐ 7 j ☐ trimestre
> **Périmètre** : ☑ Toute l'équipe ☐ Un commercial / segment précis
> **Seuil d'affichage** : ☑ features mentionnées ≥ 2 fois (sous le seuil = regroupées en « signaux faibles »)
> **Croiser l'impact deal (CRM)** : ☑ oui (€ pipeline + deals perdus par feature)

Applique, **marque la config confirmée**, enregistre, puis : « C'est prêt. Tape `features` (+ période) quand tu veux. »

---

## MODE 2 — `features [période]`
Déclenché par `features`, « voix client produit », « qu'est-ce que les prospects réclament », « quelle feature nous coûte des deals », « ce que les clients adorent ».

**Garde-fou.** Config non confirmée → fais le MODE 1. Période : celle demandée, sinon la période par défaut.

### Étape 1 — Historique (tendance)
Charge le **journal feature** (mémoire) : compteurs des périodes précédentes par feature, pour calculer
la **tendance** (en hausse / stable / en baisse). Sinon : « Première période suivie — pas de tendance encore. »

### Étape 2 — Rassembler (VITE)
> **Perf** : sources **en parallèle** ; sur Eagr prends les **insights/résumés** (pas les transcripts bruts) ;
> **plafonne** aux verbatims les plus représentatifs (2-3 par feature). Capture le **lien Eagr** de chaque call cité.

- **Eagr** : les **insights « feedback feature »** des calls de la période, avec les **verbatims** et le **lien** du call. **Si aucun → applique le pré-requis insights ci-dessus et stoppe.**
- **CRM** (si croisement activé) : pour chaque feature, les deals où elle apparaît → **€ de pipeline ouvert** concerné et **deals perdus/reportés** liés.

### Étape 3 — Classer en 3 angles + prioriser
Range chaque retour dans **un seul** angle : **manquante** (réclamée, absente), **à améliorer** (existe
mais friction/limite), **aimée** (point fort cité spontanément). Pour **chaque feature** :
- **Fréquence** : nb de mentions / nb de deals distincts.
- **Tendance** : vs journal (↑ / → / ↓).
- **Sévérité** : 🔴 bloquant d'achat · 🟠 friction · 🟢 confort — déduite de la façon dont c'est dit + du lien aux pertes.
- **Qui & segment** : rôle (champion / utilisateur / décideur) + segment / taille de deal.
- **Impact deal** (si CRM) : **€ de pipeline** concerné + **nb de deals perdus** où la feature apparaît.
- **Concurrent** : flag si demandé en comparaison d'un concurrent (« X le fait »).
- **Verbatims** : 1-2 citations exactes + **lien Eagr cliquable** vers le call.

Trie chaque angle par **impact** (fréquence × € / pertes). Distingue **vérifié** (insights, CRM) de l'**inférence**.

### Étape 4 — Dashboard (artefact graphique, dans la conversation)
Après le brief texte, **crée un artefact Claude** (HTML + Chart.js, rendu inline — **pas** de fichier, **pas** de tableau ASCII) :
- top features **manquantes** par fréquence (barres) ;
- **€ de pipeline concerné** par feature manquante (barres) ;
- répartition des mentions par angle (manquantes / à améliorer / aimées) ;
- si historique : **tendance** d'une feature (ligne, ex. 3 → 8 → 15).
Chart.js via cdnjs ; couleurs en dur ; chaque graphe en `try/catch` ; pas de graphe sans données.

### Étape 5 — Mémoriser (tendance)
Enregistre/mets à jour le **journal feature** (une entrée, gardant les ~6-8 derniers snapshots) :
période, et par feature son compteur + son angle. Permet la tendance au prochain passage.

## Format de sortie (brief texte, sortie principale)
En-tête : période, nb de calls analysés, nb de features remontées. Puis **3 sections priorisées** :
- 🔴 **Fonctionnalités manquantes** — la plus réclamée d'abord ; pour chacune : fréquence, tendance, € pipeline + deals perdus, qui/segment, verbatim + lien Eagr.
- 🟠 **À améliorer** — frictions sur l'existant, même format.
- 🟢 **Vraiment bien** — points forts cités (utile aussi **sales enablement** + **marketing/messaging**).
- 💡 **Reco produit** : les 3 chantiers à plus fort impact (manquantes/à améliorer), justifiés par la data.

Factuel, cité, priorisé par impact. Si une info manque, dis-le. Si pas d'insight feature → message de configuration, pas d'invention.

## Mise à jour
- « change mes réglages features » → réaffiche la checklist (insight mappé, période, périmètre, seuil, croisement CRM).
