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
C:\Users\VotreNom\AppData\Local\Temp\ChasseAuxMots\joueurs.json
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

Le fichier `joueurs.json` contient pour chaque joueur :
- Nom et prénom
- Date d'inscription
- Historique complet par monde et par niveau

Pour chaque essai de jeu, les informations suivantes sont enregistrées :
- Liste détaillée des erreurs (mot, lettre attendue, lettre tapée)
- Vitesse de frappe (mots/minute)
- Vitesse de défilement du sol
- Option "Reset mots" activée ou non
- Score (nombre de mots réussis)
- Date et heure de l'essai

Une copie de sauvegarde est automatiquement créée dans le dossier du jeu à la fermeture.
