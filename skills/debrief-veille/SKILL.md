---
name: debrief-veille
description: Le débrief commercial du matin. Reprend tous les appels clients analysés par Eagr la veille (le lundi, depuis vendredi) et sort en une lecture ce qu'un manager doit savoir — ce qui s'est passé sur chaque compte, ce que les prospects ont soulevé (selon les insights configurés dans Eagr : objections, concurrents, besoins…), la qualité d'exécution du playbook, le meilleur moment de la veille à partager à l'équipe, les points à coacher et les deals à surveiller. Chaque ligne renvoie au call dans Eagr. Peut tourner seul chaque matin et poster sur Slack. Utilise cette skill dès qu'un manager ou un dirigeant commercial veut savoir ce qui s'est dit hier, préparer son stand-up, ou suivre l'activité de son équipe sans réécouter les calls — même sans dire « débrief ». Deux modes : `install débrief` configure ; `débrief [date]` génère.
argument-hint: [date, ex. hier, 23/09 — défaut : jour ouvré précédent]
---

# Débrief de la veille

Tu rédiges le **débrief du matin** d'un **manager commercial** : ce qu'il doit savoir des appels d'hier
en moins de deux minutes de lecture, avec de quoi agir (coacher, relancer, partager). Tu t'appuies sur les
**analyses Eagr** des appels, pas sur ton intuition. Tout est pertinent pour l'entreprise de l'utilisateur
(profil) et adopte son ton.

**Outils** (connecteurs déjà branchés) : **Eagr** (appels réels de la veille : `callInsights`, scores du
playbook, interlocuteurs, deal lié, **lien du call**), **CRM** (optionnel : étape et montant du deal),
**Slack** ou **Gmail** (optionnel, pour diffuser). App Claude : débrief **dans la conversation**.

> **Recette Eagr.** Appels de la fenêtre : `list_real_case_sessions` avec `dateFrom` / `dateTo` (UTC) et
> `category: "analyzed"`, en suivant la pagination (`nextCursor`). Détail : `get_real_case_session` avec
> `include: ["callInsights", "results", "speakers", "contactInfo"]`. Équipe du manager :
> `list_teams_with_members`.

---

## MODE 1 — Setup (une fois)
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun débrief : affiche la checklist et **attends la réponse**.

D'abord, **lis les `callInsights` d'une dizaine d'appels récents** pour lister les insights que ce client a
configurés dans Eagr (ils sont libres), et propose d'en faire les **rubriques** du débrief. Puis affiche
**dans le chat** (pré-coché ; seul le nom d'entreprise est à taper) :

> **Profil** — Entreprise : _(nom)_ · Ton : ☑ Tutoiement ☐ Vouvoiement · ☑ Direct
> **Périmètre** : ☑ mon équipe _(détectée)_ ☐ toute l'organisation ☐ une liste de commerciaux
> **Rubriques** (insights détectés — décoche, renomme, réordonne) : ☑ _(insight 1)_ ☑ _(insight 2)_ ☑ _(insight 3)_ …
> **Blocs** : ☑ Les comptes d'hier ☑ Exécution du playbook ☑ Le moment à partager ☑ À coacher ☑ Deals à surveiller
> **Volume** : ☑ 3 éléments max par rubrique (le reste en « + N autres »)
> **Diffusion** : ☑ dans le chat ☐ Slack, canal : _(nom)_ ☐ email : _(destinataires)_ — ☐ canal public : ne cite pas les scores individuels
> **Planification** : ☐ du lundi au vendredi à 9h (heure de Paris)

Si **aucun insight n'est configuré** chez ce client : dis-le, recommande d'en créer au moins deux dans Eagr
(ex. « objections », « prochaine étape convenue ») pour un débrief plus riche, et propose en attendant un
débrief basé sur les scores et les résumés d'appel.

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `débrief` quand tu veux. »

**Planification demandée** → crée une tâche planifiée du lundi au vendredi qui lance `débrief`. Les crons
sont en **UTC** : 9h à Paris = `0 7 * * 1-5` en été (CEST), `0 8 * * 1-5` en hiver (CET). Préviens
l'utilisateur et propose de basculer au changement d'heure.

---

## MODE 2 — `débrief [date]`
Déclenché par `débrief`, « qu'est-ce qui s'est dit hier », « résumé des calls d'hier », « prépare mon stand-up ».

**Garde-fou.** Config non confirmée → MODE 1.

### Étape 1 — Fenêtre
Par défaut, **le jour ouvré précédent**, de 00:00 à 23:59 **heure de Paris** (converti en UTC pour Eagr). Le
**lundi** : de vendredi 00:00 à dimanche 23:59. Date donnée → ce jour-là.

### Étape 2 — Rassembler (VITE)
> **Perf** : liste d'abord, puis détail des appels **en parallèle** ; insights et scores seulement, jamais le
> transcript entier. Garde le **lien du call** de chaque appel.

Filtre sur le périmètre configuré. **Aucun appel** → une seule ligne (« Aucun appel client analysé hier
dans Eagr ») et arrête-toi. Charge le **journal débrief** (mémoire) pour les moyennes glissantes et les
éléments déjà vus.

### Étape 3 — Construire
- **🗂️ Les comptes d'hier** — une ligne par appel : commercial · société · type d'appel ou étape du deal ·
  score playbook · **prochaine étape convenue** (⚠️ si aucune) · [lien du call]. Groupe par commercial au-delà de 8 appels.
- **Rubriques d'insights** — pour chaque insight configuré, les éléments de la veille **regroupés** : la même
  objection dans trois appels = une ligne « ×3 » avec les trois liens. Pour chacun : ce qui a été dit (citation
  courte si l'insight en porte une), qui (société, rôle), comment le commercial a réagi si l'insight le dit,
  [lien du call]. 🆕 si absent du journal des 30 derniers jours.
- **📈 Exécution du playbook** — score moyen de la veille vs moyenne glissante 30 jours (journal) ; la
  compétence la mieux tenue et la plus en retrait sur l'ensemble des appels.
- **🌟 Le moment à partager** — l'appel où une technique du playbook a été le mieux exécutée : qui, quoi, pourquoi
  c'est un bon exemple, [lien du call]. Un seul, pour que l'équipe l'écoute.
- **🎯 À coacher** — 1 à 3 écarts **récurrents** (une même technique manquée sur plusieurs appels, ou par le même
  commercial plusieurs jours de suite d'après le journal). Pour chacun, propose un entraînement Eagr existant
  (`list_practices`) — sans l'affecter.
- **🚩 Deals à surveiller** — appels sans prochaine étape, décideur absent alors qu'on est tard dans le cycle,
  signal négatif fort (report, gel budgétaire, concurrent en tête). Montant et étape si le CRM est branché.

Rubrique ou bloc vide → « Rien hier. » (une ligne, pas de remplissage).

### Étape 4 — Diffuser
Dans le chat par défaut. Slack / email si activé : même contenu, compact, liens cliquables au format Slack
`<url|texte>`, jamais d'URL brute. Option « canal public » → retire les scores individuels et le bloc « À
coacher » (à garder pour le manager en privé). **Premier envoi** : aperçu et accord ; en planifié, envoi direct.
Un appel Eagr échoue → termine quand même, et signale en pied de message ce qui manque.

### Étape 5 — Mémoriser
Mets à jour le **journal débrief** (fenêtre glissante de 30 jours) : par jour, nb d'appels, score moyen, éléments
par rubrique avec compteur, techniques manquées par commercial. Sert aux 🆕, aux moyennes et à la récurrence.

## Format de sortie
En-tête : `Débrief du [date] — [N] appels · [M] commerciaux · score moyen [x] ([±] vs 30 j)`.
Puis les blocs dans l'ordre configuré. Phrases courtes, un lien du call par ligne, zéro paragraphe long.
Pour creuser la voix du client côté produit, renvoie vers la skill `feature-feedback`.

## Mise à jour
- « change mes réglages débrief » → réaffiche la checklist (périmètre, rubriques, blocs, volume, diffusion, planification).
- « rafraîchis les rubriques » → relis les `callInsights` récents et repropose les rubriques.
