import sys, pygame
import Fenetre
import Donnees
import Mot
import BaseDonnees
import Monde
import Obstacles

pygame.init()

# Créer le screen AVANT la fenêtre (nécessaire pour .convert())
screen = pygame.display.set_mode((Donnees.WIDTH, Donnees.HEIGHT))
fenetre = Fenetre.Fenetre(Donnees.FOND_SKIN)

# Menu d'entrée du joueur - Boucle jusqu'à ce qu'un joueur valide soit sélectionné
joueur_valide = False
nom_joueur = None
prenom_joueur = None

while not joueur_valide:
    # Afficher le menu de choix
    choix = Fenetre.fenetre_menu_joueur(screen)
    
    if choix == "nouveau":
        # Créer un nouveau joueur
        while True:
            nom, prenom = Fenetre.fenetre_joueur(screen)
            succes, message = BaseDonnees.ajouter_joueur(nom, prenom)
            
            if succes:
                nom_joueur = nom
                prenom_joueur = prenom
                joueur_valide = True
                print(f"✓ Bienvenue {prenom} {nom}! (Nouveau joueur créé)")
                break
            else:
                # Le joueur existe déjà - afficher message et revenir au choix
                screen.fill(Donnees.COULEUR_FOND)
                font = pygame.font.Font(None, 48)
                font_small = pygame.font.Font(None, 36)
                
                texte_erreur = font.render(message, True, (255, 0, 0))
                texte_retry = font_small.render("Appuyez sur une touche pour continuer...", True, (0, 0, 0))
                
                screen.blit(texte_erreur, (Donnees.WIDTH // 2 - 200, Donnees.HEIGHT // 2 - 30))
                screen.blit(texte_retry, (Donnees.WIDTH // 2 - 180, Donnees.HEIGHT // 2 + 40))
                pygame.display.flip()
                
                # Attendre une touche
                en_attente = True
                while en_attente:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            en_attente = False
                break
    
    elif choix == "existant":
        # Charger un joueur existant
        result = Fenetre.fenetre_charger_joueur(screen)
        
        if result is not None:
            nom_joueur, prenom_joueur = result
            joueur_valide = True
            print(f"✓ Bienvenue {prenom_joueur} {nom_joueur}! (Joueur existant)")
        # else: retourner au menu de choix

print(BaseDonnees.df_joueurs)

#################### Boucle principale ########################

while True:
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

    # Initialisation du monde après la sélection du niveau
    monde = Monde.Monde()
    monde.initialiser_niveau(niveau)
    
    sol_gauche = monde.get_sol_gauche()
    sol_droite = monde.get_sol_droite()
    man = monde.get_personnage()
    mechant = monde.get_mechant()
    mot = monde.get_mot()
    liste_mots = monde.get_liste_mots()
    
    jeu_demarre = False

    # Entrée dans le niveau sélectionné
    while True:

        events = pygame.event.get()          
        for event in events:
            if event.type == pygame.QUIT: 
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                jeu_demarre = True
                if monde.get_temps_debut() is None:
                    monde.set_temps_debut(pygame.time.get_ticks())  # En millisecondes

        # GAME OVER : Si collision détectée, afficher écran noir et arrêter le jeu
        if man.check_collision(mechant):
            game_over = True

        if game_over:
            fenetre.afficher_game_over(screen)
            pygame.display.flip()
            
            # Enregistrer les stats même en cas de défaite
            temps_fin = pygame.time.get_ticks()
            temps_total_ms = temps_fin - monde.get_temps_debut()
            temps_total_min = temps_total_ms / 60000.0
            vitesse_défaite = monde.get_compteur_mot() / temps_total_min if temps_total_min > 0 else 0
            
            BaseDonnees.update_stats_joueur(
                nom_joueur,
                prenom_joueur,
                mots_reussis=monde.get_compteur_mot(),
                vitesse_wpm=vitesse_défaite,
                nb_erreurs=monde.get_nb_erreurs()
            )
            
            # Attendre une touche pour retourner au menu
            retour_menu = False
            while not retour_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        retour_menu = True
            
            # Retourner au menu de sélection de niveau
            niveau = None
            jeu_demarre = False
            game_over = False
            break

        # Niveau réussi : Si tous les mots ont été complétés, afficher écran de réussite
        if monde.get_compteur_mot() >= monde.get_total_mots():
            # Calculer les statistiques une seule fois
            if monde.get_vitesse_finale() is None:
                temps_fin = pygame.time.get_ticks()
                temps_total_ms = temps_fin - monde.get_temps_debut()
                temps_total_min = temps_total_ms / 60000.0  # Convertir en minutes
                vitesse_calc = monde.get_compteur_mot() / temps_total_min if temps_total_min > 0 else 0
                monde.set_vitesse_finale(vitesse_calc)
            
            fenetre.afficher_fond(screen)
            sol_gauche.afficher(screen)
            sol_droite.afficher(screen)
            man.afficher(screen)
            fenetre.afficher_stats_fin_niveau(screen, monde.get_compteur_mot(), monde.get_vitesse_finale(), monde.get_nb_erreurs())
            pygame.display.flip()
            
            # Attendre une touche pour continuer
            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Enregistrer les stats du joueur avant de retourner au menu
                            BaseDonnees.update_stats_joueur(
                                nom_joueur, 
                                prenom_joueur,
                                mots_reussis=monde.get_compteur_mot(),
                                vitesse_wpm=monde.get_vitesse_finale(),
                                nb_erreurs=monde.get_nb_erreurs()
                            )
                            # Retourner au menu de sélection de niveau
                            niveau = None
                            jeu_demarre = False
                            game_over = False
                            attente = False
                        # Ignorer les autres touches
            break  # Sortir de la boucle du jeu pour recommencer la sélection

        # Traitement des entrées clavier pour le mot
        erreur, caracteres_corrects = mot.process_input(events)
        if erreur:
            monde.set_nb_erreurs(monde.get_nb_erreurs() + erreur)
        monde.increment_total_caracteres(caracteres_corrects)


        # Vérifier si le mot vient de passer de True à False (mot complété)
        if monde.get_mot_state_precedent() and not mot._state:
            # Le mot vient d'être complété ! Activer le déplacement du méchant
            monde.set_compteur_mot(monde.get_compteur_mot() + 1)
            monde.set_mechant_move_to_man(True)
            monde.set_animation_in_progress(False)
            monde.set_delai_nouveau_mot(0)
            monde.set_mot_visible(False)
        
            # Génération d'un nouveau mot (seulement si ce n'est pas le dernier)
            if monde.get_compteur_mot() < monde.get_total_mots():
                mot = Mot.Mot.from_string(
                    Donnees.MOT_DEPART_X + 80,
                    sol_gauche.get_rect().y - 100,
                    liste_mots[monde.get_compteur_mot()],
                    Donnees.MOT_COULEUR)
            
            # NE PAS créer de nouvel obstacle ici ! On garde l'obstacle actuel pour l'animation

        # Mettre à jour l'état précédent
        monde.set_mot_state_precedent(mot._state)

        # Gestion du déplacement du méchant vers le man
        if monde.get_mechant_move_to_man():
            distance_x = -man.position_x + mechant.position_x
            
            # Vérifier si le méchant est arrivé à la distance désirée du man
            if abs(distance_x) <= monde.get_distance_mechant_man():
                mechant.position_x = man.position_x + monde.get_distance_mechant_man()
                monde.set_mechant_move_to_man(False)
                monde.set_animation_in_progress(True)
                
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
        
        # Blocker le méchant à la bonne position pendant l'animation
        if monde.get_animation_in_progress() and not monde.get_mechant_move_to_man():
            mechant.position_x = man.position_x + monde.get_distance_mechant_man()
        
        # Gestion du délai et du respawn après animation
        if monde.get_animation_in_progress():
            # Vérifier si l'animation est terminée
            if not man.is_animating():
                # L'animation est finie, commencer le délai
                monde.set_delai_nouveau_mot(monde.get_delai_nouveau_mot() + 1)
                
                # Si le délai est écoulé (30 frames = 0.5 secondes à 60 FPS)
                if monde.get_delai_nouveau_mot() >= 30:
                    # Respawn du méchant à sa position de départ pour le prochain mot
                    if monde.get_compteur_mot() < monde.get_total_mots():
                        monde.set_num_img(1)
                        monde.set_frame_counter(0)
                        mechant = monde.creer_obstacle(monde.get_compteur_mot())
                    
                    monde.set_animation_in_progress(False)
                    monde.set_delai_nouveau_mot(0)
                    monde.set_mot_visible(True)

        # Mise à jour des positions (déplacement avec le sol)
        if jeu_demarre:
            sol_gauche.defiler(Donnees.SOL_VITESSE)
            sol_droite.defiler(Donnees.SOL_VITESSE)
            mot.update_position(Donnees.SOL_VITESSE)
            mechant.update_position(Donnees.SOL_VITESSE)

            # Gestion de l'animation du méchant
            frame_counter = monde.get_frame_counter() + 1
            monde.set_frame_counter(frame_counter)
            
            if frame_counter >= mechant.animation_delay:
                monde.set_frame_counter(0)
                num_img = monde.get_num_img()
                if num_img == mechant.nb_images:
                    monde.set_num_img(1)
                else:
                    monde.set_num_img(num_img + 1)
                
                # Mise à jour de l'image du méchant avec le chemin de l'obstacle actuel
                sprite_obstacle = f"{monde.get_obstacle_actuel_config()['chemin_base']}{monde.get_num_img()}.png"
                mechant.set_image(sprite_obstacle)

            # Mise à jour de l'animation du personnage
            man.update_animation()


        # Affichage des éléments
        fenetre.afficher_fond(screen)
        sol_gauche.afficher(screen)
        sol_droite.afficher(screen)
        man.afficher(screen)
        mechant.afficher(screen)
        if monde.get_mot_visible():
            mot.afficher(screen)
        fenetre.afficher_bandeau(screen, niveau, monde.get_compteur_mot(), monde.get_total_mots())

        # Mise à jour de l'affichage
        pygame.display.flip()
        clock.tick(Donnees.FPS)