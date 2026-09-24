# Skills Eagr pour Claude : ce qu'il faut côté tech

Contexte : 5 skills Claude (prépa RDV, passation CSM, voix client, coaching individuel, coaching
équipe) lisent Eagr via le connecteur MCP. Tests faits le 24/09/2026 avec un compte admin de
l'organisation Eagr.

## P0 · Bloquant

### 1. `list_real_case_sessions` sans `clientId` renvoie du vide pour un compte admin
- **Constaté** : sans `clientId`, la réponse est `data: []`, `hasMore: true`, `nextCursor: null`.
  Avec `clientId=cli_bbd1e5e4-…`, les appels remontent normalement.
- **En face**, `list_live_coach_sessions` sans `clientId` renvoie les sessions **d'autres organisations**
  (`cli_739723c7-…`, `cli_4584d41a-…`).
- **Attendu** :
  - sans `clientId`, filtrer par défaut sur l'organisation du token, de la même façon sur les deux endpoints ;
  - ne jamais renvoyer `hasMore: true` avec `nextCursor: null`.
- Les skills passent désormais toujours `clientId`, donc elles tournent. Le correctif protège les autres usages du connecteur.
- **Test** : `list_real_case_sessions(limit=3)` sans `clientId`, avec un compte admin, doit renvoyer les
  appels de son organisation.

### 2. Rattacher les appels aux deals CRM
- **Constaté** : sur les 3 derniers appels de l'organisation, `deal` = `null` pour 2 d'entre eux. Sur
  « Eagr x Visiativ », `deal` ne contient que le titre et `contactInfo` = `null`.
- Les skills prépa RDV et passation retrouvent les appels via
  `dealProvider + dealExternalId` puis `prospectEmail`. Sans ce rattachement, elles ne trouvent rien.
- **Attendu** :
  - rattacher chaque appel au deal CRM (id externe) et renseigner l'email des participants externes ;
  - exposer l'id externe du deal dans la réponse de la liste.
- **Test** : pour un deal HubSpot connu, `list_real_case_sessions(dealProvider=hubspot, dealExternalId=…)`
  renvoie tous ses appels.

### 3. Confirmer la visibilité par rôle
- Il faut une réponse écrite à ces questions :
  - que voit un `user` : ses appels seulement, ou aussi ceux de ses collègues ?
  - que voient `manager` et `director` : leur équipe, ou toute l'organisation ?
- **Impacts** :
  - prépa RDV veut lire les appels de deals gagnés similaires, souvent portés par d'autres commerciaux ;
  - voix client doit lire toute l'organisation ;
  - l'équipe produit a besoin d'un rôle qui voit toute l'organisation (lecture seule suffit).
- Si ce rôle n'existe pas, il faut le créer.

## P1 · Fiabilité

### 4. Renseigner `url` sur les sessions
- **Constaté** : `url` vaut `null` ou `""`.
- Les skills construisent aujourd'hui le lien `https://app.eagr.ai/v2/call-reviews/<uuid>` à partir
  de `rcs_<uuid>`. Si ce format de route change, tous les liens cassent.
- **Attendu** : `url` = ce lien, sur les appels et sur les sessions live coach (via leur `realCaseSessionId`).

### 5. Insights : lister les champs et filtrer les appels
- **Constaté** : les insights de template ont un `type` = UUID, et le nom est dans
  `metadata.fieldName` (« Missing Features », « Feature to improve »…). Aucun outil ne liste les
  champs d'un template ni ne filtre les appels par champ.
- Résultat : voix client lit 50 appels pour découvrir les champs, puis jusqu'à 100 appels un par un.
  C'est lent et plafonné.
- **Attendu** :
  - un outil `list_insight_fields` (champs des templates de l'organisation) ;
  - un outil qui renvoie les valeurs d'un champ sur une période (id appel, date, contenu, citation,
    commercial, deal), paginé.

### 6. Ne pas remplir un champ quand il n'y a rien
- **Constaté** : « Missing Features » contient une phrase du type « Le prospect ne mentionne pas de
  fonctionnalités manquantes… », alors que « Feature to improve » est vide sur le même appel.
- **Attendu** : un contenu vide quand rien n'est dit. Sinon chaque consommateur doit filtrer ces
  phrases, ce que les skills font aujourd'hui.

### 7. Documenter dans `describe_schema`
- La structure des `callInsights` (types standards `summary`, `key_points` et `action_items`, puis les
  champs de template et leurs `metadata`).
- La règle `clientId` pour les comptes admin.
- Le format de l'URL d'une session.

## P2 · Confort et performance

8. **Lecture groupée** : `get_real_case_sessions(ids[], include)` pour lire 10 à 50 appels en une fois.
9. **Agrégats d'équipe** : scores par compétence et par segment, par équipe et par période. Ça évite
   que coaching équipe interroge chaque membre un par un. Relever aussi la limite de 10 utilisateurs de `compare_users`.
10. **Réanalyse** : peut-on appliquer un nouveau champ d'insight aux appels passés ? Sinon, le dire
    dans l'interface de création du champ.
11. **Champ « Features loved »** à ajouter au template par défaut, pour que voix client ait ses 3 angles.

## Recette une fois P0 fait

Il faut un vrai compte par profil : commercial, CSM, manager, produit. Cas à tester :
- prospect sans deal, prospect avec plusieurs deals ;
- deal sans appel ;
- CRM Pipedrive ;
- template sans champ feedback ;
- équipe de plus de 10 personnes ;
- mémoire Claude désactivée.
