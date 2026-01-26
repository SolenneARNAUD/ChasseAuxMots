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

sol_gauche = Sol.Sol(Donnees.SOL_SKIN,
                    Donnees.SOL_DEPART_X,
                    Donnees.SOL_DEPART_Y)

sol_droite = Sol.Sol(Donnees.SOL_SKIN,
                     Donnees.SOL_DEPART_X + Donnees.WIDTH,
                     Donnees.SOL_DEPART_Y)

man = Personnage.Personnage(Donnees.PERSONNAGE_DEPART_X,
                            sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                            Donnees.PERSONNAGE_SKIN) # Changer position Y par WHEIGHT - 2/3 * hauteursprite
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE)

# création du mot directement depuis la base de donnée
compteur_mot = 0
niveau="niveau2"
num_img=1
frame_counter = 0  # Compteur pour contrôler la vitesse d'animation du dino
liste_mots=BaseDonnees.df["niveau2"].dropna().tolist()
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 100,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)

#### !! Attention !!! ####
# Rmq state_mot : on peut le faire dans n'importe quel ordre

def state_mot(mot, events, reset_on_error=True): 
    """Surveille le clavier et met à jour l'état du mot. 
    Lorsque la lettre du mot est tapée, elle devient grise.
    
    Args:
        mot: L'objet mot à surveiller
        events: Les événements pygame
        reset_on_error: Si True, réinitialise le mot si une mauvaise lettre est tapée
    """
    for event in events:                            # parcourir les événements passés en paramètre
        if event.type == pygame.KEYDOWN:            # vérifier si une touche est appuyée
            char = str(event.unicode)           # obtenir le caractère de la touche (minuscule)
            if mot._state and mot.symboles:         # vérifier qu'il reste des symboles
                # Trouver le premier symbole non gris
                found = False
                for symbole in mot.symboles:
                    if symbole._couleur != (128, 128, 128):
                        # Vérifier si le caractère correspond à ce symbole
                        if symbole._symbole.lower() == char:
                            symbole._couleur = (128, 128, 128)
                            print(f"Symbole {symbole._symbole} trouve!")
                            found = True
                        break
                
                # Si la lettre est fausse et reset_on_error est True
                if not found and reset_on_error:
                    for symbole in mot.symboles:
                        symbole._couleur = Donnees.MOT_COULEUR  # Réinitialiser la couleur
                    print("Lettre incorrecte! Mot reinitialise.")
                
                # Vérifier si tous les symboles sont gris (mot complété)
                if all(symbole._couleur == (128, 128, 128) for symbole in mot.symboles):
                    mot._state = False  # Marquer le mot comme complété
                    print("Mot complete!")


#################### Boucle principale ########################

clock = pygame.time.Clock()

while True:
    events = pygame.event.get()          
    for event in events:
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(f"Touche detectee: {event.unicode}")

    # Implémentation des mots
    if mot._state==False:
        compteur_mot=compteur_mot+1 
        liste_mots=BaseDonnees.df[niveau].dropna().tolist()
        mot = Mot.Mot.from_string(
                Donnees.MOT_DEPART_X,
                sol_gauche.get_rect().y - 100,
                liste_mots[compteur_mot],
                Donnees.MOT_COULEUR)
    state_mot(mot, events)  # Passer les événements à la fonction


    # Faire défiler le sol
    sol_gauche.defiler(Donnees.SOL_VITESSE)
    sol_droite.defiler(Donnees.SOL_VITESSE)
 
    # Gestion de l'animation de l'obstacle
    frame_counter += 1
    if frame_counter >= mechant.animation_delay:
        frame_counter = 0
        if num_img == 1:
            num_img = mechant.nb_images
        else:
            num_img = num_img - 1
    
    sprite_obstacle="images/Mechant/dino"+str(num_img)+".png"
    mechant = Obstacles.Obstacles(sprite_obstacle,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE)
    
    #screen.fill(fenetre.couleur_fond)
    fenetre.afficher_fond(screen)
    sol_gauche.afficher(screen)
    sol_droite.afficher(screen)
    man.afficher(screen)
    mechant.afficher(screen)
    mot.afficher(screen)

    

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(Donnees.FPS)