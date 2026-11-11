# Experts — rôles, débat, sortie de scène

La composition de l'équipe est faite une fois par `cadrage-projet` (phase F) et verrouillée dans `equipe.md`. Ce fichier dit comment les rôles interviennent pendant l'exécution.

## Ce qu'est un expert dans Claude cloud

Un rôle incarné par Claude, avec une sortie nommée, un critère de succès, un droit de veto et une exigence portée (fiabilité, simplicité ou élégance). Ce n'est **pas** un sous-agent : il parle dans le même contexte. Un sous-agent séparé n'est utilisé que si l'utilisateur l'a autorisé au gate (`routing.md`).

Plafond : 5 rôles actifs. Une mission en mode standard en a 2 ou 3, la mission éclair n'en a aucun.

## Composer pour n'importe quel sujet

Choisir les rôles d'après les livrables, pas d'après un catalogue. Exemples de familles : stratège, rédacteur, spécialiste du canal, analyste de données, développeur, designer, juriste ou conformité, vérificateur. Un rôle de **vérificateur** (fiabilité, chiffres, liens, cohérence) est recommandé dès qu'il y a plus de deux livrables.

## Débat (phase 2)

- Recopier chaque fiche rôle de `equipe.md` dans `decisions.md`.
- Pour chacune des 1 à 4 décisions structurantes : deux tours maximum, selon `cadrage-projet/references/contradiction.md`.
  - Tour 1 : chaque rôle concerné écrit position, preuve, coût, signal qui ferait changer d'avis.
  - Tour 2 : chacun répond à la position adverse et propose une troisième voie.
  - Clôture : MAESTRO tranche dans l'ordre : contrainte dure du brief, doctrine d'arbitrage, fiable > évident > beau, option la plus réversible.
  - Écrire la décision avec sa colonne **réversible** (oui ou non, à quel coût) et ce qui a été écarté.
- Les décisions non structurantes : le rôle compétent tranche seul, une ligne dans `decisions.md`.
- Une friction touchant promesse, prix, sécurité, conformité ou irréversible ouvre toujours une contradiction formelle datée, même si elle semble mineure.

## Sortie de scène et rappel

`equipe.md` fixe pour chaque rôle sa condition de sortie de scène. Si une sous-tâche fait ressurgir le besoin d'un rôle sorti, le rappeler avec le même livrable nommé et le même critère de succès. Ne pas improviser un rôle voisin. Si aucun rôle ne couvre une sous-tâche imprévue : c'est une bifurcation. Bloquer si deviner faux coûterait des heures, sinon avancer et tracer en une ligne.

## Enrichissement persona (rôles "expert de domaine" seulement)

Pour les rôles dont la valeur tient à une école de pensée, enrichir la fiche dans `decisions.md` :

- **École de pensée** : le courant porté, ce qui le distingue des voisins.
- **Méthodes éprouvées** : 2 à 4 méthodes concrètes appliquées systématiquement, avec leur logique.
- **Angle unique** : ce qu'il voit que les autres ratent.
- **Hacks** : raccourcis à fort rendement.
- **Secret sauce** : le geste signature, l'ordre d'opérations, le détail contre-intuitif.
- **Biais** : ce vers quoi il sur-oriente, pour que MAESTRO le compense à la clôture.

Pas d'enrichissement pour un rôle mécanique (vérificateur, orchestrateur, gardien technique). Le contenu vient de la recherche benchmark (praticiens réels, études de cas), jamais d'un personnage inventé.
