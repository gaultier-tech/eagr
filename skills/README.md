# Skills Eagr

Skills prêtes à l'emploi, pour l'équipe Eagr comme pour les clients Eagr. Chaque skill fonctionne en deux
temps : `install …` pose la configuration une fois (profil, mapping des insights Eagr, diffusion), puis la
commande génère le livrable.

| Skill | Pour qui | Configurer | Lancer | Livrable |
|---|---|---|---|---|
| [bilan-deals](bilan-deals/SKILL.md) | Dirigeant commercial, manager, RevOps | `install bilan` | `bilan [période]` | Pourquoi on gagne / on perd, écarts playbook gagnés vs perdus, actions + entraînements |
| [debrief-veille](debrief-veille/SKILL.md) | Manager commercial | `install débrief` | `débrief [date]` | Débrief du matin des appels de la veille, dans le chat ou sur Slack |
| [fiche-concurrent](fiche-concurrent/SKILL.md) | Commercial, manager, PMM | `install concurrents` | `concurrent [nom]` | Fiche concurrent sourcée + entraînement contre ce concurrent |
| [cas-client](cas-client/SKILL.md) | Marketing, commercial, CSM | `install cas client` | `cas client [société]` | Page cas client, post LinkedIn, one-pager, demande de validation |
| [risque-deals](risque-deals/SKILL.md) | Manager, dirigeant commercial, commercial | `install risques` | `risques` | Radar quotidien des deals en danger : score expliqué, preuve, une action nommée |
| [objections](objections/SKILL.md) | Manager, enablement | `install objections` | `objections [période]` | Tableau de bord des objections + meilleures réponses réelles de l'équipe |
| [deck-prospect](deck-prospect/SKILL.md) | Commercial | `install deck` | `deck [société]` | Deck de suivi sur mesure (.pptx / Google Slides) + questions pour le prochain RDV |

## Principes communs
- **Insights Eagr libres** : chaque client configure les siens. Au setup, la skill lit les `callInsights`
  d'appels récents et propose un mapping ; sans insight adapté, elle le dit et se replie sur les scores,
  les résumés ou une lecture plafonnée des transcripts.
- **Chaque élément cité renvoie au call dans Eagr** (lien du call).
- **Rien d'inventé** : pas de citation, pas de chiffre sans source ; une donnée manque → on l'écrit.
- **Aucune écriture sans accord** : création d'entraînement, affectation, envoi Slack / email.
- **Planification** : les crons sont en UTC — 9h à Paris = 7h UTC en été, 8h UTC en hiver.
- Skills voisines : `feature-feedback`, `handover-csm`, `coaching-user`, `prep-rdv`, `compte-rendu-eagr`.
