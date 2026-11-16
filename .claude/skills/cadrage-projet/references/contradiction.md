# Protocole de contradiction

Objectif : que les décisions structurantes soient tranchées par confrontation de positions argumentées, pas par défaut ni par le premier réflexe.

## Quand l'ouvrir

- Une décision qui engage le périmètre, la promesse faite, le prix, la sécurité, la conformité ou une action irréversible.
- Deux rôles de `equipe.md` ont des exigences qui s'opposent (fiabilité contre élégance, par exemple).
- Toute friction touchant promesse, prix, sécurité, conformité ou irréversible ouvre **systématiquement** une contradiction formelle datée, même si elle paraît mineure.

Pas de contradiction pour les décisions non structurantes : le rôle compétent tranche seul, en une ligne.
Volume : 1 à 4 contradictions par mission (3 à 4 en mode complète). Mode éclair : aucune.

## Déroulé : deux tours maximum

Dans Claude cloud, les rôles sont incarnés par le même Claude : chaque position doit être écrite honnêtement, avec la preuve la plus forte, comme si elle était défendue par quelqu'un de convaincu.

**Tour 1.** Chaque rôle concerné écrit :
- **Position** : ce qu'il propose.
- **Preuve** : le cas réel, la donnée ou la source qui l'appuie.
- **Coût** : ce qu'on sacrifie en le choisissant.
- **Signal** : ce qui lui ferait changer d'avis.

**Tour 2.** Chacun répond à la position adverse et propose une **troisième voie** qui garde l'essentiel des deux.

**Clôture.** MAESTRO ou le cadrage tranche en appliquant dans l'ordre :
1. La contrainte dure du brief (budget, délai, ligne rouge, promesse).
2. La doctrine d'arbitrage de la mission.
3. Fiable > évident > beau.
4. L'option la plus réversible.

Écrire la décision avec : le motif (lequel des quatre a tranché), ce qui est écarté et pourquoi, et la colonne **réversible** (oui ou non, à quel coût).

## Format dans journal-decisions.md

```
## AAAA-MM-JJ — Décision #n : <intitulé>
- Tour 1 — <Rôle A> : position — preuve — coût — signal
- Tour 1 — <Rôle B> : position — preuve — coût — signal
- Tour 2 : réponses et troisième voie
- CLÔTURE : <décision> — motif : <contrainte dure | doctrine | fiable > évident > beau | réversibilité>
- Écarté : <quoi et pourquoi>
- Réversible : oui | non — coût :
```

Reporter ensuite la ligne utile dans le tableau "Décisions de fond" du brief.

## Pendant l'exécution

Si une décision structurante imprévue apparaît en phase 2 ou 3 : même protocole, consignée dans `decisions.md`. Si elle change le périmètre du brief verrouillé, c'est un avenant (`lock-brief.sh --avenant`), avec l'accord de l'utilisateur.
