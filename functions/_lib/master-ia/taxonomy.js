// Taxonomie fixe : Claude choisit dans cette liste, ce qui garde les catégories stables d'une ressource à l'autre.

export const CATEGORIES = [
  'Fondamentaux IA & Machine Learning',
  'Deep Learning & réseaux de neurones',
  'LLM & IA générative',
  'Prompt engineering & agents',
  'RAG, données & bases vectorielles',
  'NLP & vision par ordinateur',
  'MLOps & mise en production',
  'Mathématiques & statistiques pour l\'IA',
  'Python & outils data',
  'IA appliquée métier & automatisation',
  'Éthique, régulation & sécurité de l\'IA',
  'Veille, actualités & recherche',
  'Carrière & certifications',
  'Autre',
];

export const TYPES = ['video', 'playlist', 'cours', 'article', 'documentation', 'podcast', 'livre', 'outil', 'autre'];
export const LEVELS = ['debutant', 'intermediaire', 'avance', 'tous'];
export const LANGS = ['fr', 'en', 'autre'];
export const STATUSES = ['a_voir', 'en_cours', 'termine', 'abandonne'];

export const SOURCES = {
  youtube: { label: 'YouTube', domains: ['youtube.com', 'youtu.be'] },
  udemy: { label: 'Udemy', domains: ['udemy.com'] },
  coursera: { label: 'Coursera', domains: ['coursera.org'] },
  openclassrooms: { label: 'OpenClassrooms', domains: ['openclassrooms.com'] },
  web: { label: 'Site web', domains: [] },
};

export const DEFAULT_PROFILE = `Je prépare un Master en intelligence artificielle.
Objectifs : maîtriser les fondamentaux (ML, deep learning, maths), comprendre et construire des applications LLM / RAG / agents, savoir déployer en production, et rester à jour sur la recherche.
Je lis le français et l'anglais. Je préfère les ressources rigoureuses, pratiques (code, projets) et récentes à la vulgarisation superficielle.`;
