# Format d'un rapport

La page « Veille YouTube » lit un seul bloc JSON : `<script id="data" type="application/json">{"sig":{…},"reports":[…]}</script>`. `scripts/rapport.py` y ajoute ou remplace un rapport. Exemple complet (sans miniatures) : `exemple-rapport-jev.json`.

```jsonc
{
  "id": "r8",              // laissé vide pour un nouveau rapport : rapport.py le numérote
  "name": "Higgsfield",    // nom dans la barre latérale
  "h1": "Higgsfield",      // titre de la page du rapport
  "date": "2026-10-28",    // date de la recherche
  "seq": 8,                // ordre des recherches du même jour (rapport.py le pose)
  "tags": ["Vidéo IA"],
  "src": "higgsfield, higgsfield avis, higgsfield vs",   // requêtes
  "note": "Dates approximatives… ; vidéos hors sujet écartées.",
  "method": "Ratio = vues / abonnés. Vues par mois = vues / (âge en jours / 30,4).",
  "approx": true,          // dates tirées de « il y a N … »
  "kpi": {                 // calculé par rapport.py s'il manque
    "n": 51, "nr": 8,      // vidéos retenues ; vidéos à 3 × ou plus
    "bv": {"t": "titre", "c": "chaîne", "v": 707986},        // la plus vue
    "br": {"c": "chaîne", "q": 25.5, "s": 336}                // le meilleur ratio
  },
  "synth":   {"angle": "html", "titles": [{"t": "", "w": ""}], "thumb": "html", "prompt": "texte",
              "struct": "A", "els": [{"o": 1, "el": ""}, {"o": 4, "el": "", "d": true}]},
  "why":     {"defs": "texte", "cards": [{"h": "1. …", "html": "<p><b>Constat.</b>…"}]},
  "pattern": {"formulas": [""], "checklist": [""], "examples": ["html"]},
  "rows": [
    {
      "i": "dQw4w9WgXcQ",  // id YouTube
      "t": "titre", "c": "chaîne",
      "d": "2026-07-29",   // date de publication (approximative si approx)
      "v": 8576,           // vues
      "s": 336,            // abonnés
      "u": 514,            // durée en secondes
      "a": 91,             // âge en jours
      "q": 25.5,           // ratio vues / abonnés
      "m": 2865.1,         // vues par mois
      "o": 1,              // rang
      "g": 1,              // 1 = top 15, 2 = le reste
      "n": false,          // récente (7 jours ou moins)
      "k": "ok",           // "nd" si une donnée manque (la ligne n'entre pas dans les meilleures)
      "r": "remarque",     // une phrase, voir analyse.md § 5
      "h": "data:image/jpeg;base64,…"   // miniature 320×180, posée par rapport.py
    }
  ]
}
```

Les champs `html` sont insérés tels quels : n'y mets que `<p>`, `<b>`, `<ul>`, `<li>`, et échappe les `<` littéraux.
