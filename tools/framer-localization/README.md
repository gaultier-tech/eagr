# Localisation EN d'eagr.ai

Ce dossier applique les traductions du copy deck EN (doc « Eagr — Copy deck EN du site (eagr.ai/en) ») dans le panneau Localization de Framer, via l'API serveur officielle de Framer (`framer-api`).

## Prérequis

1. Une clé d'API du projet : Framer → Settings → **API Keys**.
2. La clé dans la variable d'environnement `FRAMER_API_KEY`. Dans une session Claude Code cloud, elle se règle dans les réglages de l'environnement, pas dans le chat.
3. L'accès réseau à `api.framer.com`. Dans une session cloud, il faut ajouter ce domaine aux domaines autorisés de l'environnement.

## Utilisation

```bash
npm install
npm run dry-run            # simulation : rien n'est écrit, rapport dans report.md
npm run apply              # écrit les traductions EN et les slugs
npm run apply-and-publish  # écrit, ajoute les redirections 308 /en/<ancien> → /en/<nouveau>, publie
```

## Ce que fait le script

- Il lit toutes les chaînes à traduire du projet (`getLocalizationGroups`).
- Pour chaque chaîne FR, il cherche la traduction dans `translations.json` (802 paires tirées du deck, plus les meta et les slugs). La comparaison ignore les espaces, les apostrophes et les guillemets typographiques.
- Les textes que le deck abrège avec « […] » sont reconnus par leur début et leur fin.
- Les textes courts qui ont plusieurs traductions selon la page (« 2x », « -40% »…) ne sont écrits que si la page correspond. Sinon, ils sont listés comme ambigus.
- Il n'écrase pas les valeurs en lecture seule.
- Il liste à part les textes FR qui n'ont pas de traduction dans le deck.

## Régénérer translations.json

`translations.json` est construit à partir du deck exporté (voir l'historique de la session). Pour ajouter une traduction à la main, ajoute une entrée `{ "fr": "...", "en": "...", "kind": "exact", "scope": null }` dans `pairs`.
