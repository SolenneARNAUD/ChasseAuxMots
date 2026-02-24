# Guide: Sélection de Personnage dans les Paramètres

## Vue d'ensemble

Une nouvelle page de sélection de personnage a été intégrée au menu des paramètres. Les joueurs peuvent maintenant choisir leur personnage jouable dans une interface dédiée avec affichage des sprites.

## Architecture

### 1. Nouvelle fonction: `fenetre_selection_personnages()`
**Fichier:** `Menu.py` (lignes 120-298)

Affiche une fenêtre de sélection des personnages organisée par catégories avec:
- **Grille 3x3** affichant les 3 personnages d'une catégorie
- **Sprites défaut** pour chaque personnage avec **nom en-dessous**
- **Navigation par catégories** avec flèches gauche/droite
- **Navigation au clavier** pour sélectionner un personnage dans la grille
- **Boutons Valider/Retour** pour confirmer ou annuler

#### Interactions:
- **Clic souris** sur un personnage pour le sélectionner
- **Flèches gauche/droite** pour changer de catégorie
- **Flèches haut/bas/gauche/droite** pour naviguer dans la grille
- **Entrée** pour confirmer la sélection
- **Échap** pour annuler (retourner au menu paramètres)

#### Retour:
- **ID du personnage sélectionné** (ex: "fallen_angels_1")
- **None** si l'utilisateur annule

### 2. Modifications: `fenetre_parametres()`
**Fichier:** `Menu.py` (lignes 300+)

**Nouveaux paramètres:**
- `personnage_actuel=None` - Personnage actuellement sélectionné

**Modifications:**
- Ajout bouton **"Personnage"** à côté des boutons Valider/Retour
- Clic ouverture fenêtre de selection avec `fenetre_selection_personnages()`
- Retour maintenant 5 valeurs au lieu de 4:
  ```python
  return (vitesse, reset_on_error, total_mots, bibliotheques, personnage_selectionne)
  ```

### 3. Modifications: `fenetre_niveau()`
**Fichier:** `Menu.py` (lignes 775+)

**Nouveaux paramètres:**
- `personnage_par_defaut=None` - Personnage par défaut à passer aux paramètres

**Modifications:**
- Variable locale `personnage_actuel` conserve la sélection
- Passe `personnage_par_defaut` à `fenetre_parametres()`
- Récupère le personnage sélectionné depuis les paramètres
- Retourne 6 valeurs au lieu de 5:
  ```python
  return (niveau, vitesse, reset_on_error, total_mots, bibliotheques, personnage)
  ```

### 4. Modifications: Boucle principale (`jeu.py`)
**Fichier:** `jeu.py` (lignes 535-550)

**Initialisation des variables:**
- Ajout `self.personnage_joueur = "fallen_angels_1"` dans `_initialiser_variables()`

**Appel fenetre_niveau:**
```python
resultat = Menu.Menu.fenetre_niveau(
    screen,
    ...,
    personnage_par_defaut=self.personnage_joueur
)

# Récupération du résultat avec personnage
self.niveau, self.vitesse_pourcentage, ... , self.personnage_joueur = resultat
```

### 5. Fonction utilitaire: `get_personnage_nom_affiche()`
**Fichier:** `BaseDonnees.py` (lignes 1962-1973)

Récupère le nom à afficher d'un personnage depuis la base de données.
```python
def get_personnage_nom_affiche(personnage_id):
    """Récupère le nom à afficher d'un personnage jouable."""
    config = get_personnage_jouable(personnage_id)
    if config:
        return config.get('nom_affiche', personnage_id.replace('_', ' ').title())
    return personnage_id.replace('_', ' ').title()
```

## Flux de données

```
Accueil
    ↓
Menu niveau
    ↓
[Bouton Paramètres cliqué]
    ↓
Menu paramètres
    ├─ Vitesse
    ├─ Reset on error
    ├─ Nombre de mots
    ├─ Bibliothèques
    └─ [Bouton PERSONNAGE] ← NOUVEAU
        ↓
    Sélection de personnage
        ├─ Affichage catégories
        ├─ Grille 3x3 sprites
        └─ Navigation
    (Retour sélection)
    ↓
[Valider paramètres]
    ↓
Lancement jeu avec personnage sélectionné
```

## Affichage visuel

### Fenêtre de sélection de personnage:

```
┌─────────────────────────────────────────┐
│       Selection du Personnage            │
│                                          │
│        < FALLEN_ANGELS >                 │
│                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ [SPRITE] │ │ [SPRITE] │ │ [SPRITE] │ │
│  │  Name 1  │ │  Name 2  │ │  Name 3  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ [SPRITE] │ │ [SPRITE] │ │ [SPRITE] │ │
│  │  Name 4  │ │  Name 5  │ │  Name 6  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ [SPRITE] │ │ [SPRITE] │ │ [SPRITE] │ │
│  │  Name 7  │ │  Name 8  │ │  Name 9  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│                                          │
│    [Valider]   [Retour]                  │
└─────────────────────────────────────────┘
```

Les personnages sélectionnés sont affichés avec une couleur bleue `COULEUR_BLEU_BOUTON`.

## Caractéristiques du personnage

Chaque personnage dispose de:
- **nom_affiche**: Nom à afficher dans l'interface
- **chemin_base**: Dossier de base des sprites
- **sprite_defaut**: Sprite par défaut pour affichage
- **hauteur**: Hauteur du personnage en pixels
- **animations**: 8 animations (idle, walking, running, slashing, dying, jump_loop, jump_start, hurt)

## Catégories de personnages

```
1. fallen_angels (3 variantes)
2. valkyrie (3 variantes)
3. goblin (1 variante)
4. ogre (1 variante)
5. orc (1 variante)
```

**Navigation:** Les flèches gauche/droite changent de catégorie et affichent les 3 personnages de cette catégorie.

## Sauvegarde et persistance

Le personnage sélectionné est:
1. Stocké dans `self.personnage_joueur` (jeu.py)
2. Passé en paramètre `personnage_par_defaut` aux appels suivants
3. Utilisé pour l'initialisation du joueur lors du lancement du niveau

## Notes de développement

- Le personnage par défaut est "fallen_angels_1"
- Tous les sprites sont redimensionnés pour tenir dans la grille
- Les proportions originales des sprites sont conservées
- La couleur d'arrière-plan par défaut est `Donnees.COULEUR_FOND`
- La couleur de sélection est `Donnees.COULEUR_BLEU_BOUTON`

## À faire (future amélioration)

- [ ] Afficher les statistiques du personnage (force, vitesse, etc.)
- [ ] Ajouter des miniatures d'animations au survol
- [ ] Permettre le tri/filtrage des categor ies
- [ ] Sauvegarder le dernier personnage sélectionné par joueur
