# Outils et connecteurs

Pour chaque sous-tâche, MAESTRO identifie avec quoi elle se fait de façon fiable, compare les candidats, tranche, et signale ce qui manque. Le résultat va dans `TOOLING.md`, en phase 0, juste après `equipe.md`.

## Principe : existant et ouvert d'abord

À fiabilité égale, priorité à :
1. Une brique déjà en place (outil natif de la session, skill du dépôt ou du compte, connecteur connecté).
2. Un outil ouvert ou auto-hébergeable (bibliothèque, CLI libre, n8n pour l'automatisation).
3. Un dépôt GitHub existant à adapter plutôt qu'écrire de zéro.
4. Un SaaS ou connecteur propriétaire seulement si rien au-dessus ne fait le travail proprement.

Ne jamais bricoler un contournement fragile quand une brique propre existe.

## Découverte dans Claude cloud (s'arrêter au premier niveau qui couvre le besoin)

1. **Outils natifs de la session** : fichiers, Bash, navigateur Playwright pré-installé, `Artifact`, sous-agents (si autorisés), `WebSearch` et `WebFetch` (outils différés, à charger avec `ToolSearch`).
2. **Skills** : liste affichée dans la session (docx, pptx, xlsx, pdf, dataviz, deep-research, studio-lancement-app, claude-api…). `SearchSkills` pour en chercher d'autres.
3. **Connecteurs déjà connectés** : voir la liste des outils `mcp__<connecteur>__*` de la session ; `ListConnectors` pour l'état réel. Un connecteur peut être listé mais non authentifié (la session le signale) : le traiter comme "à connecter".
4. **À ajouter** : `SuggestConnectors`, `SearchMcpRegistry`, `SearchPlugins`. Remonter au gate : nom, ce que ça apporte, ce qui reste bloqué sans lui. MAESTRO ne connecte rien lui-même ; l'utilisateur le fait dans les réglages de ses connecteurs.
5. **Aucune solution fiable** : ligne rouge de cadrage, l'utilisateur tranche.

## Contraintes de l'environnement cloud à vérifier

- **Réseau** : l'accès sortant suit la politique de l'environnement. Un hôte refusé est un blocage à remonter, pas à contourner. Pour une explication ou une demande d'ouverture : outil de documentation de l'environnement, puis `update_environment` (qui demande son propre accord).
- **Clés et jetons** : jamais dans le chat. Utiliser le formulaire sécurisé `request_credential` pour l'hôte concerné.
- **Disque et temps** : conteneur éphémère, disque limité ; ne pas télécharger de gros jeux de données sans raison.
- **Ce que l'utilisateur peut ouvrir** : les fichiers du dépôt de la session. Un livrable généré ailleurs est copié dans `livrables/`.

## Grille de sélection

| Critère | Poids | Ce qu'on regarde |
|---|---|---|
| Fiabilité pour CETTE tâche | 25 | Fait-il exactement le travail, ou le détourne-t-on ? |
| Déjà en place et éprouvé | 20 | Zéro friction si oui |
| Ouvert, sans enfermement | 20 | Open source, données maîtrisées, pas de coût par tâche |
| Réversibilité et sécurité | 15 | L'action est-elle annulable ? Touche-t-elle une ligne rouge ? |
| Coût | 12 | Crédits, quotas, abonnement |
| Effort d'intégration | 8 | Temps pour brancher et fiabiliser |

Score = somme pondérée sur 100. Écart de moins de 10 points : prendre l'outil déjà en place, sinon le plus ouvert.

## Format de TOOLING.md

```
## <sous-tâche>
Candidats : <outil A> / <outil B> / <outil C>
Scores : A=82  B=71  C=40
Retenu : A — <raison en une ligne>
Connecteur requis : <nom ou "—"> — statut : connecté | à connecter | indisponible
Dépense ou ligne rouge : <aucune | laquelle>
Plan B si indisponible : <outil natif dégradé ou attente>
```

Terminer par la section "À connecter par l'utilisateur avant la phase 3" (case à cocher, ce que ça apporte, comment le connecter). Au début de la phase 1, vérifier l'état réel de ce qui est listé ; si un connecteur indispensable manque : `statut: BLOQUÉ` avec la liste exacte.
