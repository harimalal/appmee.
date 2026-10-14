// Version courte (≈ 60 s) : morceaux du film long, en secondes de scene.html, joués à une vitesse donnée.
// [début, fin, vitesse, 'net' facultatif = coupe franche au lieu du fondu enchaîné]
// Vitesses utiles : 1 pour l'accroche, 1,3 à 1,8 pour la démo, 2 au plus. Couper entre deux légendes, jamais au milieu.
// Vérifier : node <skill>/scripts/montage.cjs montage-60s.cjs
module.exports = {
  SEG: [
    [0, 2.8, 1.0],      // accroche
    [2.8, 10.6, 1.3],   // problème
    [10.6, 13.6, 1.1],  // révélation du logo
    [13.6, 18.4, 1.4],  // promesse
    [18.4, 24.9, 1.7],  // 01 …
    // [49.1, 54.5, 1.5, 'net'],  // exemple de coupe franche (cadrages trop différents pour un fondu)
    [79.4, 84.75, 1.5], // récapitulatif, premier gros plan
    [93.0, 95.9, 1.2],  // phrase de synthèse
    [95.9, 100, 1.15],  // fin, ralentie pour laisser finir la voix
  ],
  // Consigne de ton passée en tête du texte envoyé à ElevenLabs (non prononcée).
  TON: '[calm, warm, confident]',
  // Ce que la voix doit prononcer autrement qu'à l'écrit (le sous-titre garde l'écrit).
  DIT: { '80/20': 'eighty-twenty' },
  // Répliques : [instant de la scène où la réplique commence au plus tôt, texte]. ≈ 2,3 mots par seconde en voix posée.
  VOIX: [
    [0.35, 'The goal. Where do you even start?'],
    [3.3, 'Spreadsheets. Inboxes. Five different apps… and still no plan.'],
    [11.4, 'Meet <App>.'],
    [13.7, 'Not another all-in-one app. <The promise of the landing>.'],
    [18.8, '<Feature 01, said as a benefit>.'],
    [80.2, '<Recap line>.'],
    [93.2, '<Synthesis line>.'],
    [96.3, '<Slogan of the landing>.'],
  ],
};
