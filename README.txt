########################################################
# Game Fan−attic propose Rolit (édité par Goliath)     #
# Développé par ZenDev − décembre 2024                 #
# Version 3 distribuée sous licence BiduleChose        #
########################################################

========================================================
Guide utilisateur :
========================================================

# --------- Pré-requis ---------
- Python 3 doit être installé sur la machine.
- La bibliothèque FLTK est incluse dans l'archive.

# --------- Installation ---------
1. Décompressez l'archive `Rolit_Project.zip`.
2. Assurez-vous que le dossier `code` contient :
   -  Le fichier principal : `projet_fltk_raccourci.py`
   -  Les fichiers des classes : `classe_cercle.py`, `classe_coeur.py`, `classe_fleur.py`, `classe_diamant.py`
   -  Le dossier `Images/` contenant toutes les images nécessaires au programme.
   -  Le fichier `sauvegarde.json` pour enregistrer l'état du jeu.
   -  Le fichier `fltk.py` contenant la bibliothèque graphique.

# --------- Exécution ---------
1. Ouvrez un terminal.
2. Placez-vous dans le répertoire où se trouve le fichier `projet_fltk_raccourci.py`
3. Lancez le programme avec la commande suivante :
   > python projet_fltk_raccourci.py

# --------- Règles du jeu ---------
1. Le jeu se déroule sur un plateau de 8x8 cases.
2. Chaque joueur choisit un symbole (●, ♥, ✿, ⬖) au début.
3. Le but est de capturer le plus de cases possibles en retournant les pièces adverses.
4. Modes de jeu disponibles:
   - Les bonus et malus :
   	- Bonus (sous forme d'étoile) : Vous rejouez immédiatement.
   	- Malus (sous forme de tête de mort) : Vous perdez un pion ou passez votre prochain 	tour.
   - Capture obligatoire :
   	- Si un coup permet une capture, il est obligatoire de le jouer.
6. Fin de partie :
   - La partie se termine lorsque toutes les cases du plateau sont occupées.
   - Le joueur avec le plus de points gagne.

========================================================
Notes pour les développeurs :
========================================================

# --------- Structure des répertoires ---------
- Le répertoire `Code/` contient :
  - `PROJET__fltk_racourcci.py` : Fichier principal du programme.
  - `classe_cercle.py` : Classe pour le symbole cercle.
  - `classe_coeur.py` : Classe pour le symbole cœur.
  - `classe_fleur.py` : Classe pour le symbole fleur.
  - `classe_diamant.py` : Classe pour le symbole diamant.
  - `fltk/` : Bibliothèque pour l'interface graphique.
  - `Images/` : Contient les ressources graphiques nécessaires au jeu.
  - `sauvegarde.json` : Fichier pour enregistrer et restaurer l'état du jeu.

# --------- Bugs connus ---------
- Aucun bug majeur détecté pour le moment.
- Si un bug est rencontré, merci de le signaler à l'équipe ZenDev.

========================================================
Merci d'avoir choisi Game Fan-attic pour vos moments de détente !
========================================================
