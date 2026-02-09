import pandas as pd
import os
from datetime import datetime

# Fichier de sauvegarde des joueurs
FICHIER_JOUEURS = "joueurs.csv"

mots={
    "niveau1": [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
        'à', 'é', 'è', 'ù', 'ç', 'ê', 'ü'
        ],
    "niveau2": [
        'os', 'bec', 'cou', 'cri', 'dos', 'eau', 'feu', 'lac', 'nid', 'roc', 'sol',
        'vol', 'adn', 'age', 'île', 'aile', 'bois', 'boue', 'cerf', 'croc', 'dent',
        'loup', 'lave', 'main', 'mini', 'ours', 'peau', 'vent', 'abri', 'arme', 'baie',
        'clan', 'côte', 'cuir', 'dune', 'épée', 'miel', 'mont', 'poil', 'site', 'suie',
        'arbre', 'bison', 'corne', 'forêt', 'géant', 'herbe', 'hyène', 'liane', 'neige',
        'patte', 'plume', 'proie', 'queue', 'rugit', 'sable', 'sabre', 't-rex', 'terre',
        'trace', 'tyran', 'algue', 'ambre', 'antre', 'bâton', 'brume', 'chaud', 'craie',
        'épine', 'époux', 'froid', 'galet', 'hache', 'horde', 'lance', 'meute', 'nuage',
        'océan', 'ongle', 'outil', 'paroi', 'pente', 'piste', 'pluie', 'ravin', 'silex'
        ],
    "niveau3": [
        'tribu', 'argile', 'chasse', 'fourmi', 'griffe', 'loutre', 'lézard', 'marais',
        'mousse', 'museau', 'pierre', 'plante', 'raptor', 'renard', 'tortue', 'volcan',
        'bambou', 'boueux', 'braise', 'cabane', 'cactus', 'canine', 'cendre', 'corail',
        'croûte', 'désert', 'étoile', 'grotte', 'harpon', 'ivoire', 'jungle', 'plaine',
        'pollen', 'racine', 'radeau', 'résine', 'rivage', 'rocher', 'savane', 'source',
        'steppe', 'vallée', 'caverne', 'cratère', 'fossile', 'fougère', 'griffes',
        'insecte', 'météore', 'serpent', 'branche', 'caillou', 'colline', 'cristal',
        'défense', 'falaise', 'feuille', 'matière', 'minéral', 'poisson', 'prairie',
        'rivière', 'rocheux', 'tanière', 'terrier', 'torrent', 'toundra', 'végétal',
        'ammonite', 'araignée', 'chasseur', 'écailles', 'mâchoire', 'mammouth', 'scarabée',
        'carapace', 'marécage', 'sédiment', 'tonnerre', 'astéroïde', 'empreinte', 'libellule',
        'prédateur', 'squelette', 'grenouille', 'tricératops', 'vélociraptor'
        ],
    "niveau5": [
        'un os', 'un roc', 'un bec', 'un nid', 'un feu', 'un lac', 'un cri', 'une dent',
        'une peau', 'un T-Rex', 'un crâne', 'une aile', 'du sable', 'une trace', 'un raptor',
        'une patte', 'une corne', 'une queue', 'un museau', 'un marais', 'un volcan', 'une forêt',
        'une herbe', 'une proie', 'une plume', 'un lézard', 'une griffe', 'un fossile', 'une chasse',
        'une grotte', 'une pierre', 'un serpent', 'une tortue', 'une fourmi', 'un mammouth', 'un astéroïde',
        'un squelette', 'une empreinte', 'un T-Rex géant', 'du sable chaud', 'un cri perçant',
        'une dent acérée', 'un crâne massif', 'un volcan actif', 'une forêt dense', 'une herbe haute',
        'un lézard géant', 'une peau épaisse', 'un nid abandonné', 'un raptor rapide', 'une longue queue',
        'un museau pointu', 'un marais boueux', 'une proie facile', 'un raptor affamé', 'une trace fraîche',
        'une grotte sombre', 'une plume colorée', 'une tortue géante', 'une fourmi géante', 'une dent de T-Rex',
        'une griffe pointue', 'une chasse réussie', 'une pierre taillée', 'un astéroïde géant', 'une trace de patte',
        'une grotte habitée', 'une patte puissante', 'un mammouth laineux', 'un serpent venimeux', 'un nid de dinosaure',
        'un T-Rex redoutable', 'un museau de raptor', 'une corne tranchante', 'un lac préhistorique', 'une griffe de raptor',
        'un squelette complet', 'une peau de mammouth', 'un crâne de dinosaure', 'un volcan en éruption', 'une forêt de fougères',
        'une pierre volcanique', 'une empreinte profonde', 'une patte de dinosaure', 'une empreinte de T-Rex',
        'une chasse au mammouth', 'une queue de stégosaure', 'un marais préhistorique', 'un fossile bien conservé',
        'une corne de tricératops', 'une aile de ptérodactyle', 'un lac de la préhistoire'
        ]
    }

df = pd.DataFrame({k: pd.Series(v) for k, v in mots.items()})


OBSTACLES_CONFIG = {
    "dino_volant": {
        "chemin_base": "images/Mechant/dino_volant",
        "nb_images": 7,
        "animation_delay": 7,
        "hauteur": 120,
        "type": 2
    },
    "dino": {
        "chemin_base": "images/Mechant/dino",
        "nb_images": 4,
        "animation_delay": 5,
        "hauteur": 100,
        "type": 2
    },
    "rock_round": {
        "chemin_base": "images/Mechant/rock_round",
        "nb_images": 12,
        "animation_delay": 8,
        "hauteur": 80,
        "type": 0
    }
}


# DataFrame pour enregistrer les joueurs
def charger_joueurs():
    """Charge les joueurs depuis le fichier CSV s'il existe, sinon crée un DataFrame vide"""
    colonnes_attendues = [
        'Nom', 
        'Prénom', 
        'Date_Inscription',
        'Nb_Parties', 
        'Mots_Réussis_Total',
        'Vitesse_Moyenne_WPM',
        'Erreurs_Total'
    ]
    
    if os.path.exists(FICHIER_JOUEURS):
        df = pd.read_csv(FICHIER_JOUEURS)
        
        # Migration : Ajouter les colonnes manquantes
        for col in colonnes_attendues:
            if col not in df.columns:
                if col == 'Mots_Réussis_Total':
                    df[col] = 0
                elif col == 'Vitesse_Moyenne_WPM':
                    df[col] = 0.0
                elif col == 'Erreurs_Total':
                    df[col] = 0
                elif col == 'Date_Inscription':
                    df[col] = ''
                else:
                    df[col] = ''
        
        return df
    else:
        return pd.DataFrame(columns=colonnes_attendues)

df_joueurs = charger_joueurs()

def sauvegarder_joueurs():
    """Sauvegarde le DataFrame des joueurs dans un fichier CSV"""
    global df_joueurs
    df_joueurs.to_csv(FICHIER_JOUEURS, index=False)

def ajouter_joueur(nom, prenom):
    """Ajoute un nouveau joueur au DataFrame et sauvegarde"""
    global df_joueurs
    
    # Vérifier si le joueur existe déjà
    joueur_existant = df_joueurs[
        (df_joueurs['Nom'].str.lower() == nom.lower()) & 
        (df_joueurs['Prénom'].str.lower() == prenom.lower())
    ]
    
    if not joueur_existant.empty:
        # Le joueur existe déjà
        return False, "Ce joueur existe déjà!"
    
    # Ajouter le nouveau joueur
    nouvelle_ligne = {
        'Nom': nom.capitalize(),
        'Prénom': prenom.capitalize(),
        'Date_Inscription': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Nb_Parties': 0,
        'Mots_Réussis_Total': 0,
        'Vitesse_Moyenne_WPM': 0.0,
        'Erreurs_Total': 0
    }
    df_joueurs = pd.concat([df_joueurs, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    sauvegarder_joueurs()
    return True, "Joueur créé avec succès!"

def joueur_existe(nom, prenom):
    """Vérifie si un joueur existe"""
    return not df_joueurs[
        (df_joueurs['Nom'].str.lower() == nom.lower()) & 
        (df_joueurs['Prénom'].str.lower() == prenom.lower())
    ].empty

def get_joueur(nom, prenom):
    """Récupère les données d'un joueur"""
    joueur = df_joueurs[
        (df_joueurs['Nom'].str.lower() == nom.lower()) & 
        (df_joueurs['Prénom'].str.lower() == prenom.lower())
    ]
    if not joueur.empty:
        return joueur.iloc[0]
    return None

def update_stats_joueur(nom, prenom, mots_reussis, vitesse_wpm, nb_erreurs):
    """Met à jour les statistiques du joueur après une partie"""
    global df_joueurs
    mask = (df_joueurs['Nom'].str.lower() == nom.lower()) & (df_joueurs['Prénom'].str.lower() == prenom.lower())
    if mask.any():
        idx = df_joueurs[mask].index[0]
        
        # Récupérer les anciennes stats
        nb_parties_ancien = df_joueurs.loc[idx, 'Nb_Parties']
        mots_reussis_ancien = df_joueurs.loc[idx, 'Mots_Réussis_Total']
        vitesse_ancienne = df_joueurs.loc[idx, 'Vitesse_Moyenne_WPM']
        erreurs_ancien = df_joueurs.loc[idx, 'Erreurs_Total']
        
        # Calculer les nouvelles statistiques
        nb_parties_nouveau = nb_parties_ancien + 1
        mots_reussis_nouveau = mots_reussis_ancien + mots_reussis
        
        # Calculer la moyenne de vitesse
        if nb_parties_ancien == 0:
            vitesse_nouvelle = vitesse_wpm
        else:
            vitesse_nouvelle = (vitesse_ancienne * nb_parties_ancien + vitesse_wpm) / nb_parties_nouveau
        
        erreurs_nouveau = erreurs_ancien + nb_erreurs
        
        # Mettre à jour les valeurs
        df_joueurs.loc[idx, 'Nb_Parties'] = nb_parties_nouveau
        df_joueurs.loc[idx, 'Mots_Réussis_Total'] = mots_reussis_nouveau
        df_joueurs.loc[idx, 'Vitesse_Moyenne_WPM'] = round(vitesse_nouvelle, 2)
        df_joueurs.loc[idx, 'Erreurs_Total'] = erreurs_nouveau
        
        sauvegarder_joueurs()

