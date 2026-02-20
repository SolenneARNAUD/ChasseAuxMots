import json
import os
import sys
import tempfile
import shutil
import atexit
from datetime import datetime

def resource_path(relative_path):
    """ Calcule le chemin absolu pour les ressources (indispensable pour le .exe) """
    if hasattr(sys, '_MEIPASS'):
        # Chemin vers le dossier temporaire du .exe
        return os.path.join(sys._MEIPASS, relative_path)
    # Chemin vers le dossier habituel en développement
    return os.path.join(os.path.abspath("."), relative_path)

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
    "niveau4": [
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
            "chemin": "images/Foret_bleue/Background/"
        },
        "personnages": {
            "Skelette_Crusader_1": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_1/PNG/PNG Sequences/Idle/0_Skeleton_Crusader_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_1/PNG/PNG Sequences/Walking/0_Skeleton_Crusader_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Skelette_Crusader_2": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_2/PNG/PNG Sequences/Idle/0_Skeleton_Crusader_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_2/PNG/PNG Sequences/Walking/0_Skeleton_Crusader_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Skelette_Crusader_3": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_3/PNG/PNG Sequences/Idle/0_Skeleton_Crusader_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Crusader_3/PNG/PNG Sequences/Walking/0_Skeleton_Crusader_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Skelette_warrior_1": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_1/PNG/PNG Sequences/Idle/0_Skeleton_Warrior_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_1/PNG/PNG Sequences/Walking/0_Skeleton_Warrior_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Skelette_warrior_2": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_2/PNG/PNG Sequences/Idle/0_Skeleton_Warrior_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_2/PNG/PNG Sequences/Walking/0_Skeleton_Warrior_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Skelette_warrior_3": {
                "idle": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_3/PNG/PNG Sequences/Idle/0_Skeleton_Warrior_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_bleue/Skeleton_Warrior_3/PNG/PNG Sequences/Walking/0_Skeleton_Warrior_Walking_",
                    "nb_images": 24,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            }
        }
    },
    "foret_violette":{
        "background": { 
            "chemin": "images/Foret_violette/Background/"
        },
        "personnages": {
            "Golem_01": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Golem_01/PNG Sequences/Idle/Golem_01_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Golem_01/PNG Sequences/Walking/Golem_01_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Golem_02": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Golem_02/PNG Sequences/Idle/Golem_02_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Golem_02/PNG Sequences/Walking/Golem_02_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Golem_03": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Golem_03/PNG Sequences/Idle/Golem_03_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Golem_03/PNG Sequences/Walking/Golem_03_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Wraith_01": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Wraith_01/PNG Sequences/Idle/Wraith_01_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Wraith_01/PNG Sequences/Walking/Wraith_01_Moving Forward_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Wraith_02": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Wraith_02/PNG Sequences/Idle/Wraith_02_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Wraith_02/PNG Sequences/Walking/Wraith_02_Moving Forward_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Wraith_03": {
                "idle": {
                    "chemin_base": "images/Foret_violette/Wraith_03/PNG Sequences/Idle/Wraith_03_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_violette/Wraith_03/PNG Sequences/Walking/Wraith_03_Moving Forward_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            }
        }
    },
    "foret_au_champignon":{
        "background": { 
            "chemin": "images/Foret_au_champignon/Background/"
        },
        "personnages": {
            "Golem_1": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Golem_1/PNG/PNG Sequences/Idle/0_Golem_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Golem_1/PNG/PNG Sequences/Walking/0_Golem_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Golem_2": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Golem_2/PNG/PNG Sequences/Idle/0_Golem_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Golem_2/PNG/PNG Sequences/Walking/0_Golem_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Golem_3": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Golem_3/PNG/PNG Sequences/Idle/0_Golem_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Golem_3/PNG/PNG Sequences/Walking/0_Golem_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Satyr_01": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_01/PNG Sequences/Idle/Satyr_01_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_01/PNG Sequences/Walking/Satyr_01_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Satyr_02": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_02/PNG Sequences/Idle/Satyr_02_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_02/PNG Sequences/Walking/Satyr_02_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Satyr_03": {
                "idle": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_03/PNG Sequences/Idle/Satyr_03_Idle_",
                    "nb_images": 12,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Foret_au_champignon/Satyr_03/PNG Sequences/Walking/Satyr_03_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            }
        }
    },
    "vallee_verte":{
        "background": { 
            "chemin": "images/Vallee_verte/Background/"
        },
        "personnages": {
            "Forest_Ranger_1": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_1/PNG/PNG Sequences/Idle/0_Forest_Ranger_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_1/PNG/PNG Sequences/Walking/0_Forest_Ranger_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Forest_Ranger_2": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_2/PNG/PNG Sequences/Idle/0_Forest_Ranger_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_2/PNG/PNG Sequences/Walking/0_Forest_Ranger_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Forest_Ranger_3": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_3/PNG/PNG Sequences/Idle/0_Forest_Ranger_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Forest_Ranger_3/PNG/PNG Sequences/Walking/0_Forest_Ranger_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Minotaur_1": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Minotaur_1/PNG/PNG Sequences/Idle/0_Minotaur_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Minotaur_1/PNG/PNG Sequences/Walking/0_Minotaur_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Minotaur_2": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Minotaur_2/PNG/PNG Sequences/Idle/0_Minotaur_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Minotaur_2/PNG/PNG Sequences/Walking/0_Minotaur_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
            },
            "Minotaur_3": {
                "idle": {
                    "chemin_base": "images/Vallee_verte/Minotaur_3/PNG/PNG Sequences/Idle/0_Minotaur_Idle_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                },
                "walking": {
                    "chemin_base": "images/Vallee_verte/Minotaur_3/PNG/PNG Sequences/Walking/0_Minotaur_Walking_",
                    "nb_images": 18,
                    "animation_delay": 5,
                    "format": "{:03d}.png"
                }
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
            return [resource_path(anim_config['sprite'])]
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
        frames.append(resource_path(frame_path))
    
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
    sprite_defaut = PERSONNAGES_CONFIG[personnage_type].get('sprite_defaut')
    if sprite_defaut:
        return resource_path(sprite_defaut)
    return None

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

def get_mechants_univers(univers_cle):
    """
    Retourne la liste des méchants disponibles pour un univers donné.
    
    Args:
        univers_cle: Clé de l'univers (ex: "foret_bleue", "foret_violette", etc.)
    
    Returns:
        Liste des noms des méchants disponibles ou liste vide if univers not found
    """
    if univers_cle not in Univers:
        return []
    
    return list(Univers[univers_cle]["personnages"].keys())

def get_mechant_animation_frames(univers_cle, mechant_nom, animation_name="idle"):
    """
    Génère la liste des chemins des frames d'animation pour un méchant.
    
    Args:
        univers_cle: Clé de l'univers (ex: "foret_bleue")
        mechant_nom: Nom du méchant (ex: "Skelette_Crusader_1")
        animation_name: Nom de l'animation (par défaut "idle")
    
    Returns:
        Tuple (liste des chemins des frames, nombre d'images, délai animation)
        ou (None, 0, 5) if not found
    """
    if univers_cle not in Univers:
        return None, 0, 5
    
    if mechant_nom not in Univers[univers_cle]["personnages"]:
        return None, 0, 5
    
    mechant = Univers[univers_cle]["personnages"][mechant_nom]
    
    if animation_name not in mechant:
        return None, 0, 5
    
    anim_config = mechant[animation_name]
    
    chemin_base = anim_config.get('chemin_base', '')
    nb_images = anim_config.get('nb_images', 1)
    animation_delay = anim_config.get('animation_delay', 5)
    format_str = anim_config.get('format', '{:03d}.png')
    
    # Générer les chemins des frames
    frames = []
    for i in range(nb_images):
        # Format utilise des indices de 0 à n-1
        if '{}' in format_str or '{:03d}' in format_str:
            frame_path = f"{chemin_base}{format_str.format(i)}"
        else:
            # Si pas de format, utiliser le chemin tel quel
            frame_path = chemin_base
        frames.append(resource_path(frame_path))
    
    return frames, nb_images, animation_delay

def get_mechant_config(univers_cle, mechant_nom):
    """
    Retourne la configuration complète d'un méchant pour un univers donné.
    
    Args:
        univers_cle: Clé de l'univers
        mechant_nom: Nom du méchant
    
    Returns:
        Dict avec 'frames', 'nb_images', 'animation_delay' ou empty dict if not found
    """
    frames, nb_images, animation_delay = get_mechant_animation_frames(univers_cle, mechant_nom)
    
    if frames is None:
        return {}
    
    return {
        'frames': frames,
        'nb_images': nb_images,
        'animation_delay': animation_delay,
        'type': 2  # Type 2 = méchant
    }

# Dictionnaire pour enregistrer les joueurs
def migrer_ancienne_structure(joueurs):
    """Migre l'ancienne structure JSON vers la nouvelle structure avec historique et pseudo."""
    joueurs_migres = {}
    
    for cle, joueur in joueurs.items():
        # Si l'ancien format avait nom + prenom, créer un pseudo à partir de la clé
        if 'nom' in joueur and 'prenom' in joueur:
            # Conversion: nom_prenom -> utiliser la clé comme pseudo
            print(f"[INFO] Migration du joueur {cle} vers le format pseudo")
            pseudo = cle  # La clé était déjà nom_prenom en minuscules
            
            # Si pas d'historique, créer la structure complète
            if 'historique' not in joueur:
                joueurs_migres[pseudo] = {
                    'pseudo': pseudo,
                    'date_inscription': joueur.get('date_inscription', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    'historique': {
                        'vallee_verte': {
                            'niveau_1': [],
                            'niveau_2': [],
                            'niveau_3': [],
                            'niveau_4': [],
                            'niveau_5': []
                        },
                        'foret_violette': {
                            'niveau_1': [],
                            'niveau_2': [],
                            'niveau_3': [],
                            'niveau_4': [],
                            'niveau_5': []
                        },
                        'foret_bleue': {
                            'niveau_1': [],
                            'niveau_2': [],
                            'niveau_3': [],
                            'niveau_4': [],
                            'niveau_5': []
                        },
                        'foret_aux_champignons': {
                            'niveau_1': [],
                            'niveau_2': [],
                            'niveau_3': [],
                            'niveau_4': [],
                            'niveau_5': []
                        }
                    }
                }
            else:
                # A déjà l'historique mais pas le pseudo
                joueurs_migres[pseudo] = joueur
                joueurs_migres[pseudo]['pseudo'] = pseudo
                # Supprimer les anciens champs
                joueurs_migres[pseudo].pop('nom', None)
                joueurs_migres[pseudo].pop('prenom', None)
        else:
            # Déjà la nouvelle structure avec pseudo
            joueurs_migres[cle] = joueur
    
    return joueurs_migres

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
            
            # Migrer si nécessaire
            joueurs_originaux = joueurs.copy()
            joueurs = migrer_ancienne_structure(joueurs)
            
            # Si migration effectuée, sauvegarder immédiatement
            if joueurs != joueurs_originaux:
                print(f"[INFO] Sauvegarde après migration...")
                try:
                    with open(FICHIER_JOUEURS, 'w', encoding='utf-8') as f:
                        json.dump(joueurs, f, ensure_ascii=False, indent=4)
                    print(f"[INFO] Migration sauvegardée avec succès")
                except Exception as e:
                    print(f"[WARNING] Erreur lors de la sauvegarde de la migration: {e}")
            
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

def ajouter_joueur(pseudo):
    """Ajoute un nouveau joueur au dictionnaire et sauvegarde"""
    global dict_joueurs
    
    print("[DEBUG] Debut ajouter_joueur()")
    print(f"[DEBUG] Repertoire de sauvegarde: {REPERTOIRE_DONNEES}")
    
    # Créer la clé unique
    cle = pseudo.lower()
    
    # Vérifier si le joueur existe déjà
    if cle in dict_joueurs:
        return False, "Ce joueur existe deja!"
    
    # Créer les données du nouveau joueur avec la nouvelle structure
    dict_joueurs[cle] = {
        'pseudo': pseudo,
        'date_inscription': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'historique': {
            'vallee_verte': {
                'niveau_1': [],
                'niveau_2': [],
                'niveau_3': [],
                'niveau_4': [],
                'niveau_5': []
            },
            'foret_violette': {
                'niveau_1': [],
                'niveau_2': [],
                'niveau_3': [],
                'niveau_4': [],
                'niveau_5': []
            },
            'foret_bleue': {
                'niveau_1': [],
                'niveau_2': [],
                'niveau_3': [],
                'niveau_4': [],
                'niveau_5': []
            },
            'foret_aux_champignons': {
                'niveau_1': [],
                'niveau_2': [],
                'niveau_3': [],
                'niveau_4': [],
                'niveau_5': []
            }
        }
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

def joueur_existe(pseudo):
    """Verifie si un joueur existe"""
    cle = pseudo.lower()
    return cle in dict_joueurs

def get_joueur(pseudo):
    """Recupere les donnees d'un joueur"""
    cle = pseudo.lower()
    if cle in dict_joueurs:
        return dict_joueurs[cle]
    return None

def supprimer_joueur(pseudo):
    """Supprime un joueur du dictionnaire et sauvegarde"""
    global dict_joueurs
    
    # Créer la clé unique
    cle = pseudo.lower()
    
    # Vérifier si le joueur existe
    if cle not in dict_joueurs:
        return False, "Ce joueur n'existe pas!"
    
    # Supprimer le joueur
    del dict_joueurs[cle]
    
    print(f"[DEBUG] Joueur supprimé: {pseudo}")
    print(f"[DEBUG] Dictionnaire en mémoire: {len(dict_joueurs)} joueurs")
    
    # Sauvegarder
    try:
        succes = sauvegarder_joueurs()
        
        if succes:
            print("[DEBUG] Suppression sauvegardée avec succès!")
            print(f"[INFO] Joueur supprimé et sauvegardé dans: {FICHIER_JOUEURS}")
            return True, "Joueur supprimé avec succès!"
        else:
            return True, "Joueur supprimé en mémoire (erreur sauvegarde)"
        
    except Exception as e:
        print(f"[DEBUG] ERREUR lors de la sauvegarde: {e}")
        import traceback
        traceback.print_exc()
        return True, f"Joueur supprimé en mémoire (erreur sauvegarde: {e})"

def update_stats_joueur(pseudo, mots_reussis, vitesse_wpm, nb_erreurs):
    """Met a jour les statistiques du joueur apres une partie (fonction maintenue pour compatibilité)"""
    # Cette fonction est maintenant obsolète mais conservée pour compatibilité
    # Les vraies données sont enregistrées via enregistrer_essai()
    return True

def enregistrer_essai(pseudo, monde, niveau, erreurs_detaillees, vitesse_frappe, 
                     vitesse_defilement, reset_mots_actif, score, delai_niveau4=1500):
    """Enregistre un essai complet dans l'historique du joueur.
    
    Args:
        pseudo: Pseudo du joueur
        monde: Nom du monde (ex: 'foret_bleue')
        niveau: Numéro du niveau (1-5)
        erreurs_detaillees: Liste de dict {'mot': str, 'lettre_attendue': str, 'lettre_tapee': str}
        vitesse_frappe: Vitesse de frappe en caractères/s
        vitesse_defilement: Vitesse de défilement du sol
        reset_mots_actif: Boolean indiquant si le reset est activé
        score: Score final (nombre de mots réussis)
        delai_niveau4: Délai d'affichage des mots au niveau 4 (en ms)
    
    Returns:
        bool: True si sauvegarde réussie
    """
    global dict_joueurs
    
    cle = pseudo.lower()
    
    if cle not in dict_joueurs:
        print(f"[WARNING] Joueur {pseudo} non trouvé")
        return False
    
    joueur = dict_joueurs[cle]
    
    # Vérifier que le monde existe dans l'historique
    if 'historique' not in joueur:
        print(f"[WARNING] Pas d'historique pour {pseudo}")
        return False
    
    if monde not in joueur['historique']:
        print(f"[WARNING] Monde {monde} non trouvé dans l'historique")
        return False
    
    niveau_key = f'niveau_{niveau}'
    if niveau_key not in joueur['historique'][monde]:
        print(f"[WARNING] Niveau {niveau} non trouvé dans {monde}")
        return False
    
    # Créer l'objet essai
    essai = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'erreurs': erreurs_detaillees,  # Liste de {'mot': str, 'lettre_attendue': str, 'lettre_tapee': str}
        'vitesse_frappe': round(vitesse_frappe, 2),
        'vitesse_defilement': round(vitesse_defilement, 2),
        'reset_mots_actif': reset_mots_actif,
        'score': score,
        'delai_niveau4': delai_niveau4
    }
    
    # Ajouter l'essai à l'historique du niveau
    joueur['historique'][monde][niveau_key].append(essai)
    
    # Sauvegarder
    succes = sauvegarder_joueurs()
    if not succes:
        print("ATTENTION: L'essai n'a pas pu être sauvegardé!")
    else:
        print(f"[INFO] Essai enregistré pour {pseudo} - {monde} niveau {niveau}")
    
    return succes


def set_derniere_vitesse(pseudo, valeur):
    """Enregistre la dernière valeur de vitesse entrée pour le joueur (obsolète mais conservée)."""
    # Cette fonction ne fait plus rien car la structure a changé
    pass

def get_statistiques_joueur(pseudo, monde=None, niveau=None):
    """Récupère les statistiques d'un joueur.
    
    Args:
        pseudo: Pseudo du joueur
        monde: Optionnel - filtre par monde
        niveau: Optionnel - filtre par niveau (1-5)
    
    Returns:
        dict: Statistiques calculées depuis l'historique
    """
    cle = pseudo.lower()
    
    if cle not in dict_joueurs:
        return None
    
    joueur = dict_joueurs[cle]
    
    if 'historique' not in joueur:
        return None
    
    stats = {
        'nb_parties': 0,
        'mots_reussis_total': 0,
        'vitesse_moyenne_wpm': 0.0,
        'erreurs_total': 0
    }
    
    # Parcourir l'historique pour calculer les stats
    mondes_a_parcourir = [monde] if monde else joueur['historique'].keys()
    
    for m in mondes_a_parcourir:
        if m not in joueur['historique']:
            continue
        
        niveaux_a_parcourir = [f'niveau_{niveau}'] if niveau else joueur['historique'][m].keys()
        
        for n in niveaux_a_parcourir:
            if n not in joueur['historique'][m]:
                continue
            
            essais = joueur['historique'][m][n]
            stats['nb_parties'] += len(essais)
            
            for essai in essais:
                stats['mots_reussis_total'] += essai.get('score', 0)
                stats['erreurs_total'] += len(essai.get('erreurs', []))
                stats['vitesse_moyenne_wpm'] += essai.get('vitesse_frappe', 0)
    
    # Calculer la moyenne de vitesse
    if stats['nb_parties'] > 0:
        stats['vitesse_moyenne_wpm'] = round(stats['vitesse_moyenne_wpm'] / stats['nb_parties'], 2)
    
    return stats

def get_derniers_parametres_joueur(pseudo):
    """Récupère les derniers paramètres utilisés par le joueur.
    
    Args:
        pseudo: Pseudo du joueur
    
    Returns:
        dict: {'vitesse_defilement': int, 'reset_mots_actif': bool, 'delai_niveau4': int} ou None si pas d'historique
    """
    cle = pseudo.lower()
    
    if cle not in dict_joueurs:
        return None
    
    joueur = dict_joueurs[cle]
    
    if 'historique' not in joueur:
        return None
    
    dernier_essai = None
    dernier_timestamp = None
    
    # Parcourir tous les mondes et niveaux pour trouver l'essai le plus récent
    for monde in joueur['historique'].values():
        for niveau in monde.values():
            if isinstance(niveau, list) and len(niveau) > 0:
                for essai in niveau:
                    timestamp_str = essai.get('timestamp')
                    if timestamp_str:
                        if dernier_timestamp is None or timestamp_str > dernier_timestamp:
                            dernier_timestamp = timestamp_str
                            dernier_essai = essai
    
    if dernier_essai:
        return {
            'vitesse_defilement': dernier_essai.get('vitesse_defilement', 100),
            'reset_mots_actif': dernier_essai.get('reset_mots_actif', True),
            'delai_niveau4': dernier_essai.get('delai_niveau4', 1500)
        }
    
    return None


