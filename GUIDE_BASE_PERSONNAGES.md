# Base de Données des Personnages - Guide d'Utilisation

## 📋 Résumé

Une base de données complète des 9 personnages disponibles a été créée dans `BaseDonnees.py` avec toutes les informations d'animations et de configuration.


## 📊 Structure de Données

Chaque personnage contient :

```python
{
    "nom_affiche": "Nom à afficher",           # Nom lisible
    "chemin_base": "images/Personnages/...",  # Chemin de base
    "sprite_defaut": "chemin/vers/sprite",    # Image par défaut
    "hauteur": 120,                           # Hauteur en pixels
    "animations": {
        "animation_name": {
            "chemin_base": "chemin/animation",
            "nb_images": 18,                  # Nombre de frames
            "animation_delay": 5,             # Délai en ms entre les frames
            "format": "{:03d}.png"            # Format de numérotation
        }
    }
}
```

## 🎬 Animations Disponibles

Chaque personnage a les animations suivantes :

1. **idle** - État inactif (18 images)
2. **walking** - Marche (24 images)
3. **running** - Course (12 images)
4. **slashing** - Attaque au sabre (12 images)
5. **dying** - Mort (15 images)
6. **jump_loop** - Boucle de saut (6 images)
7. **jump_start** - Début du saut (6 images)
8. **hurt** - Blessé (6 images)

## 🔧 Fonctions Disponibles

### Récupérer la Liste des Personnages

```python
from BaseDonnees import lister_personnages_jouable

personnages = lister_personnages_jouable()
# Retourne: ['fallen_angels_1', 'fallen_angels_2', ..., 'valkyrie_3']
```

### Obtenir la Configuration Complète d'un Personnage

```python
from BaseDonnees import get_personnage_jouable

config = get_personnage_jouable('fallen_angels_1')
# Retourne le dictionnaire complet du personnage
```

### Récupérer le Sprite Par Défaut

```python
from BaseDonnees import get_personnage_sprite_defaut_jouable

sprite_path = get_personnage_sprite_defaut_jouable('goblin')
# Retourne: 'images/Personnages/Goblin/PNG/PNG Sequences/Idle/0_Goblin_Idle_000.png'
```

### Obtenir la Hauteur d'un Personnage

```python
from BaseDonnees import get_personnage_hauteur_jouable

hauteur = get_personnage_hauteur_jouable('ogre')
# Retourne: 150 (en pixels)
```

### Lister les Animations d'un Personnage

```python
from BaseDonnees import get_animations_personnage_jouable

animations = get_animations_personnage_jouable('valkyrie_1')
# Retourne: ['dying', 'hurt', 'idle', 'jump_loop', 'jump_start', 'running', 'slashing', 'walking']
```

### Obtenir les Chemins des Frames d'une Animation

```python
from BaseDonnees import get_animation_frames_jouable

frames = get_animation_frames_jouable('fallen_angels_1', 'idle')
# Retourne une liste de 18 chemins d'images
# Exemple: ['images/Personnages/Fallen_Angels_1/.../0_Fallen_Angels_Idle_000.png', ...]
```

### Obtenir les Informations Complètes d'une Animation

```python
from BaseDonnees import get_animation_info_jouable

info = get_animation_info_jouable('orc', 'running')
# Retourne:
# {
#     'frames': [...],           # Liste des 12 frames
#     'nb_images': 12,          # Nombre de frames
#     'animation_delay': 5,     # Délai entre frames (ms)
#     'chemin_base': 'images/Personnages/Orc/PNG/PNG Sequences/Running/0_Orc_Running_',
#     'format': '{:03d}.png'
# }
```

### Obtenir le Nom d'Affichage d'un Personnage

```python
from BaseDonnees import get_personnage_nom_affiche

nom = get_personnage_nom_affiche('fallen_angels_1')
# Retourne: 'Fallen Angels 1'
```

### Grouper les Personnages par Catégorie

```python
from BaseDonnees import get_personnages_jouables_par_categorie

categories = get_personnages_jouables_par_categorie()
# Retourne:
# {
#     'fallen_angels': ['fallen_angels_1', 'fallen_angels_2', 'fallen_angels_3'],
#     'goblin': ['goblin'],
#     'ogre': ['ogre'],
#     'orc': ['orc'],
#     'valkyrie': ['valkyrie_1', 'valkyrie_2', 'valkyrie_3']
# }
```

## 📝 Exemples d'Utilisation

### Exemple 1 : Charger et Afficher Tous les Personnages

```python
from BaseDonnees import lister_personnages_jouable, get_personnage_nom_affiche, get_personnage_hauteur_jouable

for pers_id in lister_personnages_jouable():
    nom = get_personnage_nom_affiche(pers_id)
    hauteur = get_personnage_hauteur_jouable(pers_id)
    print(f"- {nom} ({pers_id}) - Hauteur: {hauteur}px")
```

### Exemple 2 : Créer un Menu de Sélection

```python
from BaseDonnees import get_personnages_jouables_par_categorie

categories = get_personnages_jouables_par_categorie()
for categorie, personnages in categories.items():
    print(f"\n{categorie.upper()}:")
    for i, pers_id in enumerate(personnages, 1):
        print(f"  {i}. {pers_id}")
```

### Exemple 3 : Obtenir Toutes les Animations d'un Personnage

```python
from BaseDonnees import get_animations_personnage_jouable, get_animation_info_jouable

pers_id = 'valkyrie_1'
for anim_name in get_animations_personnage_jouable(pers_id):
    info = get_animation_info_jouable(pers_id, anim_name)
    print(f"{anim_name}: {info['nb_images']} frames @ {info['animation_delay']}ms")
```

## 🎯 Points Importants

- **Format des images** : `{:03d}.png` signifie numérotation sur 3 chiffres avec zéros (000, 001, 002, ...)
- **Animation delay** : Temps en millisecondes entre l'affichage de chaque frame
- **Chemin base** : Ajoutez le format au chemin base pour obtenir le chemin complet
- **resource_path()** : Tous les chemins sont automatiquement passés à `resource_path()` pour la compatibilité .exe

## 📦 Données de la Base

**Total : 9 personnages**
- **Total d'animations par personnage** : 8 animations
- **Total de frames** : Entre 6 et 24 selon l'animation
- **Hauteurs de personnages** : Varient de 100px (Goblin) à 150px (Ogre)

---

**Créé le** : 24 février 2026
**Version** : 1.0
