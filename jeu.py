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
mechant = Obstacles.Obstacles(Donnees.OBSTACLE_SKIN_CENTIPEDE,
                              Donnees.OBSTACLE_DEPART_X,
                              sol_gauche.get_rect().y+sol_gauche.get_rect().height/4,
                              Donnees.OBSTACLE_TYPE_CENTIPEDE)

# création du mot directement depuis la base de donnée
compteur = 0
niveau="niveau2"
liste_mots=BaseDonnees.df["niveau2"].dropna().tolist()
mot = Mot.Mot.from_string(
    Donnees.MOT_DEPART_X,
    sol_gauche.get_rect().y - 30,
    Donnees.MOT_SYMBOLE,
    Donnees.MOT_COULEUR
)

#### !! Attention !!! ####
# Rmq state_mot : on peut le faire dans n'importe quel ordre

def state_mot(mot, events): 
    """Surveille le clavier et met à jour l'état du mot. 
    Lorsque la lettre du mot est tapée, elle devient grise"""
    for event in events:                            # parcourir les événements passés en paramètre
        if event.type == pygame.KEYDOWN:            # vérifier si une touche est appuyée
            char = str(event.unicode)           # obtenir le caractère de la touche (minuscule)
            if mot._state and mot.symboles:         # vérifier qu'il reste des symboles
                # Parcourir les symboles du mot
                for symbole in mot.symboles:
                    print(f"Symbole char: {symbole._symbole}, couleur: {symbole._couleur}")
                    # Vérifier si le caractère correspond au symbole et qu'il n'est pas déjà gris
                    if symbole._symbole.lower() == char and symbole._couleur != (128, 128, 128):
                        # Changer la couleur en gris (symbole trouvé)
                        symbole._couleur = (128, 128, 128)
                        print(f"Symbole {symbole._symbole} trouvé!")
                        break
                
                # Vérifier si tous les symboles sont gris (mot complété)
                if all(symbole._couleur == (128, 128, 128) for symbole in mot.symboles):
                    mot._state = False  # Marquer le mot comme complété
                    print("Mot complété!")


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
        compteur=compteur+1 
        liste_mots=BaseDonnees.df[niveau].dropna().tolist()
        mot = Mot.Mot.from_string(
                Donnees.MOT_DEPART_X,
                sol_gauche.get_rect().y - 30,
                liste_mots[compteur],
                Donnees.MOT_COULEUR)
    state_mot(mot, events)  # Passer les événements à la fonction


    # Faire défiler le sol
    sol_gauche.defiler(Donnees.SOL_VITESSE)
    sol_droite.defiler(Donnees.SOL_VITESSE)
 
    # Affichage des éléments
    
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