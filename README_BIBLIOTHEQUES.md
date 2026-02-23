# Système de Bibliothèques - ChasseAuxMots

## 🎯 Qu'est-ce qu'une bibliothèque ?

Une **bibliothèque** est un ensemble de mots sur une même thématique (dinosaures, moyen âge, animaux, espace, etc.). Cela permet de varier les parties en fonction du sujet que vous souhaitez travailler.

## 📚 Bibliothèques disponibles

### 1. **dinosaure** (par défaut)
- Thème : Préhistoire & Dinosaures
- 265 mots sur les dinosaures et la nature primitive
- Utilisée automatiquement au lancement

### 2. **moyen_age**
- Thème : Moyen Âge
- 85 mots sur les chevaliers, châteaux et l'époque médiévale

## 🔄 Comment changer de bibliothèque

### Méthode 1 : Modifier le code (permanent)

Ouvrez `BaseDonnees.py` et modifiez la ligne ~100 :

```python
# Bibliothèque active par défaut
BIBLIOTHEQUE_ACTIVE = "moyen_age"  # Au lieu de "dinosaure"
```

Sauvegardez et relancez le jeu.

### Méthode 2 : Depuis Python (temporaire)

```python
import BaseDonnees
BaseDonnees.set_bibliotheque_active("moyen_age")
```

## ➕ Comment créer une nouvelle bibliothèque

### Étape 1 : Créer la structure dans mots.json

Ouvrez `mots.json` et ajoutez votre bibliothèque dans la section `"bibliotheques"` :

```json
{
    "lettres": [...],
    "bibliotheques": {
        "dinosaure": {...},
        "moyen_age": {...},
        
        "votre_bibliotheque": {
            "nom": "Nom d'affichage",
            "description": "Description de votre thème",
            "mots": [
                "mot1", "mot2", "mot3",
                "groupe nominal 1",
                "groupe nominal 2"
            ]
        }
    }
}
```

### Étape 2 : Activer votre bibliothèque

Dans `BaseDonnees.py` :
```python
BIBLIOTHEQUE_ACTIVE = "votre_bibliotheque"
```

### Conseils pour créer vos mots :

- **Niveau 1** : Géré automatiquement (lettres)
- **Niveau 2** : Mots courts (< 5 lettres) sans accents → `roi`, `arc`, `lac`
- **Niveau 3** : Mots longs (≥ 5 lettres) OU avec accents → `château`, `forêt`, `île`
- **Niveau 4** : Identique au niveau 3 automatiquement
- **Niveau 5** : Groupes nominaux (avec espaces) → `un roi brave`, `le château fort`

## 📖 Exemples de bibliothèques

Consultez le fichier `exemple_bibliotheque.json` pour des exemples complets de bibliothèques sur :
- Les animaux
- L'océan
- Les sciences

Vous pouvez copier ces exemples directement dans `mots.json` !

## 🔍 Lister les bibliothèques disponibles

Dans un script Python :

```python
import BaseDonnees

bibliotheques = BaseDonnees.lister_bibliotheques()
for biblio in bibliotheques:
    print(f"{biblio['id']}: {biblio['nom']}")
    print(f"   {biblio['description']}")
    print(f"   {biblio['nb_mots']} mots\n")
```

## 📊 Statistiques actuelles

**Bibliothèque dinosaure :**
- 59 lettres (niveau 1)
- 38 mots courts (niveau 2)
- 135 mots longs (niveaux 3-4)
- 92 groupes nominaux (niveau 5)
- **Total : 324 mots**

**Bibliothèque moyen_age :**
- 59 lettres (niveau 1)
- 18 mots courts (niveau 2)
- 37 mots longs (niveaux 3-4)
- 30 groupes nominaux (niveau 5)
- **Total : 144 mots**

## 💡 Idées de bibliothèques

- 🦁 Animaux (safari, jungle, ferme)
- 🌊 Océan & vie marine
- 🚀 Espace & astronomie
- 🏙️ Ville & métiers
- 🌳 Nature & environnement
- 🎨 Arts & couleurs
- 🍕 Nourriture
- 🏃 Sports
- 🎭 Émotions & sentiments
- 📚 École & éducation
- 🌍 Géographie & pays
- ⚗️ Sciences

## 📝 Fichiers importants

- `mots.json` : Fichier contenant toutes les bibliothèques
- `BaseDonnees.py` : Code de chargement des bibliothèques
- `GUIDE_MOTS.md` : Guide détaillé sur la gestion des mots
- `exemple_bibliotheque.json` : Modèles et exemples de bibliothèques
- `test_bibliotheques.py` : Script pour tester les bibliothèques

---

**Besoin d'aide ?** Consultez `GUIDE_MOTS.md` pour plus de détails !
