# AppMétier Platform — Guide de déploiement Cloudflare Pages

## Structure des fichiers

```
appmetier-platform/
├── index.html          ← Page de connexion / inscription
├── dashboard.html      ← Dashboard (protégé, redirige si non connecté)
├── _headers            ← En-têtes de sécurité HTTP (Cloudflare Pages)
├── _redirects          ← Routage Cloudflare Pages
├── css/
│   ├── tokens.css      ← Design tokens partagés (charte AppMétier)
│   ├── auth.css        ← Styles page authentification
│   └── dashboard.css   ← Styles dashboard
└── js/
    ├── auth.js         ← Module auth (login, register, session, validation)
    └── dashboard.js    ← Module dashboard (apps, abonnements, profil)
```

---

## Déploiement Cloudflare Pages

### Méthode 1 — Drag & Drop (immédiat)

1. Allez sur dash.cloudflare.com
2. Workers & Pages → Create → Pages → Upload assets
3. Glissez-déposez le dossier `appmetier-platform/` entier
4. Nom du projet : `appmetier`
5. Cliquez "Deploy site"

URL automatique : `https://appmetier.pages.dev`

### Méthode 2 — Via GitHub (recommandée, mises à jour automatiques)

1. Créez un dépôt GitHub avec le contenu de ce dossier
2. Cloudflare Pages → Create → Connect to Git
3. Sélectionnez votre dépôt
4. Framework preset : None
5. Build command : (vide)
6. Build output : /
7. Deploy

Chaque `git push` redéploie automatiquement → tous vos clients ont la mise à jour en quelques secondes.

### Domaine personnalisé

Pages → Custom domains → Set up a custom domain
→ Entrez `app.votredomaine.fr`
→ Ajoutez l'enregistrement CNAME chez votre registrar

---

## Ajouter l'application Facturation

Copiez le dossier `elinea/` dans `apps/facturation/` :

```
appmetier-platform/
└── apps/
    └── facturation/
        ├── index.html
        ├── css/style.css
        └── js/app.js
```

Le lien dans `dashboard.js` est déjà configuré :
```js
url: 'apps/facturation/index.html',
```

---

## Ajouter une nouvelle application au catalogue

Dans `js/dashboard.js`, ajoutez un objet dans le tableau `APPS` :

```js
{
  id:       'mon-app',          // identifiant unique, sans espace
  label:    'MON APP',          // affiché en grand sur la vignette
  category: 'Ma catégorie',     // affiché en petit au-dessus
  desc:     'Description courte de l\'application.',
  url:      'apps/mon-app/index.html',
  features: ['Fonctionnalité 1', 'Fonctionnalité 2', 'Fonctionnalité 3'],
},
```

---

## Migration vers Supabase (production)

### Auth
Dans `js/auth.js`, remplacez `_apiLogin` et `_apiRegister` :

```js
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Login
const { data, error } = await supabase.auth.signInWithPassword({ email, password })

// Register
const { data, error } = await supabase.auth.signUp({
  email, password,
  options: { data: { prenom, nom } }
})
```

### Abonnements
Dans `js/dashboard.js`, remplacez `getSubs()` et `saveSubs()` :

```js
// Lire les abonnements
const { data } = await supabase
  .from('subscriptions')
  .select('*')
  .eq('user_id', currentUser.id)

// Activer un abonnement (via webhook Stripe)
// → Cloudflare Worker reçoit le webhook Stripe
// → Insère dans la table subscriptions
```

### Intégration Stripe
Dans `handleSubscribe()`, remplacez `_mockSubscribe()` :

```js
// Redirection vers Stripe Checkout
window.location.href = `/api/checkout?app=${appId}&user=${currentUser.id}`
```

---

## Sécurité

- HTTPS : automatique sur Cloudflare ✓
- En-têtes HTTP : configurés dans `_headers` (CSP, HSTS, X-Frame-Options…) ✓
- XSS : toutes les données utilisateur sont échappées via `esc()` ✓
- Auth : `requireAuth()` redirige vers `index.html` si session absente ou expirée ✓
- Sessions : expiration 7 jours (configurable dans `CFG.TTL` dans `auth.js`) ✓
- Mots de passe : hashés SHA-256 côté client en mode démo — déléguer à Supabase en prod ✓

---

## Variables à personnaliser

| Fichier | Variable | Description |
|---------|----------|-------------|
| `js/auth.js` | `CFG.DASHBOARD_URL` | URL du dashboard après connexion |
| `js/auth.js` | `CFG.TTL` | Durée de session (ms) |
| `js/auth.js` | `CFG.SESSION_KEY` | Clé localStorage de session |
| `js/dashboard.js` | `APPS` | Catalogue des applications |
