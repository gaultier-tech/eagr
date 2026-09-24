# Skills Eagr pour Claude

| Skill | Pour qui | Commande | Rôle Eagr minimum | Connecteurs |
|---|---|---|---|---|
| `prep-rdv` | Commercial | `prépa RDV [email]` (sans email : prochain RDV de l'agenda) | user | Eagr, CRM, web · Calendar (option) |
| `handover-csm` | Commercial (envoi) · CSM (`kickoff`) | `handover [email]` · `kickoff [client]` | user | Eagr, CRM, Gmail, web · Slack (option) |
| `feature-feedback` | Produit | `voix client [période]` | manager / director / admin | Eagr · CRM (option) |
| `coaching-user` | Manager | `coaching [nom]` | manager | Eagr, CRM |
| `coaching-team` | Manager | `coaching équipe [équipe]` | manager | Eagr, CRM |

`install eagr` règle le profil partagé (entreprise, offre, ton, CRM) une seule fois pour toutes les skills (commande portée par `prep-rdv`, qui doit donc être installée).
`coaching-team` et `coaching-user` se livrent **ensemble**.

## Déployer chez un client

1. **Admin claude.ai du client** : ajouter le connecteur **Eagr** au niveau de l'organisation, provisionner
   les 5 fichiers `dist/*.skill`, et vérifier que l'**exécution de code** et la **recherche web** sont activées.
2. **Chaque utilisateur** : Paramètres → Connecteurs → connecter Eagr (son propre compte), son CRM, Gmail /
   Calendar / Slack selon la skill. Activer la **mémoire** si possible (sinon les skills affichent un bloc
   de config et un bloc-journal à recoller).
3. **Admin Eagr du client** (pour `feature-feedback`) : créer l'insight « Feedback produit » (réglages
   conseillés dans la skill, section Pré-requis).
4. Premier lancement : `install eagr`, puis la commande `install …` de chaque skill.

## Côté Eagr (hors skills, à corriger dans le produit)

- `list_real_case_sessions` renvoie `data: []` avec `hasMore: true` et `nextCursor: null` (constaté avec un
  compte admin). Les skills le traitent comme une anomalie, mais tant que ce n'est pas corrigé, elles ne
  peuvent pas lire les appels.
- Renvoyer une **URL de session** dans les réponses du connecteur (les skills n'affichent un lien que s'il est fourni).
- Ajouter un outil qui **liste les types d'insights** et **filtre les appels par insight** (aujourd'hui
  `feature-feedback` échantillonne et lit les appels un par un, plafond de 100).
- Confirmer la **visibilité par rôle** (un commercial voit-il les appels des deals gagnés de ses collègues ?).

## Modifier une skill

Éditer `<skill>/SKILL.src.md` (et `_socle.md` pour les règles communes), puis `python3 build.py` : régénère
`<skill>/SKILL.md` et `dist/<skill>.skill`, et vérifie le nom et la longueur de la description (≤ 1024).
