# ChasseAuxMots

Jeu éducatif de frappe au clavier avec des dinosaures ! 🦖⌨️

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python jeu.py
```

## Configuration du chemin de sauvegarde

Par défaut, vos données de joueurs sont enregistrées dans le dossier TEMP de Windows :
```
C:\Users\VotreNom\AppData\Local\Temp\ChasseAuxMots\joueurs.csv
```

### Changer le dossier de sauvegarde

1. Ouvrez le fichier **`config.txt`** situé à côté du jeu
2. Modifiez le chemin vers le dossier de votre choix, par exemple :
   ```
   C:\Users\VotreNom\Documents\ChasseAuxMots
   ```
3. Enregistrez et relancez le jeu

**Note :** Le dossier TEMP est recommandé si vous avez des problèmes avec votre antivirus qui bloque la création de fichiers.

## Données sauvegardées

Le fichier `joueurs.csv` contient :
- Nom et prénom des joueurs
- Date d'inscription
- Nombre de parties jouées
- Statistiques (mots réussis, vitesse moyenne, erreurs)

Une copie de sauvegarde est automatiquement créée dans le dossier du jeu à la fermeture.
