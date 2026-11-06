# Benchmark-first

MAESTRO n'invente rien de zéro. Tout part de ce qui est déjà éprouvé, décortiqué, puis adapté. La méthode s'adapte à la nature de la tâche.

## Quand le benchmark est obligatoire

- Une décision de fond (stratégie, structure d'offre, architecture, choix d'outil, angle).
- Un chiffre, un standard ou un repère de marché qui sera suivi littéralement.
- Un livrable dont l'efficacité dépend d'un pattern connu (page de vente, séquence, onboarding, script, plan de contenu…).

## Quand une dispense suffit

Tâche purement mécanique ou interne : mise en forme, conversion, calcul sur données fournies, résumé d'un document fourni, correction. Écrire alors dans `BENCHMARK.md` : `Dispense : <raison en une ligne>`. Une dispense n'est pas valable pour un chiffre externe.

## Principe

Pour chaque sous-tâche à enjeu :
1. Trouver 2 à 3 cas réels reconnus comme efficaces (3 en mode complète).
2. Décortiquer le pattern précis, pas l'impression générale.
3. Le consigner dans `BENCHMARK.md`.
4. L'adapter à l'objectif et au sujet de la mission.

## Un bon cas de référence

- Réel et identifiable : produit, campagne, page, séquence, système, article, playbook, offre, dépôt de code.
- Reconnu efficace : résultats publics, adoption large, cité par des praticiens, ou repris massivement.
- Assez documenté pour en extraire la mécanique.

Pour une tâche "construire ou automatiser" : chercher aussi un dépôt GitHub existant (étoiles, activité récente, licence permissive) et un workflow n8n tout fait. Un dépôt ou un workflow éprouvé est une référence à part entière. Regarder d'abord le dépôt de la session : une brique déjà là bat une brique à écrire.

À éviter : listicles génériques, avis sans preuve, cas isolé unique, contenu d'un vendeur sur son propre produit.

## Décortiquer = extraire le pattern

Mauvais : "ils ont une bonne page de vente."

Bon : "structure en 7 blocs : accroche problème, preuve sociale chiffrée en position 2, offre décomposée en 4 lignes, garantie inversée, FAQ qui traite les 5 objections, CTA répété 3 fois, urgence datée. La preuve sociale vient avant l'offre."

Pour chaque cas, noter : structure, leviers, chiffres, ordre d'opérations, ce qui est contre-intuitif.

## Sources et outils dans Claude cloud

- `WebSearch` et `WebFetch` (outils différés : les charger avec `ToolSearch` si besoin). Toute affirmation chiffrée : 3 sources concordantes, sinon mentionner l'incertitude.
- Outils GitHub (`mcp__github__*`) pour les dépôts, uniquement dans le périmètre autorisé de la session.
- Un sous-agent de recherche par bloc indépendant **seulement si autorisé au gate** (`routing.md`). Sinon, enchaîner les recherches soi-même.
- Une page fermée ou privée : ne pas inventer son contenu, noter "non lu" et chercher une autre source.

## Seuils

- Toute affirmation chiffrée dans un livrable : 3 sources concordantes ou incertitude écrite.
- Toute option de fond au cadrage : 2 cas réels minimum.
- Jamais un nombre de mémoire qui sera suivi littéralement.

## Format de BENCHMARK.md

```
## [Sous-tâche ou décision]
- Cas 1 : [nom] — [lien]
  Pattern extrait : [le mécanisme précis]
  Chiffres : [si disponibles]
- Cas 2 : ...
Adaptation retenue pour la mission : [comment on transpose]
```

ou `Dispense : <raison>`.

Le livrable final reste propre : pas de "d'après X". Les sources restent dans `BENCHMARK.md`.
