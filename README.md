# ChasseAuxMots

## Environnement (Windows)


```
setup_env.bat
```


```
setup_env.ps1
```


```
.venv\Scripts\activate
```


```
. .venv\Scripts\Activate.ps1
```

```markdown
# ChasseAuxMots

Petit jeu Python utilisant `pygame` — but pédagogique / prototype.

## Prérequis

- Python 3.8 ou supérieur installé (vérifier avec `python --version`).
- Sur Windows, il est recommandé d'installer la distribution officielle ou via le Microsoft Store.

## Installer les dépendances (Windows)

Le dépôt contient :

- `requirements.txt` — liste des paquets Python requis (actuellement `pygame`).
- `setup_env.bat` — script pour `cmd.exe` qui crée un virtualenv et installe les dépendances.
- `setup_env.ps1` — script PowerShell plus robuste pour créer/activer le virtualenv et installer les dépendances.

Exemples d'utilisation :

- Avec l'invite de commandes (cmd) — ouvre le dossier du projet, puis :

```cmd
cd C:\Users\PC\Documents\Projets\ChasseAuxMots\ChasseAuxMots
setup_env.bat
```

- Avec PowerShell — ouvre le dossier du projet, puis :

```powershell
Set-Location 'C:\Users\PC\Documents\Projets\ChasseAuxMots\ChasseAuxMots'
.\setup_env.ps1
```

Remarques :

- Les scripts créent un dossier `.venv` contenant l'environnement virtuel.
- `setup_env.ps1` vérifie si `.venv` existe, le crée si nécessaire, active l'environnement pour la session courante et installe les paquets.

## Activer l'environnement

- Dans `cmd.exe` :

```cmd
.venv\Scripts\activate
```

- Dans PowerShell :

```powershell
. .venv\Scripts\Activate.ps1
```

Après activation, l'invite affiche généralement le préfixe `(.venv)`.

## Lancer le jeu

Une fois l'environnement activé et les dépendances installées, lancez :

```powershell
python Jeu.py
```

ou

```cmd
python Jeu.py
```

## Mettre à jour les dépendances

Si vous ajoutez une nouvelle dépendance dans votre code :

```powershell
pip install <nouveau-paquet>
pip freeze > requirements.txt
```

Ainsi `requirements.txt` reste à jour pour d'autres postes.

## Résolution des problèmes courants

- Erreur lors de l'activation PowerShell (`Could not load module .venv`): assurez-vous d'exécuter la commande de dot-sourcing (avec un espace) :

```powershell
. .venv\Scripts\Activate.ps1
```

- Si PowerShell bloque l'exécution de scripts, exécutez (en tant qu'administrateur si nécessaire) :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

- Si `pygame` ne s'installe pas, vérifiez la version de Python et utilisez `pip` à jour :

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Remarques supplémentaires

- Le point d'entrée du jeu est `Jeu.py`.
- Les ressources (images) sont dans le dossier `images/`.
- Pour exécuter sur d'autres plateformes (Linux/macOS), créez un virtualenv équivalent et installez `requirements.txt`.

Si vous voulez, je peux :

- ajouter un script `run_game.bat` pour lancer directement `Jeu.py` depuis `cmd` ;
- préparer un fichier `pyproject.toml` ou `pipenv/poetry` si vous préférez un autre gestionnaire.

```
