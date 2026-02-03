import sys, pygame
import Fenetre
import Donnees
import Personnage
import Obstacles
import Mot
import Symbole
import Sol  
import BaseDonnees

pygame.init()

# Créer le screen AVANT la fenêtre (nécessaire pour .convert())
screen = pygame.display.set_mode((Donnees.WIDTH, Donnees.HEIGHT))
fenetre = Fenetre.Fenetre(Donnees.FOND_SKIN)

# Initialisation des sols
sol_gauche = Sol.Sol(Donnees.SOL_SKIN,
                    Donnees.SOL_DEPART_X,
                    Donnees.SOL_DEPART_Y)

sol_droite = Sol.Sol(Donnees.SOL_SKIN,
                     Donnees.SOL_DEPART_X + Donnees.WIDTH,
                     Donnees.SOL_DEPART_Y)

# Initialisation du personnage
man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                            Donnees.PERSONNAGE_SKIN)

# Initialisation du méchant
num_img = 1
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png",
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE,
                              Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
                              Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)

# Initialisation des mots
compteur_mot = 0
total_mots = 10
frame_counter = 0

mot_state_precedent = True  # Suivre l'état précédent du mot

# État de la séquence d'attaque
mechant_move_to_man = False  # Le méchant se déplace vers le man
animation_in_progress = False  # Animation du man en cours
delai_nouveau_mot = 0  # Délai avant d'afficher le nouveau mot
distance_mechant_man = 150  # Distance entre le méchant et le man

mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 100,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)

#################### Boucle principale ########################

clock = pygame.time.Clock()
game_over = False
jeu_demarre = False
niveau = None

while niveau is None:
    
    events = pygame.event.get() 
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    # Fenetre de sélection des niveaux
    niveau = Fenetre.fenetre_niveau(screen, events) 
    clock.tick(60)

# Entrée dans le niveau sélectionné
while True:

    events = pygame.event.get()          
    for event in events:
        if event.type == pygame.QUIT: 
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            jeu_demarre = True

    # GAME OVER : Si collision détectée, afficher écran noir et arrêter le jeu
    if man.check_collision(mechant):
        game_over = True

    if game_over:
        fenetre.afficher_game_over(screen)
        pygame.display.flip()
        continue

    # Niveau réussi : Si tous les mots ont été complétés, afficher écran de réussite
    if compteur_mot >= total_mots:
        fenetre.afficher_fond(screen)
        sol_gauche.afficher(screen)
        sol_droite.afficher(screen)
        man.afficher(screen)
        fenetre.afficher_niveau_reussi(screen)
        pygame.display.flip()
        continue

    # Traitement des entrées clavier pour le mot
    mot.process_input(events)


    # Vérifier si le mot vient de passer de True à False (mot complété)
    if mot_state_precedent and not mot._state:
        # Le mot vient d'être complété ! Activer le déplacement du méchant
        compteur_mot += 1
        liste_mots = BaseDonnees.df["niveau" + str(niveau)].dropna().tolist()
        mechant_move_to_man = True
        animation_in_progress = False
        delai_nouveau_mot = 0
    
        # Génération d'un nouveau mot et respawn du méchant si le mot actuel est complété
        mot = Mot.Mot.from_string(
            Donnees.MOT_DEPART_X,
            sol_gauche.get_rect().y - 100,
            liste_mots[compteur_mot],
            Donnees.MOT_COULEUR)
        
        # Respawn du méchant
        num_img = 1
        frame_counter = 0
        mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png",
                                      Donnees.OBSTACLE_DEPART_X,
                                      sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                                      Donnees.OBSTACLE_TYPE,
                                      Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
                                      Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)

    # Mettre à jour l'état précédent
    mot_state_precedent = mot._state

    # Gestion du déplacement du méchant vers le man
    if mechant_move_to_man:
        distance_x = -man.position_x + mechant.position_x
        
        # Vérifier si le méchant est arrivé à la distance désirée du man
        if abs(distance_x) <= distance_mechant_man:
            mechant.position_x = man.position_x + distance_mechant_man 
            mechant_move_to_man = False
            animation_in_progress = True
            print(mechant.position_x)
            
            # Lancer l'animation du man
            animation_frames = [
                "images/Man/Viking/viking_attaque_1.png",
                "images/Man/Viking/viking_attaque_2.png",
                "images/Man/Viking/viking_attaque_3.png",
                "images/Man/Viking/viking_attaque_4.png",
                "images/Man/Viking/viking_attaque_5.png"
            ]
            man.start_animation(animation_frames, animation_delay=8)
        else:
            # Déplacer le méchant vers le man
            mechant.position_x -= 3
            print(mechant.position_x,"déplacemnt")
    
    # Bloquer le méchant à la bonne position pendant l'animation
    if animation_in_progress and not mechant_move_to_man:
        # Déterminer si le méchant doit être à gauche ou à droite du man
        mechant.position_x = man.position_x + distance_mechant_man
        print(mechant.position_x, man.position_x)
    
    # Gestion du délai et du respawn après animation
    if animation_in_progress:
        # Vérifier si l'animation est terminée
        if not man.is_animating():
            # L'animation est finie, commencer le délai
            delai_nouveau_mot += 1
            
            # Si le délai est écoulé (30 frames = 0.5 secondes à 60 FPS)
            if delai_nouveau_mot >= 30:
                # Créer le nouveau mot et respawn du méchant
                if compteur_mot < total_mots:
                    liste_mots = BaseDonnees.df["niveau" + str(niveau)].dropna().tolist()
                    mot = Mot.Mot.from_string(
                        Donnees.MOT_DEPART_X,
                        sol_gauche.get_rect().y - 100,
                        liste_mots[compteur_mot],
                        Donnees.MOT_COULEUR)
                    
                    # Respawn du méchant
                    num_img = 1
                    frame_counter = 0
                    mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png",
                                                  Donnees.OBSTACLE_DEPART_X,
                                                  sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                                                  Donnees.OBSTACLE_TYPE,
                                                  Donnees.OBSTACLE_VIMAGES_DINO_VOLANT,
                                                  Donnees.OBSTACLE_NIMAGES_DINO_VOLANT)
                
                animation_in_progress = False
                delai_nouveau_mot = 0

    # Mise à jour des positions (déplacement avec le sol)
    if jeu_demarre:
        sol_gauche.defiler(Donnees.SOL_VITESSE)
        sol_droite.defiler(Donnees.SOL_VITESSE)
        mot.update_position(Donnees.SOL_VITESSE)
        mechant.update_position(Donnees.SOL_VITESSE)

        # Gestion de l'animation du méchant
        frame_counter += 1
        if frame_counter >= mechant.animation_delay:
            frame_counter = 0
            if num_img == mechant.nb_images:
                num_img = 1
            else:
                num_img = num_img + 1
            
            # Mise à jour de l'image du méchant
            sprite_obstacle = Donnees.OBSTACLE_SKIN_DINO_VOLANT + str(num_img) + ".png"
            mechant.set_image(sprite_obstacle)

        # Mise à jour de l'animation du personnage
        man.update_animation()


    # Affichage des éléments
    fenetre.afficher_fond(screen)
    sol_gauche.afficher(screen)
    sol_droite.afficher(screen)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)
    fenetre.afficher_bandeau(screen, niveau, compteur_mot, total_mots)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)