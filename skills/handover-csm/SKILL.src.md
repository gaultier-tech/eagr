---
name: handover-csm
description: Passation d'un compte signé du commercial au CSM. Côté COMMERCIAL (usage principal) : à la signature, génère la fiche de passation à partir du deal gagné dans le CRM, des appels Eagr et de SES échanges email avec le client (parties prenantes et comment les aborder, ce qui a été vendu, objectifs et critères de succès, promesses faites, red flags, plan d'onboarding, to-do priorisée pour le CSM), lui fait compléter les zones d'ombre en chat, puis l'envoie au CSM par email ou Slack après accord. Côté CSM : `kickoff [client]` retrouve la fiche reçue et prépare le kickoff. Utilise cette skill dès qu'un deal est signé et doit passer au Customer Success, qu'un commercial veut briefer un CSM, ou qu'un CSM prépare le kickoff d'un compte transmis, même sans dire « handover ». Commandes : `install handover` ; `handover [email ou société]` ; `kickoff [client]`.
---

# Passation commercial → CSM

Le **commercial qui a signé** est le seul à avoir toute la matière : ses appels, **ses emails** avec le
client, le contexte non écrit. Le CSM n'a pas accès à la boîte mail du commercial. Donc :
**c'est le commercial qui lance `handover` et qui envoie la fiche au CSM.** La fiche elle-même est
écrite **pour le CSM** (« tu reprends ce compte »). Tes échanges avec l'utilisateur (le commercial)
se font dans son ton habituel.

**Outils** : **CRM** (obligatoire : deal gagné, contacts, montant, CSM assigné), **Eagr** (appels du
deal), **Gmail** (les fils du commercial avec le client : engagements écrits, ton, points en suspens),
**recherche web** (actu du compte), **Gmail / Slack** pour l'envoi. App Claude : tout se fait en chat.

<!-- SOCLE -->

---

## MODE 1 · Setup (une fois)
Déclenché par `install handover`, ou automatiquement au premier `handover`.
⛔ Sans config confirmée, pas de fiche : affiche la checklist et **attends la réponse**.

1. Pré-vol (§0). Lis les **propriétés du CRM** (deal et société) pour repérer celle qui porte le
   **CSM assigné** (ex. « CSM », « Customer Success Owner », propriétaire secondaire).
2. Affiche (profil partagé seulement s'il manque) :

> **Passation**
> - Qui est le CSM d'un compte : ☑ _[propriété CRM détectée]_ ☐ je te le dirai à chaque fois
> - Envoi au CSM : ☑ Email (Gmail) ☐ Slack (message privé) · ☑ Brouillon d'abord (tu relis dans Gmail) ☐ Envoi direct après mon accord
> - ☑ Déposer aussi la fiche en **note sur la société dans le CRM** (le CSM la retrouve même sans l'email)
> - ☑ Me poser les questions « à compléter » avant l'envoi
>
> **Sections de la fiche** (décoche ce que tu ne veux pas) :
> ☑ Parties prenantes ☑ Ce qui a été vendu ☑ Objectifs et critères de succès ☑ Promesses et engagements
> ☑ Red flags ☑ Plan d'onboarding ☑ To-do du CSM

3. Applique, enregistre (mémoire ou bloc « Ma config Eagr »), puis : « C'est prêt. À la signature :
   `handover` + l'email d'un contact du client. »

---

## MODE 2 · `handover [email ou société]` (le commercial)
Déclenché par `handover …`, « deal signé avec … », « passe [client] au CS », « brief le CSM sur … ».

**Garde-fou.** Config absente → MODE 1. Déduis la **société** depuis l'email.

### Étape 1 · Le deal gagné
Dans le CRM, cherche le(s) deal(s) **gagné(s)** de la société. Plusieurs → fiche consolidée.
Pas encore en « gagné » → « Le deal n'est pas encore passé en gagné dans le CRM : je prépare quand
même la passation ? » et attends.

### Étape 2 · La matière (en parallèle, vite)
- **CRM** : offre / produits, montant, conditions, durée, dates, contacts, CSM assigné.
- **Eagr** (recette §0) : liste tous les appels du deal, lis les **5 plus utiles** (découverte,
  démo, négociation, le plus récent) en analyse légère.
- **Gmail** (la boîte du commercial) : fils avec le **domaine du client** et les emails des contacts,
  les **5 fils les plus récents ou décisifs** → promesses écrites, engagements, ton, questions restées
  ouvertes, qui répond et qui ne répond plus. Gmail absent → dis que la section Promesses ne reposera
  que sur les appels.
- **Web** (une recherche) : actualité récente du compte (réorganisation, levée, acquisition).

### Étape 3 · La fiche (écrite pour le CSM)
Uniquement les sections configurées. Chaque affirmation porte sa **source** (CRM, appel Eagr du
[date], email du [date]) ; les inférences sont marquées `[à valider au kickoff]`.

- **👥 Parties prenantes** : champion, décideur économique, utilisateurs clés, détracteurs. Pour chacun :
  - **Rôle et influence** : son poids dans la décision et dans l'usage à venir.
  - **Sentiment** : positif / neutre / réticent, appuyé sur les appels et les emails.
  - **Style de communication** `[à valider au kickoff]` : orienté résultat / data / relationnel /
    process ; canal et rythme préférés ; ce qui le motive, ce qui le braque. Déduit de sa façon de
    parler et d'écrire. **Strictement professionnel** : pas de jugement de personnalité, rien sur la
    vie privée ou la santé. Cette fiche sera envoyée par écrit.
  - **Ses enjeux** : ce qu'il a à gagner ou à perdre selon que le projet réussit ou échoue.
  - **➡️ Comment l'embarquer** : une action concrète.
  - Termine par **qui appeler en premier** et pourquoi.
- **📦 Ce qui a été vendu** : offre, périmètre, montant, conditions, durée, date de signature.
- **🎯 Objectifs et critères de succès** : pourquoi ils ont acheté, résultats attendus, **métriques
  que le CSM doit faire atteindre**. Cités, pas supposés.
- **🤝 Promesses et engagements** : tout ce que la vente a promis (fonctionnalités, délais,
  accompagnement, conditions), avec la source. C'est ce que le CSM devra tenir.
- **🚩 Red flags** : objections non résolues, timeline serrée, décideur absent, sur-promesses, budget
  tendu, emails restés sans réponse.
- **🚀 Plan d'onboarding** : premières actions, quick wins, jalons, rythme des points.
- **✅ To-do du CSM** : cases `[ ]` concrètes et priorisées, groupées **Avant le kickoff**,
  **Semaine 1**, **30 premiers jours**. Chaque tâche : action · avec qui · pourquoi (une demi-ligne).
  Chaque red flag majeur et chaque promesse à risque se retrouve ici.

### Étape 4 · À compléter par toi (le commercial)
Ce que la data ne tranche pas, **tu le demandes maintenant au commercial** plutôt que de le laisser au
CSM. En **un seul message**, 5 questions maximum, fermées ou courtes, par exemple :
engagements pris à l'oral non écrits ? · qui a vraiment porté le choix en interne ? · un sujet
sensible à éviter au kickoff ? · une date ou une échéance clé côté client ? · un interlocuteur à
ménager ?
Le commercial peut répondre « passe ». Intègre les réponses dans la fiche (source : « le commercial »)
et retire la question du reste.

### Étape 5 · Envoi au CSM
1. **Destinataire** : le CSM depuis la propriété CRM configurée. Vide → demande « À quel CSM
   j'envoie la fiche ? ».
2. **Aperçu** : montre l'objet et le début du message.
   Objet : **`Passation client · [Société] · fiche de reprise`** (format fixe : le CSM le retrouve
   avec `kickoff`). Corps : une ligne d'intro du commercial, puis la fiche. Termine par : « Fiche
   préparée à partir du CRM, des appels Eagr et de mes échanges avec le client. Les points
   [à valider au kickoff] sont des hypothèses. »
3. **N'envoie qu'après un accord explicite** (« ok », « envoie »). Selon la config : brouillon Gmail
   (donne le lien) ou envoi ; Slack en message privé au CSM.
4. Si l'option est cochée : dépose la même fiche en **note sur la société** dans le CRM (après le même accord).
5. Confirme : « Envoyé à [CSM]. Il peut préparer son kickoff avec `kickoff [société]`. »

---

## MODE 3 · `kickoff [client]` (le CSM)
Déclenché par `kickoff …`, « je reprends [client] », « prépare mon kickoff avec … ».

1. Pré-vol (§0). Cherche la fiche dans **le Gmail du CSM** (objet `Passation client · [Société]`) puis
   dans les **notes CRM** de la société.
2. **Fiche trouvée** → résume-la en 10 lignes, puis produis l'**agenda du kickoff** (objectifs à
   valider, questions pour lever les `[à valider au kickoff]`, prochaines étapes) et rappelle la
   to-do « Avant le kickoff ». Complète avec le CRM (état actuel) et une recherche web si utile.
3. **Pas de fiche** → ne reconstruis pas une fiche au rabais depuis la boîte du CSM (elle ne contient
   pas les échanges de la vente). Dis : « Je ne trouve pas de fiche de passation pour [société].
   Demande à [commercial du deal, depuis le CRM] de lancer `handover [société]`. » Propose en
   attendant un mini-brief CRM + web, clairement étiqueté comme partiel.

---

Factuel, concret, orienté action. Pas de fichier : tout reste dans le chat, l'email et le CRM.

## Mise à jour
- `install eagr` → profil partagé. « change mes réglages handover » → réaffiche la checklist du MODE 1.
