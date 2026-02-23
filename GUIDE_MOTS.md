# Guide de gestion des mots - ChasseAuxMots

## Fichier de mots : mots.json

Le jeu charge maintenant tous les mots depuis le fichier `mots.json`. 

### Structure du fichier

Le fichier contient une simple liste de mots :

```json
{
    "mots": [
        "a", "b", "c",
        "os", "lac", "nid",
        "arbre", "forêt",
        "un os", "une forêt dense"
    ]
}
```

### Tri automatique par niveau

Les mots sont automatiquement triés dans les niveaux au démarrage du jeu selon ces critères :

- **Niveau 1** : Un seul caractère
  - Exemples : `a`, `b`, `é`, `ç`
  
- **Niveau 2** : Mots de moins de 5 lettres SANS caractères spéciaux (accents, etc.)
  - Exemples : `os`, `lac`, `nid`, `air`
  
- **Niveau 3** : Mots d'au moins 5 lettres OU mots avec caractères spéciaux
  - Exemples : `arbre`, `forêt`, `île`, `épée`
  
- **Niveau 4** : Identique au niveau 3 (mêmes mots)
  
- **Niveau 5** : Groupes nominaux (expressions contenant des espaces)
  - Exemples : `un os`, `une forêt dense`, `le petit chat`

### Comment ajouter de nouveaux mots

1. Ouvrez le fichier `mots.json`
2. Ajoutez vos mots dans la liste `"mots"`, séparés par des virgules
3. Sauvegardez le fichier
4. Les mots seront automatiquement triés dans les niveaux appropriés au prochain lancement

**Exemple :**
```json
{
    "mots": [
        "a", "b", "c",
        "lac",
        "dragon",
        "château médiéval"
    ]
}
```

### Distribution actuelle

- Niveau 1 : 59 caractères
- Niveau 2 : 38 mots courts sans accents
- Niveau 3 : 135 mots longs ou avec accents
- Niveau 4 : 135 mots (identiques au niveau 3)
- Niveau 5 : 92 groupes nominaux

### Notes importantes

- Le fichier doit être au format JSON valide
- Les mots avec espaces seront toujours dans le niveau 5
- Les caractères spéciaux (accents) rendent un mot plus difficile → niveau 3 minimum
- Les mots courts sans accents vont dans le niveau 2
