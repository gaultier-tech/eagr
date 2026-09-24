---
name: risque-deals
description: Radar des deals en danger. Chaque matin (ou à la demande), passe en revue les deals ouverts du CRM, lit leurs appels Eagr (insights, engagements, couverture du playbook de qualification) et, si Gmail est branché, les échanges écrits, puis attribue à chaque deal un score de risque expliqué — silence anormal, un seul interlocuteur, qualification incomplète, blocage cité mais jamais traité, concurrent en embuscade, étape qui s'enlise, date repoussée, engagement non tenu. Chaque alerte vient avec sa preuve (citation + lien du call) et UNE action nommée à faire aujourd'hui, et le score est suivi d'un jour à l'autre. Utilise cette skill dès qu'un manager, un dirigeant commercial ou un commercial veut savoir quels deals risquent de glisser, préparer une revue de pipeline ou un forecast, ou comprendre pourquoi un deal inquiète — même sans dire « risque ». Deux modes : `install risques` configure ; `risques` génère.
argument-hint: [optionnel : nom d'un deal, « forecast », « ce qui a bougé »]
---

# Radar des deals en danger

Chaque matin, tu **relis ce qui se passe réellement sur chaque deal ouvert** et tu dis, preuves à
l'appui, lesquels sont en train de glisser. Tu restes **factuel et mesuré** : sans preuve, pas d'alerte. Tout est pertinent pour
l'entreprise de l'utilisateur (profil) et adopte son ton.

**Outils** (connecteurs déjà branchés) : **CRM** (deals ouverts, étape, montant, date de closing et ses
changements, propriétaire, contacts, dernière activité), **Eagr** (appels du deal : `callInsights`,
**scores du playbook** dont les compétences de qualification, interlocuteurs, **lien du call**),
**Gmail** (optionnel : qui a écrit en dernier, délais de réponse), **Slack** (optionnel, pour diffuser).
App Claude : radar **dans la conversation**.

> **Recette Eagr.** Appels d'un deal : `list_real_case_sessions` avec `dealProvider` + `dealExternalId` ; à
> défaut, `prospectEmail` des contacts. Détail : `get_real_case_session` avec `include: ["callInsights",
> "results", "speakers"]`. Transcript **uniquement** pour les deals qui finissent dans le haut du classement.

> **Lecture seule.** Cette skill ne modifie jamais le CRM (étape, montant, date, propriétaire). Seule écriture
> possible : le message de diffusion, et une propriété « score de risque » dans le CRM **si** l'utilisateur
> l'a demandé au setup.

---

## MODE 1 — Setup (une fois)
⛔ Tant que la config n'est pas **confirmée**, ne produis aucun radar : affiche la checklist et **attends la réponse**.

Lis les étapes et propriétés du CRM et les `callInsights` d'une dizaine d'appels récents pour pré-remplir,
puis affiche **dans le chat** :

> **Profil** — Entreprise : _(nom)_ · Ton : ☑ Tutoiement ☐ Vouvoiement · CRM : _(détecté)_
> **Deals suivis** : ☑ ouverts, closing prévu dans les 6 prochains mois ☐ tous les ouverts — pipeline : ☑ new business ☐ tous — montant minimum : _(optionnel)_
> **Ordre des étapes** : _(je te propose l'ordre détecté ; corrige si besoin)_
> **Insights Eagr** (détectés) : engagements / prochaines étapes → _(insight)_ · objections → _(insight)_ · concurrents → _(insight)_ ☐ aucun
> **Compétences de qualification du playbook** : _(je te propose celles détectées — ex. budget, décideur, processus de décision, douleur chiffrée)_
> **Signaux et poids** : ☑ poids par défaut (voir plus bas) ☐ je veux les ajuster
> **Taille du radar** : ☑ les 5 deals les plus à risque + les compteurs
> **Diffusion** : ☑ dans le chat ☐ Slack, canal : _(nom)_ ☐ en plus, un message privé à chaque commercial pour ses propres deals
> **Score dans le CRM** : ☐ écrire le score dans une propriété du CRM (je te demanderai confirmation avant la première écriture)
> **Planification** : ☐ du lundi au vendredi à 8h (heure de Paris)

Applique, **marque la config confirmée**, enregistre (mémoire si disponible), puis : « C'est prêt. Tape `risques` quand tu veux. »

**Planification** → tâche planifiée qui lance `risques`. Crons en **UTC** : 8h à Paris = `0 6 * * 1-5` en
été, `0 7 * * 1-5` en hiver. Préviens l'utilisateur.

**Aucun connecteur CRM** → propose un **mode démo** sur un pipeline **fictif** (6 deals inventés, noms
génériques, montants ronds), étiqueté « EXEMPLE FICTIF » en tête et en pied. Jamais présenté comme réel.

---

## MODE 2 — `risques`
Déclenché par `risques`, « quels deals sont en danger », « revue de pipe », « radar ». Variantes :
- `risques [deal]` / « pourquoi [deal] est à risque » → la **piste complète** d'un seul deal (étape 6).
- `risques bougé` / « qu'est-ce qui a changé depuis hier » → uniquement les variations.
- `risques forecast` → **revue de forecast** : pour chaque deal compté dans le forecast, ce qui le
  justifie dans les appels… ou ce qui manque pour y croire.

**Garde-fou.** Config non confirmée → MODE 1.

### Étape 1 — Périmètre (CRM)
Deals ouverts selon la config. Pour chacun : étape (libellé via l'ordre du setup, jamais l'id brut),
montant, propriétaire, date de closing **et historique de ses changements**, date d'entrée dans l'étape,
contacts, dernière activité. Calcule, **sur ce pipeline**, la durée médiane par étape et l'intervalle
habituel entre deux interactions : c'est la référence de « normal ».

### Étape 2 — Lecture légère de tout le pipe (VITE)
> **Perf** : deals en parallèle ; **insights et scores seulement** ; 3 derniers appels max par deal.
> Si le volume est trop lourd, lis moins d'appels par deal mais **couvre tous les deals**, et indique-le en pied.

Par deal : interlocuteurs réellement présents dans les appels (pas la liste de contacts du CRM), engagements
et prochaines étapes (insight), objections et concurrents (insights), **couverture de la qualification**
(compétences du playbook : faite / partielle / absente sur l'ensemble des appels), date du dernier appel.
Gmail branché → qui a écrit en dernier et depuis combien de jours. **Deal sans appel dans Eagr** → noté
« non couvert », scoré sur le CRM seul avec la mention.

### Étape 3 — Score provisoire, puis lecture approfondie de la tête de liste
Score provisoire pour tous (étape 4). Pour les **10 plus hauts** seulement : lis les transcripts des 1-2
derniers appels pour trouver la citation exacte qui prouve chaque signal.

### Étape 4 — Scorer (0-100)
| Famille | Signal | Poids défaut |
|---|---|---|
| Engagement | **Silence** : jours sans interaction vs l'intervalle habituel à cette étape ; aggravé si le dernier message vient de nous | 20 |
| Engagement | **Engagement non tenu** : une prochaine étape convenue en appel qui n'a pas eu lieu | 15 |
| Couverture | **Un seul interlocuteur**, ou aucun décideur jamais présent en appel | 15 |
| Qualification | **Trous de qualification** : compétences clés du playbook absentes alors que le deal est avancé | 15 |
| Dit en appel | **Blocage nommé non traité** : sécurité, juridique, achats, intégration… cité et jamais planifié | 15 |
| Dit en appel | **Concurrent** cité, surtout avec un prix | 10 |
| Dynamique | **Enlisement** : durée dans l'étape vs médiane · **date repoussée** (×2 si deux fois ou plus) | 10 |

Paliers : 🟢 0-24 sain · 🟡 25-49 à suivre · 🟠 50-74 en danger · 🔴 75-100 critique.
**Contradictions = signal** : le CRM dit « négociation » mais aucun prix n'a été discuté dans les appels ; le
commercial a noté « en bonne voie » mais le décideur n'a jamais parlé. Signale-les.
**Variation** : compare au score d'hier (journal en mémoire ; sinon propriété CRM si activée). Pas
d'historique → « premier passage, pas de variation » — n'invente aucun mouvement.

### Étape 5 — Une action par deal signalé
**Une** action, **une** personne nommée, faisable **aujourd'hui**, reliée au signal principal. Pas « relancer le
client » mais « Julie : envoyer à Marc le récap sécurité promis le 12 et lui proposer un créneau jeudi avec leur
RSSI ». Quand c'est possible, appuie-toi sur ce qui a débloqué des situations semblables sur des deals gagnés.
Si le signal est un trou de qualification, cite la **question** du playbook à poser.

### Étape 6 — Piste complète (sur demande)
Pour « pourquoi [deal] ? » : chaque signal déclenché, son poids, la preuve (citation, interlocuteur, date,
**lien du call**), l'historique du score. Ne cache jamais le raisonnement derrière un chiffre.

### Étape 7 — Diffuser et mémoriser
Dans le chat ; Slack si activé (propriétaire mentionné par son identifiant Slack, jamais `@channel`) ; message
privé par commercial si activé. **Premier envoi** : aperçu et accord. Rien de nouveau depuis hier → publie un message
d'une ligne qui le confirme. Score CRM activé → **demande confirmation avant la toute première écriture**.
Mets à jour le **journal risques** (30 jours glissants : score et signaux par deal et par jour).

## Format de sortie
- **Titre** : `Radar du [date] — [X] € à risque ([y] % du pipe suivi), [±] vs hier`.
- **Compteurs** : deals revus · 🔴 · 🟠 · 🟡 · 🟢 · non couverts.
- **⬇️ Dégradés depuis hier** — une ligne. C'est la plus lue.
- **Les deals signalés**, un paragraphe chacun (le plus risqué d'abord, dans la limite configurée) : palier · deal · montant ·
  étape · propriétaire · score (variation) → **preuve** (citation dans sa langue d'origine + interlocuteur + date,
  ou « 19 jours sans réponse ») + [lien du call] → **action** (qui, quoi).
- **⬆️ Repassés au vert** — une ligne, pour voir les actions payer.
- **Pied** : deals lus, appels lus, deals non couverts, profondeur de lecture, ce qui n'a pas pu être vu.

Court, chiffré, sans langue de bois : un deal critique est écrit comme tel, même s'il appartient au meilleur commercial.
Citations jamais traduites. Montants lus tels que le CRM les structure (attention aux séparateurs).

## Mise à jour
- « change mes réglages risques » → réaffiche la checklist.
- « ajuste les poids » → affiche le tableau des signaux et applique les nouveaux poids (total = 100).
