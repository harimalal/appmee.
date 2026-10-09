# Déclic — plateforme de gestion pour Claire RTH

Site public + portail cliente + back-office, générés depuis le document « BusinessFlow Pro — Structuration Guidée Solopreneur ».
Aucun build : fichiers statiques (Cloudflare Pages, racine = `declic/`).

## Pages
- `index.html` — site public, quiz diagnostic → création automatique de l'espace cliente
- `app.html` — connexion ; routes `#/me/...` (cliente) et `#/admin/...` (Claire)
- `legal.html` — mentions légales, CGV, RGPD (alimentées par Réglages)

## Ce qui est automatisé
Parcours en 5 étapes (Je me découvre → Je choisis → Je démarre → Je me transforme → J'ai ancré → Et maintenant).
Chaque case cochée : débloque les ressources, programme les emails (séquence de bienvenue J0→J+10, relances proposition J+2/J+5,
compte-rendu de séance…), crée les factures, génère proposition/contrat/feuille de route/kit de recommandation, et fait avancer d'étape.
Claire n'a que les actions humaines : relire un dossier, « appel fait → proposer », « séance réalisée » (écran **À faire**).
Les 39 templates du document sont dans **Mise en route** (30 gérés automatiquement) et **Bibliothèque** (18 textes complets).

## Démo
Ouvrir `app.html` → « Entrer comme Claire » (charge des clientes de démo). Compte coach : `claire@declic.fr` / `declic2026` (à changer).

## Limites du mode démo (à lire avant d'ouvrir au public)
- Données dans le navigateur (localStorage) : une cliente ne voit pas son espace depuis un autre appareil.
- Authentification côté client : pas sécurisée. Passer sur Supabase (`supabase/schema.sql`, RLS inclus) en remplaçant `js/store.js`.
- Emails simulés : renseigner un webhook (Zapier/Make/Worker) dans Réglages → Emails pour l'envoi réel.
- Paiement simulé : coller des liens Stripe Payment Links dans Réglages ; Claire confirme alors la réception en un clic.
- Contrat et pages légales = modèles à faire relire par un juriste. Le texte du document prévoit « 3 × 450 € » pour DÉCLIC (1 350 €) contre 1 200 € comptant : à confirmer.
