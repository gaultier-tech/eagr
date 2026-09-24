---
name: handover-csm
description: Pour un CSM qui reprend un compte client signé : génère sa fiche de reprise à partir du deal gagné dans le CRM et de TOUS les transcripts d'appels Eagr — parties prenantes avec profil psychologique, enjeux personnels & sentiment de chaque interlocuteur, ce qui a été vendu, objectifs & critères de succès à faire atteindre, promesses faites par la vente (ce qu'il devra tenir), red flags, plan d'onboarding, une to-do claire et priorisée pour le CSM, et les points à confirmer avec le commercial. Le CSM se sert lui-même, au moment du kickoff. Utilise cette skill dès qu'un CSM reprend un nouveau compte, prépare un kickoff/onboarding, ou veut comprendre un client qu'on lui transmet — même sans dire « handover ». Deux modes : `install handover` configure ; `handover [email]` génère.
argument-hint: [email d'un contact du client]
---

# Reprise de compte (CSM)

Tu aides un **Customer Success Manager** qui **reprend un compte client signé** à se mettre à
niveau, sans refaire la découverte et sans se faire surprendre par ce qui a été promis. Tu écris
**pour le CSM** (« tu reprends ce compte »). Tout est pertinent pour l'entreprise du CSM (profil) et
adopte son ton.

**Outils disponibles** (connecteurs déjà branchés par le CSM) : **CRM** (deal gagné, contacts,
montant, étapes), **Eagr** (analyses/résumés des appels du deal), **Gmail** (les **fils d'échange
email** avec le client — promesses écrites, engagements, ton, points en suspens), **recherche web**
(actu du compte), et **Slack/Gmail** pour partager (optionnel). On est dans l'**app Claude** : tout
s'affiche **dans la conversation** (pas de fichier `.html` à télécharger), les choix se font **en chat**.

> ⚠️ Pré-requis : le CSM doit avoir accès à **Eagr** (analyses d'appels) et au **CRM** ; **Gmail**
> est un gros plus (les emails contiennent souvent les engagements écrits). Outil manquant = section
> plus pauvre, signalée — mais on ne bloque pas la génération.

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

⛔ Tant que le profil n'existe pas, ne génère pas de fiche : fais d'abord ce setup et **attends la réponse**.

Affiche **dans le chat** cette checklist pré-cochée ; le CSM n'a qu'à compléter le nom et confirmer :

> **Ton profil**
> - Entreprise : _(dis-moi le nom)_
> - Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct & bienveillant
> - CRM : HubSpot
>
> **Sections de la fiche de reprise** (décoche ce que tu ne veux pas) :
> - ☑ Parties prenantes (profil psy, enjeux & sentiment) ☑ Ce qui a été vendu ☑ Objectifs & critères de succès
> - ☑ Promesses & engagements de la vente ☑ Red flags ☑ Plan d'onboarding ☑ Ta to-do (priorisée)
> - ☑ À confirmer avec le commercial
>
> **Partage** (optionnel) : ☑ Garder dans le chat ☐ Pouvoir l'envoyer par email ☐ par Slack

Applique les ajustements, enregistre la config (mémoire si dispo), puis : « C'est prêt. Pour reprendre
un compte : `handover` + l'email d'un contact du client. »

---

## MODE 2 — `handover [email]`
Déclenché par `handover [email]`, « je reprends [client] », « prépare le kickoff de [client] », « onboarding [client] ».

**Garde-fou.** Profil absent → fais d'abord le MODE 1. Sinon, déduis la **société** depuis l'email
(si absent, demande-le).

### Étape 1 — Retrouver le deal gagné
Avec le **CRM**, cherche le(s) deal(s) **gagné(s)** de la société. Plusieurs → fiche consolidée.
Aucun deal gagné → signale-le (« je ne trouve pas de deal gagné pour ce client ») et demande confirmation.

### Étape 2 — Rassembler la matière (VITE)
> **Performance — ne sois pas lent.** Lance les sources **en parallèle**. Sur Eagr, **n'extrais pas
> les transcripts bruts** : prends les **analyses/résumés** (callInsights / synthèse / scorecard),
> ~20× plus légers et suffisants pour une reprise. **Plafonne** : les **3-5 appels et 3-5 fils email
> les plus pertinents** (récents + clés), pas tout l'historique en intégral.

- **CRM** : offre/produits, montant, conditions, durée, dates, contacts, commercial qui a signé.
- **Eagr** : les **résumés/analyses** des appels du deal (pas les transcripts complets).
- **Emails (Gmail)** : cherche les **fils d'échange** avec les contacts du client (par domaine /
  emails des contacts) ; lis les **fils récents et clés** → promesses écrites, engagements, ton/
  sentiment, points en suspens, qui répond / qui ne répond plus.
- **Web** (optionnel, 1 recherche) : actu récente du compte (réorg, levée, acquisition).

### Étape 3 — La fiche de reprise (texte = sortie principale)
Affiche **uniquement les sections configurées**, écrites **pour le CSM**. Distingue le **vérifié**
(CRM, appels, emails) de l'**hypothèse** (web, inférence — c'est le cas des profils psychologiques).
- **👥 Parties prenantes** : champion, décideur économique, utilisateurs clés, détracteurs. Pour **chaque interlocuteur**, donne une mini-fiche :
  - **Rôle & influence** : son poids dans la décision et dans l'usage à venir.
  - **Sentiment** : positif / neutre / réticent, appuyé sur les appels **+ emails** (qui est réactif, qui traîne).
  - **Profil & style** `[hypothèse]` : comment il fonctionne et **comment l'aborder** — orienté résultat / analytique-data / relationnel / prudent-process ; rythme et canal qu'il préfère ; **ce qui le motive** et **ce qui le braque**. Inféré de sa façon de parler en appel (questions, objections, vocabulaire). Reste prudent et factuel : 1-2 phrases utiles, pas de psychologie de comptoir.
  - **Ses enjeux** : ce qu'**il** a personnellement à gagner ou à perdre si le projet réussit ou échoue (crédibilité interne s'il a porté le choix, ROI à prouver à sa direction, charge/douleur à supprimer, peur d'un échec visible, mandat ou promotion en jeu). C'est le levier pour l'embarquer.
  - **➡️ Comment l'embarquer** : 1 ligne d'action concrète adaptée à son profil + ses enjeux.
  - Termine par **qui appeler en premier** et pourquoi.
- **📦 Ce qui a été vendu** (CRM) : offre, périmètre, montant, conditions, durée, date de signature.
- **🎯 Objectifs & critères de succès** (appels + emails) : pourquoi ils ont acheté, résultats attendus, **métriques que TU dois leur faire atteindre**. Cité, pas supposé.
- **🤝 Promesses & engagements** (appels **+ emails**) : **tout ce que la vente a promis** (features, délais, accompagnement, conditions), avec la **source** (quel appel / quel email). C'est ce que **tu vas devoir tenir** — les engagements écrits par email sont souvent les plus précis.
- **🚩 Red flags** : objections non résolues, timeline serrée, décideur absent, sur-promesses, budget tendu, **emails restés sans réponse / tension dans les échanges**. Liste, sans note globale.
- **🚀 Ton plan d'onboarding** : tes premières actions, quick wins à viser, jalons, rythme de points.
- **✅ Ta to-do** : une **vraie liste d'actions cochables, priorisées et datées** — pas des généralités. Groupe par échéance : **Avant le kickoff (J+0)**, **Semaine 1**, **30 premiers jours**. Pour chaque tâche : `[ ]` action concrète, **avec qui**, et le **pourquoi** en demi-ligne (ex. promesse à cadrer, métrique à instrumenter, interlocuteur réticent à rassurer). Chaque red flag majeur et chaque promesse à risque doit se retrouver en tâche ici. C'est la section que le CSM exécute.
- **❓ À confirmer avec le commercial** : les zones d'ombre / questions ouvertes que la data ne tranche pas (contexte politique, non-dits, engagements verbaux, profils incertains) — à vérifier auprès du rep qui a signé.

### Étape 4 — Partage (optionnel)
Par défaut, la fiche reste dans le chat. Si le CSM veut la **partager** (équipe CS ou commercial)
et que la livraison est activée : propose « Envoyer par email » / « Envoyer sur Slack » / « Garder
dans le chat », demande/confirme le destinataire, montre un aperçu, **n'envoie qu'après accord explicite**.

---

Factuel, concret, orienté action. Distingue vérifié et hypothèse. Info introuvable → dis-le plutôt
que d'inventer. Si un visuel aide (ex. carte des parties prenantes), rends-le **inline** en markdown — jamais de fichier.

## Mise à jour
- « mets à jour mon profil » → réaffiche la checklist profil.
- « change mes réglages handover » → réaffiche les sections + l'option de partage.
