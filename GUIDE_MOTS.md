# Guide de gestion des mots - ChasseAuxMots

## Fichier de mots : mots.json

Le jeu charge maintenant tous les mots depuis le fichier `mots.json` qui est organisé en **bibliothèques thématiques**.

### Structure du fichier

Le fichier contient les lettres et des bibliothèques de mots par thème :

```json
{
    "lettres": [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "à", "é", "è", "ù", "ç", "ê", "ü"
    ],
    "bibliotheques": {
        "dinosaure": {
            "nom": "Préhistoire & Dinosaures",
            "description": "Mots sur les dinosaures...",
            "mots": ["os", "raptor", "volcan", "un T-Rex géant", ...]
        },
        "moyen_age": {
            "nom": "Moyen Âge",
            "description": "Mots sur le monde médiéval...",
            "mots": ["roi", "château", "chevalier", "une épée tranchante", ...]
        }
    }
}
```

### Bibliothèques disponibles

#### 1. **dinosaure** (par défaut)
- **Nom complet** : Préhistoire & Dinosaures
- **265 mots** sur les dinosaures, la préhistoire et la nature primitive
- Exemples : os, raptor, volcan, mammouth, un T-Rex géant, une forêt dense

#### 2. **moyen_age**
- **Nom complet** : Moyen Âge
- **85 mots** sur le monde médiéval, les chevaliers et les châteaux
- Exemples : roi, château, chevalier, armure, une épée tranchante, un château fort

### Tri automatique par niveau

Les mots (lettres + bibliothèque active) sont automatiquement triés au démarrage :

- **Niveau 1** : Un seul caractère (les lettres)
  - Exemples : `a`, `b`, `é`, `ç`
  
- **Niveau 2** : Mots de moins de 5 lettres SANS caractères spéciaux
  - Exemples dinosaure : `os`, `lac`, `nid`
  - Exemples moyen_age : `roi`, `arc`, `duc`
  
- **Niveau 3** : Mots d'au moins 5 lettres OU mots avec caractères spéciaux
  - Exemples dinosaure : `arbre`, `forêt`, `île`
  - Exemples moyen_age : `château`, `chevalier`, `épée`
  
- **Niveau 4** : Identique au niveau 3 (mêmes mots)
  
- **Niveau 5** : Groupes nominaux (expressions contenant des espaces)
  - Exemples dinosaure : `un os`, `une forêt dense`, `un T-Rex géant`
  - Exemples moyen_age : `un roi`, `une épée tranchante`, `un château fort`

### Comment créer une nouvelle bibliothèque

1. Ouvrez le fichier `mots.json`
2. Ajoutez une nouvelle entrée dans `"bibliotheques"` avec :
   - Un **id** unique (nom technique, sans espaces, ex: `ma_bibliotheque`)
   - Un **nom** d'affichage
   - Une **description** courte
   - Une liste de **mots**

**Exemple d'ajout de bibliothèque "espace" :**
```json
{
    "lettres": [...],
    "bibliotheques": {
        "dinosaure": {...},
        "moyen_age": {...},
        "espace": {
            "nom": "Exploration Spatiale",
            "description": "Mots sur l'espace, les planètes et les étoiles",
            "mots": [
                "Mars", "lune", "étoile", "comète", "fusée",
                "planète", "satellite", "astronaute", "galaxie",
                "une étoile filante", "un trou noir", "la Voie lactée"
            ]
        }
    }
}
```

### Comment changer de bibliothèque (dans le code)

Pour utiliser une bibliothèque différente, modifiez la variable dans `BaseDonnees.py` :

```python
# Dans BaseDonnees.py, ligne ~100
BIBLIOTHEQUE_ACTIVE = "moyen_age"  # Au lieu de "dinosaure"
```

Ou utilisez la fonction :
```python
import BaseDonnees
BaseDonnees.set_bibliotheque_active("moyen_age")
```

### Lister les bibliothèques disponibles (dans le code)

```python
import BaseDonnees
bibliotheques = BaseDonnees.lister_bibliotheques()
for biblio in bibliotheques:
    print(f"{biblio['id']}: {biblio['nom']} - {biblio['nb_mots']} mots")
```

### Distribution actuelle (bibliothèque dinosaure)

- Niveau 1 : 59 caractères
- Niveau 2 : 38 mots
- Niveau 3 : 135 mots  
- Niveau 4 : 135 mots
- Niveau 5 : 92 groupes nominaux

**Total : 324 mots** (59 lettres + 265 mots dinosaure)

### Distribution bibliothèque moyen_age

- Niveau 1 : 59 caractères
- Niveau 2 : 18 mots
- Niveau 3 : 37 mots  
- Niveau 4 : 37 mots
- Niveau 5 : 30 groupes nominaux

**Total : 144 mots** (59 lettres + 85 mots moyen_age)

### Notes importantes

- Les **lettres** sont partagées par toutes les bibliothèques (toujours en niveau 1)
- Chaque bibliothèque peut avoir des mots différents pour les niveaux 2-5
- Le fichier doit être au format JSON valide
- Les mots avec espaces seront toujours dans le niveau 5
- Les caractères spéciaux (accents) rendent un mot plus difficile → niveau 3 minimum
