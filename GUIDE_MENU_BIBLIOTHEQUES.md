# Guide d'utilisation - Menu de sélection de bibliothèque

## 📚 Comment changer de bibliothèque dans le jeu

### Étape 1 : Accéder aux paramètres

1. Lancez le jeu avec `python jeu.py`
2. Sélectionnez votre personnage et votre monde
3. Dans l'écran de sélection de niveau, cliquez sur le bouton **"Paramètres"** (en bas à gauche)

### Étape 2 : Sélectionner une bibliothèque

Dans le menu Paramètres, vous verrez maintenant **4 paramètres** :

1. **Vitesse de défilement** (input numérique)
2. **Reset du mot après erreur** (case à cocher)
3. **Nombre de mots par partie** (input numérique)
4. **Bibliothèque** (liste scrollable) ← NOUVEAU !

#### Utiliser le sélecteur de bibliothèque :

- **Voir les bibliothèques** : Toutes les bibliothèques disponibles sont listées
- **Sélectionner** : Cliquez sur le carré à gauche du nom de la bibliothèque souhaitée
- **Scroll** : S'il y a plus de bibliothèques que d'espace disponible :
  - Utilisez la **molette de la souris** pour descendre/monter dans la liste
  - Un indicateur affiche `(1-2/3)` = bibliothèques visibles / total

- **Bibliothèque active** : Le carré contient un carré vert plein

### Étape 3 : Valider

1. Cliquez sur **"Valider"** pour appliquer vos changements
2. Ou cliquez sur **"Retour"** pour annuler

### Exemple visuel

```
┌─────────────────────────────────────────┐
│            Paramètres                    │
├─────────────────────────────────────────┤
│                                          │
│  Vitesse de défilement      [100 %]     │
│                                          │
│  Reset du mot après erreur  [✓]         │
│                                          │
│  Nombre de mots par partie  [20]        │
│                                          │
│  Bibliothèque:              (1-2/2)     │
│    [■] Préhistoire & Dinosaures         │
│    [ ] Moyen Âge                        │
│                                          │
├─────────────────────────────────────────┤
│     [Valider]     [Retour]              │
└─────────────────────────────────────────┘
```

**Légende :**
- `[■]` = Bibliothèque sélectionnée (carré avec un carré vert plein)
- `[ ]` = Bibliothèque non sélectionnée (carré vide)
- `(1-2/2)` = On voit les bibliothèques 1 à 2 sur un total de 2

## 🎮 Utilisation dans le jeu

Une fois la bibliothèque sélectionnée :

1. Les mots de la partie seront tirés de cette bibliothèque
2. Le changement reste actif pour toutes les parties suivantes
3. Vous pouvez changer de bibliothèque à tout moment via les paramètres

## 📊 Bibliothèques disponibles

### Préhistoire & Dinosaures (par défaut)
- **265 mots** sur les dinosaures et la préhistoire
- Exemples : raptor, volcan, mammouth, un T-Rex géant

### Moyen Âge
- **85 mots** sur le monde médiéval
- Exemples : roi, château, chevalier, une épée tranchante

## 🔧 Pour les développeurs

### Ajouter une nouvelle bibliothèque

Consultez [README_BIBLIOTHEQUES.md](README_BIBLIOTHEQUES.md) pour apprendre à :
- Créer une nouvelle bibliothèque dans `mots.json`
- Ajouter vos propres thèmes (animaux, espace, nature, etc.)

### Tester le menu

Utilisez le script de test :
```bash
python test_menu_bibliotheques.py
```

## ⚙️ Paramètres techniques

- **Scroll** : Molette de la souris (boutons 4 et 5)
- **Affichage** : Adaptatif selon le nombre de bibliothèques et l'espace disponible
- **Persistance** : La bibliothèque sélectionnée reste active entre les parties

## 🐛 Résolution de problèmes

**Le menu ne s'affiche pas correctement** :
- Vérifiez que `mots.json` est valide (format JSON correct)
- Assurez-vous qu'il y a au moins une bibliothèque dans le fichier

**La bibliothèque ne change pas** :
- Cliquez bien sur "Valider" (pas "Retour")
- Vérifiez que le carré à cocher est bien rempli en vert

**Pas assez de place pour voir toutes les bibliothèques** :
- Utilisez la molette pour scroller
- L'indicateur `(x-y/z)` montre votre position dans la liste

## 📝 Changements apportés

1. **Menu.py** :
   - Ajout du paramètre bibliothèque dans `fenetre_parametres()`
   - Ajout du paramètre bibliothèque dans `fenetre_niveau()`
   - Gestion du scroll avec la molette
   - Affichage des bibliothèques avec cases à cocher (radio buttons)

2. **jeu.py** :
   - Ajout de `self.bibliotheque` dans `_initialiser_variables()`
   - Appel de `BaseDonnees.set_bibliotheque_active()` après sélection

3. **Tests** :
   - Nouveau script `test_menu_bibliotheques.py` pour tester le menu

---

**Besoin d'aide ?** Consultez les autres guides :
- [README_BIBLIOTHEQUES.md](README_BIBLIOTHEQUES.md) - Gestion des bibliothèques
- [GUIDE_MOTS.md](GUIDE_MOTS.md) - Gestion des mots
- [test_menu_bibliotheques.py](test_menu_bibliotheques.py) - Script de test
