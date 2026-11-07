# Rolit — Jeu de plateau en Python

> Adaptation informatique du jeu de société Rolit sur plateau $8\times8$, développée dans le cadre du projet universitaire 2024-2025 à l'Université Gustave Eiffel.

---

## Présentation du Projet

Rolit est un jeu de stratégie au tour par tour. L'objectif est d'encercler les pions adverses pour les retourner à votre couleur et posséder le plus grand nombre de cases en fin de partie.

### Fonctionnalités Principales
- **Multijoueur (2 à 4 joueurs) :** Configuration personnalisée des pseudonymes et des identifiants.
- **Symboles sur mesure :** Pions représentés par un cercle, un cœur, une fleur ou un diamant.
- **Variante Bonus & Malus :** Cases étoiles pour rejouer et têtes de mort avec pénalités.
- **Moteur de jeu complet :** Prise en compte du mode de capture obligatoire.
- **Système de manches :** Cumul et comptage des scores sur plusieurs parties.
- **Sauvegarde dynamique :** Interruption et reprise de partie grâce au stockage JSON.

---

## Stack Technique

- **Langage :** Python 3
- **Interface Graphique :** `fltk.py`
- **Format de Sauvegarde :** Fichiers JSON (`sauvegarde.json`)

---

## Installation et Lancement

1. **Cloner le projet :**
   ```bash
   git clone [https://github.com/VOTRE_PSEUDO/rolit-python.git](https://github.com/VOTRE_PSEUDO/rolit-python.git)
   cd rolit-python
