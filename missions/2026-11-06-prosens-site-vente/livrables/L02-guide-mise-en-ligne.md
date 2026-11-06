# PROSENS — guide de mise en ligne et pièces à fournir

Ce guide accompagne le site `L01-prosens/index.html`. Le site est terminé et se consulte tel quel. Trois informations que vous seul détenez le rendent publiable : le moyen de prise de rendez-vous, les preuves du fondateur et les mentions légales. Rien n'a été publié, acheté ni branché : chaque geste ci-dessous est le vôtre.

## 1. Voir le site

- Ouvrez `livrables/L01-prosens/index.html` dans un navigateur : la page est autonome (CSS et JavaScript inclus, aucune image, aucun cookie, aucun traceur).
- Un aperçu privé est aussi publié sous forme d'artefact : le lien figure dans `LIVRAISON.md`. Il n'est visible que par vous tant que vous ne le partagez pas.

## 2. Les trois pièces à fournir avant la mise en ligne

### 2.1 Votre moyen de prise de rendez-vous (indispensable)

Tous les boutons « Réserver un échange » de la page lisent un seul réglage, en tête du script, dans `index.html` :

```
var CONTACT_URL = '';
```

- Renseigné avec le lien de votre agenda en ligne (par exemple `'https://…'`), tous les boutons l'ouvrent dans un nouvel onglet.
- Laissé vide, les boutons ouvrent un panneau « Préparez votre échange » : le visiteur y répond à trois questions et copie sa demande pour vous l'envoyer. C'est un repli complet, mais il suppose que vous donnez un contact à vos visiteurs par ailleurs.

Un lien d'agenda en ligne donne le meilleur parcours : un seul clic mène à un créneau dans votre agenda. Faites ce changement avant toute mise en ligne.

### 2.2 Les preuves du fondateur

La page présente le fondateur par sa fonction, sans nom ni photo, et attribue ses résultats à sa propre déclaration : « à chaque ouverture de business unit, un chiffre d'affaires multiplié par 4 à 5 sur des marchés B2B émergents ». Pour renforcer la crédibilité, fournissez, par ordre d'effet :

1. Votre nom, votre titre et une photo professionnelle.
2. Pour chaque résultat : le marché, la période, le périmètre (chiffre d'affaires de quoi, sur combien de temps) et, si possible, une personne qui peut le confirmer.
3. Un ou deux clients ou anciens employeurs que vous avez le droit de citer, avec leur accord écrit.

Tant que ces éléments ne sont pas fournis, laissez la formulation actuelle : elle est exacte et ne promet rien de plus. Ne mettez jamais un chiffre que vous ne pourriez pas justifier devant un prospect.

### 2.3 Les mentions légales

Un site professionnel en France doit afficher l'identité de son éditeur et de son hébergeur. Il n'existe pas encore de page de mentions dans le site : à vous de fournir la raison sociale, la forme juridique, le numéro d'immatriculation, l'adresse, un moyen de contact, le directeur de la publication et l'hébergeur. Ajoutez ensuite un lien « Mentions légales » dans le pied de page. Faites relire ce texte par la personne qui s'occupe de votre conformité.

## 3. Les engagements que la page prend en votre nom

La page décrit une méthode de travail. Chaque ligne ci-dessous est une promesse faite au visiteur : validez-la, ou demandez-moi de la reformuler.

| Ce que dit la page | Où | À valider |
|---|---|---|
| Un rendez-vous n'est compté que s'il passe cinq tests : cible, besoin exprimé, accord du prospect, présence dans l'agenda, contexte transmis avant l'échange | Section « Le rendez-vous qualifié », questions | Les cinq tests et leur ordre |
| Les contacts prospectés, les réponses et les comptes rendus appartiennent au client | Offres grands groupes, questions | Oui ou non, et jusqu'à quand |
| Le closing est conduit avec le client par un commercial senior | Accroche, méthode, comparaison | Qui, concrètement, tient ce rôle |
| Un interlocuteur unique et un rythme de compte rendu fixés au lancement | Offres | La fréquence des comptes rendus |
| Le calendrier de démarrage est fixé à l'issue de l'échange de 30 minutes | Questions, comparaison | Cohérent avec vos capacités |
| La proposition écrite suit l'échange | Appel final | Un délai que vous pouvez tenir |
| Aucun prix affiché | Questions | Garder ce choix ou afficher une fourchette |

La page ne promet aucun volume de rendez-vous, aucun taux de signature et aucun délai chiffré : ce choix vient du cadrage, parce qu'une garantie non étayée ne résiste pas à un prospect qui vérifie.

## 4. Mettre en ligne

Rien n'est fait à votre place : publier est un geste qui vous revient.

1. Renseignez `CONTACT_URL` (2.1), ajoutez vos mentions légales (2.3) et validez le tableau de la section 3.
2. Relisez la page entière sur un téléphone et sur un ordinateur.
3. Choisissez un hébergement statique. Votre compte Cloudflare Pages, déjà utilisé pour d'autres sites, convient : le dossier `L01-prosens` se dépose tel quel, avec `index.html` à sa racine. Tout hébergeur de fichiers statiques fonctionne.
4. Achetez ou choisissez le nom de domaine, puis rattachez-le à l'hébergement.
5. Ouvrez la page en ligne et vérifiez que chaque bouton d'échange ouvre bien votre agenda.

Point d'attention sur les données : les polices sont chargées depuis les serveurs de Google, ce qui transmet l'adresse IP du visiteur à Google. Pour l'éviter, hébergez les trois polices (Archivo, IBM Plex Sans, IBM Plex Mono) avec le site. Aucun autre service tiers n'est appelé.

## 5. Suivre les résultats

La page ne mesure rien. Après la mise en ligne, notez à la main ou avec l'outil de mesure de votre choix : le nombre de visites, le nombre de clics sur les boutons d'échange et le nombre d'échanges réservés. À titre de repère seulement, des sources commerciales situent les pages de demande d'appel entre 1,5 % et 4 % de conversion, et les services B2B autour de 2,6 % en moyenne. Ces chiffres ne sont pas une promesse et ne se comparent pas sans connaître la source du trafic.

## 6. Modifier la page

- **Textes** : tout le contenu est dans `index.html`, section par section, en français lisible.
- **Couleurs** : les huit couleurs sont déclarées une seule fois en haut du bloc de style (`--ink`, `--paper`, `--amber`, etc.).
- **Retirer une section** : chaque `<section>` est indépendante ; supprimez-la ainsi que son lien dans le menu.
- **Réduire les mouvements** : les visiteurs qui ont réglé leur appareil sur « réduire les animations » voient la page complète, sans aucun mouvement.

## 7. Ce qui a été vérifié

- Affichage de 375 à 1440 pixels : aucun défilement horizontal, aucune erreur dans la console.
- Contrastes de toutes les paires de couleurs de texte : au moins 5,6 pour 1.
- Navigation au clavier : boutons, onglets, questions et panneau d'échange atteignables.
- Mouvement réduit : aucune animation active, tout le contenu visible.
- Sans JavaScript : tout le contenu reste visible ; seuls les onglets, le visuel de la méthode et le panneau d'échange demandent JavaScript.

Limites : l'audit n'a pas mesuré la vitesse de chargement ni le référencement ; les polices s'affichent par défaut avec des polices système si Google est injoignable.

## 8. Pour aller plus loin (hors de cette mission)

- Une étude de cas réelle, avec chiffres et accord du client.
- Un formulaire de qualification relié à votre outil de gestion de contacts.
- Une page de mentions légales et une politique de confidentialité si vous ajoutez une mesure d'audience.
- Une version en anglais pour les grands groupes internationaux.
