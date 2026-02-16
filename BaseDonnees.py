import json
import os
import tempfile
import shutil
import atexit
from datetime import datetime

# Configuration des répertoires
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DATA_DIR = os.path.join(tempfile.gettempdir(), "ChasseAuxMots")
os.makedirs(TEMP_DATA_DIR, exist_ok=True)

# Fichier de configuration
FICHIER_CONFIG = os.path.join(SCRIPT_DIR, "config.txt")

def lire_repertoire_config():
    """Lit le répertoire de sauvegarde depuis config.txt"""
    
    # Lire le fichier de configuration s'il existe
    if os.path.exists(FICHIER_CONFIG):
        try:
            with open(FICHIER_CONFIG, 'r', encoding='utf-8') as f:
                # Lire ligne par ligne pour ignorer les commentaires
                for ligne in f:
                    chemin = ligne.strip()
                    
                    # Ignorer les lignes vides et commentaires
                    if chemin and not chemin.startswith('#'):
                        # Tester l'accès en écriture
                        try:
                            os.makedirs(chemin, exist_ok=True)
                            test_file = os.path.join(chemin, ".test_write.tmp")
                            with open(test_file, 'w') as tf:
                                tf.write("test")
                            os.remove(test_file)
                            print(f"[INFO] Repertoire configure: {chemin}")
                            return chemin
                        except Exception as e:
                            print(f"[WARNING] Impossible d'utiliser {chemin}: {e}")
                            print(f"[INFO] Basculement vers TEMP")
                            return TEMP_DATA_DIR
        except Exception as e:
            print(f"[WARNING] Erreur lecture config.txt: {e}")
    
    # Par défaut : créer config.txt avec TEMP
    try:
        with open(FICHIER_CONFIG, 'w', encoding='utf-8') as f:
            f.write(f"# Configuration ChasseAuxMots - Chemin de sauvegarde des donnees\n")
            f.write(f"# Modifiez cette ligne pour changer le dossier de sauvegarde\n")
            f.write(f"# Exemple: C:\\Users\\VotreNom\\Documents\\ChasseAuxMots\n")
            f.write(f"\n{TEMP_DATA_DIR}\n")
        print(f"[INFO] Fichier config.txt cree avec le repertoire par defaut")
    except Exception as e:
        print(f"[WARNING] Impossible de creer config.txt: {e}")
    
    return TEMP_DATA_DIR

# Obtenir le répertoire de données depuis la configuration
REPERTOIRE_DONNEES = lire_repertoire_config()
FICHIER_JOUEURS = os.path.join(REPERTOIRE_DONNEES, "joueurs.json")
FICHIER_JOUEURS_PROJET = os.path.join(SCRIPT_DIR, "joueurs.json")

print(f"[INFO] Repertoire de sauvegarde: {REPERTOIRE_DONNEES}")
print(f"[INFO] Fichier joueurs: {FICHIER_JOUEURS}")

def copier_fichier_vers_projet():
    """Copie le fichier vers le dossier du projet à la fermeture (si différent)"""
    try:
        # Ne copier que si le répertoire de données est différent du projet
        if os.path.exists(FICHIER_JOUEURS) and REPERTOIRE_DONNEES != SCRIPT_DIR:
            print(f"[INFO] Copie de {FICHIER_JOUEURS} vers {FICHIER_JOUEURS_PROJET}...")
            # Utiliser une copie manuelle plus robuste au lieu de shutil.copy2
            with open(FICHIER_JOUEURS, 'r', encoding='utf-8') as f_source:
                contenu = f_source.read()
            with open(FICHIER_JOUEURS_PROJET, 'w', encoding='utf-8') as f_dest:
                f_dest.write(contenu)
            print(f"[INFO] Copie reussie!")
    except Exception as e:
        print(f"[WARNING] Impossible de copier le fichier vers le projet: {e}")
        print(f"[INFO] Les donnees sont sauvegardees dans: {FICHIER_JOUEURS}")

# Enregistrer la fonction pour qu'elle s'exécute à la fermeture
atexit.register(copier_fichier_vers_projet)

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

# Note: Le dictionnaire 'mots' est directement accessible pour obtenir les mots par niveau
# Exemple: mots["niveau1"], mots["niveau2"], etc.

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

PERSONNAGES_CONFIG = {
    "viking": {
        "chemin_base": "images/Man/Viking",
        "sprite_defaut": "images/Man/Viking/viking_attaque_1.png",
        "hauteur": 120,
        "animations": {
            "attaque": {
                "chemin_base": "images/Man/Viking/viking_attaque",
                "nb_images": 5,
                "animation_delay": 8
            }
        }
    },
    "dino_vert": {
        "chemin_base": "images/Dino_vert",
        "sprite_defaut": "images/Dino_vert/Idle (1).png",
        "hauteur": 120,
        "animations": {
            "idle": {
                "chemin_base": "images/Dino_vert/Idle",
                "nb_images": 10,
                "animation_delay": 5,
                "format": " ({}).png"
            },
            "run": {
                "chemin_base": "images/Dino_vert/Run",
                "nb_images": 8,
                "animation_delay": 5,
                "format": " ({}).png"
            },
            "jump": {
                "chemin_base": "images/Dino_vert/Jump",
                "nb_images": 12,
                "animation_delay": 5,
                "format": " ({}).png"
            },
            "walk": {
                "chemin_base": "images/Dino_vert/Walk",
                "nb_images": 10,
                "animation_delay": 5,
                "format": " ({}).png"
            },
            "dead": {
                "chemin_base": "images/Dino_vert/Dead",
                "nb_images": 8,
                "animation_delay": 5,
                "format": " ({}).png"
            }
        }
    }
}

Univers = {
    "foret_bleue":{
        "background": { 
            "chemin": "images/Foret_bleue/Background/" #ajouter le numéro de 1 a nombre de fichier-1 et .png
        },
        "personnages": {
            "Skelette_Crusader_1": {
                "running": "images/Foret_bleue/Skeleton_Crusader_1/PNG/PNG Sequences/Running/0_Skeleton_Crusader_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Skelette_Crusader_2": {
                "running": "images/Foret_bleue/Skeleton_Crusader_2/PNG/PNG Sequences/Running/0_Skeleton_Crusader_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Skelette_Crusader_3": {
                "running": "images/Foret_bleue/Skeleton_Crusader_3/PNG/PNG Sequences/Running/0_Skeleton_Crusader_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Skelette_warrior_1": {
                "running": "images/Foret_bleue/Skeleton_Warrior_1/PNG/PNG Sequences/Running/0_Skeleton_Warrior_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Skelette_warrior_2": {
                "running": "images/Foret_bleue/Skeleton_Warrior_2/PNG/PNG Sequences/Running/0_Skeleton_Warrior_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Skelette_warrior_3": {
                "running": "images/Foret_bleue/Skeleton_Warrior_3/PNG/PNG Sequences/Running/0_Skeleton_Warrior_Running_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            }
        }
    },
    "foret_violette":{
        "background": { 
            "chemin": "images/Foret_violette/Background/" #ajouter le numéro de 1 a nombre de fichier-1 et .png
        },
        "personnages": {
            "Golem_01": {
                "walking": "images/Foret_violette/Golem_01/PNG Sequences/Walking/0_Golem_01_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Golem_02": {
                "walking": "images/Foret_violette/Golem_02/PNG Sequences/Walking/0_Golem_02_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Golem_03": {
                "walking": "images/Foret_violette/Golem_03/PNG Sequences/Walking/0_Golem_03_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Wraith_01": {
                "walking": "images/Foret_violette/Wraith_01/PNG Sequences/Walking/0_Wraith_01_Moving Forward_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Wraith_02": {
                "walking": "images/Foret_violette/Wraith_02/PNG Sequences/Walking/0_Wraith_02_Moving Forward_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Wraith_03": {
                "walking": "images/Foret_violette/Wraith_03/PNG Sequences/Walking/0_Wraith_03_Moving Forward_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            }
        }
    },
    "foret_au_champignon":{
        "background": { 
            "chemin": "images/Foret_au_champignon/Background/" #ajouter le numéro de 1 a nombre de fichier-1 et .png
        },
        "personnages": {
            "Golem_1": {
                "walking": "images/Foret_au_champignon/Golem_1/PNG/PNG Sequences/Walking/0_Golem_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Golem_2": {
                "walking": "images/Foret_au_champignon/Golem_2/PNG/PNG Sequences/Walking/0_Golem_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Golem_3": {
                "walking": "images/Foret_au_champignon/Golem_3/PNG/PNG Sequences/Walking/0_Golem_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Satyr_01": {
                "walking": "images/Foret_au_champignon/Satyr_01/PNG Sequences/Walking/Satyr_01_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Satyr_02": {
                "walking": "images/Foret_au_champignon/Satyr_02/PNG Sequences/Walking/Satyr_02_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Satyr_03": {
                "walking": "images/Foret_au_champignon/Satyr_03/PNG Sequences/Walking/Satyr_03_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            }
        }
    },
    "vallee_verte":{
        "background": { 
            "chemin": "images/Vallee_verte/Background/" #ajouter le numéro de 1 a nombre de fichier-1 et .png
        },
        "personnages": {
            "Forest_Ranger_1": {
                "walking": "images/Vallee_verte/Forest_Ranger_1/PNG/PNG Sequences/Walking/0_Forest_Ranger_1_Walking_00_Forest_Ranger_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Forest_Ranger_2": {
                "walking": "images/Vallee_verte/Forest_Ranger_2/PNG/PNG Sequences/Walking/0_Forest_Ranger_2_Walking_00_Forest_Ranger_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Forest_Ranger_3": {
                "walking": "images/Vallee_verte/Forest_Ranger_3/PNG/PNG Sequences/Walking/0_Forest_Ranger_3_Walking_00_Forest_Ranger_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Minautor_1": {
                "walking": "images/Vallee_verte/Minautor_1/PNG/PNG Sequences/Walking/0_Minotaur_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Minautor_2": {
                "walking": "images/Vallee_verte/Minautor_2/PNG/PNG Sequences/Walking/0_Minotaur_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            },
            "Minautor_3": {
                "walking": "images/Vallee_verte/Minautor_3/PNG/PNG Sequences/Walking/0_Minotaur_Walking_0" #ajouter le numéro de 00 a nombre de fichier-1 et .png
            }
        }
    }
}

def get_animation_frames(personnage_type, animation_name):
    """
    Génère la liste des chemins des frames d'animation pour un personnage.
    
    Args:
        personnage_type: Type de personnage (ex: "viking", "man", "centipede", "dino_vert")
        animation_name: Nom de l'animation (ex: "attaque", "walk", "idle", etc.)
    
    Returns:
        Liste des chemins des frames d'animation ou None si non trouvé
    """
    if personnage_type not in PERSONNAGES_CONFIG:
        return None
    
    config = PERSONNAGES_CONFIG[personnage_type]
    
    if animation_name not in config['animations']:
        return None
    
    anim_config = config['animations'][animation_name]
    
    # Si c'est un sprite unique (nb_images = 1)
    if anim_config.get('nb_images', 1) == 1:
        if 'sprite' in anim_config:
            return [anim_config['sprite']]
        else:
            return None
    
    # Si c'est une séquence d'images
    frames = []
    chemin_base = anim_config.get('chemin_base', '')
    nb_images = anim_config.get('nb_images', 1)
    format_str = anim_config.get('format', '_{}.png')  # Format par défaut: _1.png, _2.png, etc.
    
    for i in range(1, nb_images + 1):
        # Si le format contient {}, remplacer par le numéro
        if '{}' in format_str:
            frame_path = f"{chemin_base}{format_str.format(i)}"
        else:
            frame_path = f"{chemin_base}{format_str}"
        frames.append(frame_path)
    
    return frames

def get_personnage_sprite_defaut(personnage_type):
    """
    Retourne le sprite par défaut d'un personnage.
    
    Args:
        personnage_type: Type de personnage (ex: "viking", "man", etc.)
    
    Returns:
        Chemin du sprite par défaut ou None
    """
    if personnage_type not in PERSONNAGES_CONFIG:
        return None
    return PERSONNAGES_CONFIG[personnage_type].get('sprite_defaut')

def get_personnage_hauteur(personnage_type):
    """
    Retourne la hauteur par défaut d'un personnage.
    
    Args:
        personnage_type: Type de personnage (ex: "viking", "man", etc.)
    
    Returns:
        Hauteur du personnage ou 120 par défaut
    """
    if personnage_type not in PERSONNAGES_CONFIG:
        return 120
    return PERSONNAGES_CONFIG[personnage_type].get('hauteur', 120)

def get_animation_delay(personnage_type, animation_name):
    """
    Retourne le délai d'animation pour un personnage et une animation donnés.
    
    Args:
        personnage_type: Type de personnage (ex: "viking", "man", etc.)
        animation_name: Nom de l'animation (ex: "attaque", "walk", etc.)
    
    Returns:
        Délai d'animation ou 5 par défaut
    """
    if personnage_type not in PERSONNAGES_CONFIG:
        return 5
    
    config = PERSONNAGES_CONFIG[personnage_type]
    if animation_name not in config['animations']:
        return 5
    
    return config['animations'][animation_name].get('animation_delay', 5)

# Dictionnaire pour enregistrer les joueurs
def charger_joueurs():
    """Charge les joueurs depuis le fichier JSON s'il existe, sinon crée un dictionnaire vide"""
    
    # Si le fichier TEMP n'existe pas mais que le fichier projet existe, copier
    if not os.path.exists(FICHIER_JOUEURS) and os.path.exists(FICHIER_JOUEURS_PROJET):
        try:
            print(f"[INFO] Copie de {FICHIER_JOUEURS_PROJET} vers {FICHIER_JOUEURS}...")
            shutil.copy2(FICHIER_JOUEURS_PROJET, FICHIER_JOUEURS)
            print(f"[INFO] Copie initiale reussie!")
        except Exception as e:
            print(f"[WARNING] Impossible de copier depuis le projet: {e}")
    
    if os.path.exists(FICHIER_JOUEURS):
        try:
            with open(FICHIER_JOUEURS, 'r', encoding='utf-8') as f:
                joueurs = json.load(f)
            return joueurs
        except Exception as e:
            print(f"[WARNING] Erreur lors du chargement de {FICHIER_JOUEURS}: {e}")
            return {}
    else:
        return {}

dict_joueurs = charger_joueurs()

def sauvegarder_joueurs():
    """Sauvegarde le dictionnaire des joueurs dans un fichier JSON dans le répertoire configuré"""
    global dict_joueurs
    
    try:
        import random
        # Utiliser le répertoire de données configuré
        temp_filename = os.path.join(REPERTOIRE_DONNEES, f"joueurs_temp_{random.randint(1000,9999)}.json")
        
        print(f"[DEBUG] Sauvegarde dans: {FICHIER_JOUEURS}")
        
        # Écrire dans le fichier temporaire
        with open(temp_filename, 'w', encoding='utf-8') as f:
            json.dump(dict_joueurs, f, ensure_ascii=False, indent=4)
        
        # Supprimer l'ancien et renommer
        if os.path.exists(FICHIER_JOUEURS):
            os.remove(FICHIER_JOUEURS)
        
        os.rename(temp_filename, FICHIER_JOUEURS)
        
        print(f"[DEBUG] Sauvegarde OK: {len(dict_joueurs)} joueurs")
        return True
        
    except Exception as e:
        print(f"[DEBUG] Erreur sauvegarde: {e}")
        import traceback
        traceback.print_exc()
        # Nettoyer
        try:
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                os.remove(temp_filename)
        except:
            pass
        return False

def ajouter_joueur(nom, prenom):
    """Ajoute un nouveau joueur au dictionnaire et sauvegarde"""
    global dict_joueurs
    
    print("[DEBUG] Debut ajouter_joueur()")
    print(f"[DEBUG] Repertoire de sauvegarde: {REPERTOIRE_DONNEES}")
    
    # Créer la clé unique
    cle = f"{nom}_{prenom}".lower()
    
    # Vérifier si le joueur existe déjà
    if cle in dict_joueurs:
        return False, "Ce joueur existe deja!"
    
    # Créer les données du nouveau joueur
    dict_joueurs[cle] = {
        'nom': nom.capitalize(),
        'prenom': prenom.capitalize(),
        'date_inscription': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'nb_parties': 0,
        'mots_reussis_total': 0,
        'vitesse_moyenne_wpm': 0.0,
        'derniere_vitesse_wpm': 40.0,
        'erreurs_total': 0
    }
    
    print(f"[DEBUG] Nouveau joueur: {dict_joueurs[cle]}")
    print(f"[DEBUG] Dictionnaire en memoire: {len(dict_joueurs)} joueurs")
    
    # ECRIRE DANS LE REPERTOIRE CONFIGURE (ou TEMP par défaut)
    try:
        succes = sauvegarder_joueurs()
        
        if succes:
            print("[DEBUG] SUCCES!")
            print(f"[INFO] Joueur sauvegarde dans: {FICHIER_JOUEURS}")
            return True, "Joueur cree avec succes!"
        else:
            return True, "Joueur cree en memoire (erreur sauvegarde)"
        
    except Exception as e:
        print(f"[DEBUG] ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return True, f"Joueur cree en memoire (erreur sauvegarde: {e})"

def joueur_existe(nom, prenom):
    """Verifie si un joueur existe"""
    cle = f"{nom}_{prenom}".lower()
    return cle in dict_joueurs

def get_joueur(nom, prenom):
    """Recupere les donnees d'un joueur"""
    cle = f"{nom}_{prenom}".lower()
    if cle in dict_joueurs:
        return dict_joueurs[cle]
    return None

def update_stats_joueur(nom, prenom, mots_reussis, vitesse_wpm, nb_erreurs):
    """Met a jour les statistiques du joueur apres une partie"""
    global dict_joueurs
    
    cle = f"{nom}_{prenom}".lower()
    
    if cle in dict_joueurs:
        joueur = dict_joueurs[cle]
        
        # Récupérer les anciennes stats
        nb_parties_ancien = joueur['nb_parties']
        mots_reussis_ancien = joueur['mots_reussis_total']
        vitesse_ancienne = joueur['vitesse_moyenne_wpm']
        erreurs_ancien = joueur['erreurs_total']
        
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
        joueur['nb_parties'] = nb_parties_nouveau
        joueur['mots_reussis_total'] = mots_reussis_nouveau
        joueur['vitesse_moyenne_wpm'] = round(vitesse_nouvelle, 2)
        # Ne pas modifier 'derniere_vitesse_wpm' ici : conserver la valeur saisie
        joueur['erreurs_total'] = erreurs_nouveau
        
        # Tenter de sauvegarder (ne crash pas si échec)
        succes = sauvegarder_joueurs()
        if not succes:
            print("ATTENTION: Les statistiques n'ont pas pu être sauvegardées!")
        return succes
    return False


def set_derniere_vitesse(nom, prenom, valeur):
    """Enregistre la dernière valeur de vitesse entrée pour le joueur."""
    global dict_joueurs
    
    cle = f"{nom}_{prenom}".lower()
    
    if cle in dict_joueurs:
        try:
            dict_joueurs[cle]['derniere_vitesse_wpm'] = float(valeur)
            sauvegarder_joueurs()
        except Exception:
            pass

