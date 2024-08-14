# Changelog
Tous les changements notables apportés au projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2023-08-14

### Ajouté
- Système de logging pour une meilleure traçabilité des opérations et des erreurs.
- Support des arguments en ligne de commande avec argparse.
- Documentation initiale avec ce fichier CHANGELOG.md.

### Modifié
- Optimisation des requêtes à la base de données pour de meilleures performances.
- Amélioration de la gestion des erreurs avec des messages de log plus détaillés.
- Restructuration du code pour une meilleure lisibilité et maintenance.

### Corrigé
- Gestion améliorée des slugs uniques pour éviter les conflits de noms de pages.

## [1.0.0] - 2023-08-13

### Ajouté
- Fonctionnalité de base pour générer des pages TYPO3 à partir de thèmes Wikipedia.
- Connexion directe à la base de données TYPO3 pour créer des pages et du contenu.
- Génération de titres de pages basés sur des modèles prédéfinis.
- Support multi-langues pour la création de contenu.

### Notes
- Version initiale du script avec les fonctionnalités de base pour la génération de pages TYPO3.
