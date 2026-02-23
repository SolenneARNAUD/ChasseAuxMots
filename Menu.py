import Donnees
import pygame as pg
import sys
import BaseDonnees
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Backend sans interface graphique
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime


class Menu:
    """Classe regroupant tous les menus du jeu."""
    
    @staticmethod
    def generer_graphique_stats(pseudo, fichier_sortie=None):
        """Génère un graphique matplotlib avec l'historique de vitesse et précision (10 dernières parties).
        
        Args:
            pseudo: Pseudo du joueur
            fichier_sortie: Chemin du fichier de sortie (optionnel). Si None, utilise TEMP/stats_{pseudo}.png
        
        Returns:
            str: Chemin du fichier image généré, ou None si erreur
        """
        # Récupérer l'historique complet
        historique = BaseDonnees.get_historique_chronologique(pseudo)
        
        if not historique or len(historique) < 2:
            # Pas assez de données pour un graphique
            return None
        
        # Prendre seulement les 10 dernières parties
        historique = historique[-10:]
        
        # Extraire les données
        timestamps = []
        vitesses = []
        precisions = []
        
        for partie in historique:
            try:
                # Parser le timestamp
                dt = datetime.strptime(partie['timestamp'], '%Y-%m-%d %H:%M:%S')
                timestamps.append(dt)
                vitesses.append(partie['vitesse_frappe'])
                precisions.append(partie['precision'])
            except:
                continue
        
        if len(timestamps) < 2:
            return None
        
        # Créer les numéros de parties (N-9, N-8, ..., N-1, N)
        nb_parties = len(timestamps)
        parties_labels = [f"N-{nb_parties - i - 1}" if i < nb_parties - 1 else "N" for i in range(nb_parties)]
        positions = list(range(nb_parties))
        
        # Créer le graphique avec un seul axe
        fig, ax1 = plt.subplots(figsize=(12, 7))
        fig.suptitle(f'Historique des 10 dernières parties - {pseudo}', fontsize=16, fontweight='bold')
        
        # Axe gauche : Précision
        color_precision = '#A23B72'
        ax1.set_xlabel('Partie', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Précision (%)', fontsize=12, fontweight='bold', color=color_precision)
        line1 = ax1.plot(positions, precisions, marker='s', linestyle='-', color=color_precision, 
                        linewidth=2.5, markersize=7, label='Précision')
        ax1.tick_params(axis='y', labelcolor=color_precision)
        ax1.set_ylim(0, 105)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Axe droit : Vitesse de frappe
        ax2 = ax1.twinx()
        color_vitesse = '#2E86AB'
        ax2.set_ylabel('Vitesse (caractères/s)', fontsize=12, fontweight='bold', color=color_vitesse)
        line2 = ax2.plot(positions, vitesses, marker='o', linestyle='-', color=color_vitesse, 
                        linewidth=2.5, markersize=7, label='Vitesse')
        ax2.tick_params(axis='y', labelcolor=color_vitesse)
        ax2.set_ylim(bottom=0)
        
        # Légende combinée
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=10)
        
        # Configurer l'axe X avec les labels de parties
        ax1.set_xticks(positions)
        ax1.set_xticklabels(parties_labels)
        ax1.set_xlim(-0.5, nb_parties - 0.5)
        
        # Ajuster l'espacement
        plt.tight_layout()
        
        # Sauvegarder le graphique
        if fichier_sortie is None:
            temp_dir = tempfile.gettempdir()
            fichier_sortie = os.path.join(temp_dir, "ChasseAuxMots", f"stats_{pseudo}.png")
            os.makedirs(os.path.dirname(fichier_sortie), exist_ok=True)
        
        # Supprimer l'ancien fichier s'il existe pour éviter les problèmes de cache
        if os.path.exists(fichier_sortie):
            try:
                os.remove(fichier_sortie)
            except Exception as e:
                print(f"[WARNING] Impossible de supprimer l'ancien graphique: {e}")
        
        try:
            plt.savefig(fichier_sortie, dpi=100, bbox_inches='tight')
            plt.close(fig)
            return fichier_sortie
        except Exception as e:
            print(f"[ERROR] Impossible de sauvegarder le graphique: {e}")
            plt.close(fig)
            return None
    
    @staticmethod
    def fenetre_parametres(screen, vitesse_actuelle, reset_on_error_actuel=True, total_mots_actuel=20, joueur=None, bibliotheques_actuelles=None):
        """
        Affiche une fenêtre modale pour configurer les paramètres du jeu.
        Retourne un tuple (vitesse_pourcentage, reset_on_error, total_mots, bibliotheques) ou None si annulé.
        """
        vitesse_str = ""
        vitesse_affichee = str(vitesse_actuelle)
        total_mots_str = ""
        total_mots_affiche = str(total_mots_actuel)
        reset_on_error = reset_on_error_actuel
        
        # Gérer la sélection multiple de bibliothèques
        if bibliotheques_actuelles is None:
            bibliotheques_selectionnees = {"dinosaure"}
        elif isinstance(bibliotheques_actuelles, str):
            bibliotheques_selectionnees = {bibliotheques_actuelles}
        else:
            bibliotheques_selectionnees = set(bibliotheques_actuelles)
        
        clock = pg.time.Clock()
        input_active = False
        input_mots_active = False
        
        # Charger la liste des bibliothèques
        bibliotheques = BaseDonnees.lister_bibliotheques()
        scroll_offset = 0
        
        # Division de l'écran en 3 zones
        zone_titre_height = Donnees.HEIGHT // Donnees.PARAMS_ZONE_TITRE_RATIO
        zone_params_height = Donnees.HEIGHT // Donnees.PARAMS_ZONE_PARAMS_RATIO
        zone_boutons_y = zone_titre_height + zone_params_height
        
        # Zone du milieu : calcul de l'espacement vertical
        # X pixels vides, Y pixels texte, X pixels vides, Y pixels texte, X pixels vides
        param_height = Donnees.PARAMS_PARAM_HEIGHT
        spacing = (zone_params_height - 4 * param_height) // 5  # Espacement X pour 4 paramètres
        
        # Position verticale des paramètres dans la zone milieu
        param1_y = zone_titre_height + spacing
        param2_y = param1_y + param_height + spacing
        param3_y = param2_y + param_height + spacing
        param4_y = param3_y + param_height + spacing
        
        # Alignement horizontal : labels à gauche, inputs à droite alignés
        label_x = Donnees.WIDTH // Donnees.PARAMS_LABEL_X_RATIO
        input_x = Donnees.WIDTH // 2 + Donnees.PARAMS_INPUT_X_OFFSET
        
        # Zones interactives
        input_box = pg.Rect(input_x, param1_y, Donnees.PARAMS_INPUT_BOX_WIDTH, Donnees.PARAMS_INPUT_BOX_HEIGHT)
        checkbox_rect = pg.Rect(input_x + Donnees.PARAMS_CHECKBOX_OFFSET_X, param2_y + Donnees.PARAMS_CHECKBOX_OFFSET_Y, 
                               Donnees.PARAMS_CHECKBOX_SIZE, Donnees.PARAMS_CHECKBOX_SIZE)
        input_mots_box = pg.Rect(input_x, param3_y, Donnees.PARAMS_INPUT_BOX_WIDTH, Donnees.PARAMS_INPUT_BOX_HEIGHT)
        
        # Zone de scroll pour les bibliothèques (avec offset pour le label)
        biblio_label_height = 25  # Hauteur réservée pour le label "Bibliothèque"
        biblio_zone_x = label_x
        biblio_zone_y = param4_y + biblio_label_height  # Décaler vers le bas pour le label
        biblio_zone_width = Donnees.WIDTH - 2 * label_x
        biblio_zone_height = param_height - biblio_label_height  # Réduire la hauteur disponible
        biblio_item_height = 30
        max_visible_items = max(1, biblio_zone_height // biblio_item_height)
        
        # Boutons en bas
        bouton_w = Donnees.PARAMS_BOUTON_WIDTH
        bouton_h = Donnees.PARAMS_BOUTON_HEIGHT
        bouton_spacing = Donnees.PARAMS_BOUTON_SPACING
        total_boutons_width = 2 * bouton_w + bouton_spacing
        bouton_y = zone_boutons_y + (Donnees.HEIGHT - zone_boutons_y) // 2 - bouton_h // 2
        
        bouton_valider = pg.Rect(Donnees.WIDTH // 2 - total_boutons_width // 2, bouton_y, bouton_w, bouton_h)
        bouton_retour = pg.Rect(Donnees.WIDTH // 2 - total_boutons_width // 2 + bouton_w + bouton_spacing, bouton_y, bouton_w, bouton_h)
        
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                
                # Gestion de la molette pour le scroll
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Molette vers le haut
                        scroll_offset = max(0, scroll_offset - 1)
                    elif event.button == 5:  # Molette vers le bas
                        max_scroll = max(0, len(bibliotheques) - max_visible_items)
                        scroll_offset = min(max_scroll, scroll_offset + 1)
                
                # Clic sur la zone de saisie
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche uniquement
                    if input_box.collidepoint(event.pos):
                        input_active = True
                        input_mots_active = False
                        vitesse_str = ""
                    elif input_mots_box.collidepoint(event.pos):
                        input_mots_active = True
                        input_active = False
                        total_mots_str = ""
                    elif checkbox_rect.collidepoint(event.pos):
                        reset_on_error = not reset_on_error
                    else:
                        # Vérifier si clic sur une bibliothèque (sélection multiple)
                        for i, biblio in enumerate(bibliotheques[scroll_offset:scroll_offset + max_visible_items]):
                            actual_index = i + scroll_offset
                            item_y = biblio_zone_y + i * biblio_item_height
                            checkbox_biblio_rect = pg.Rect(biblio_zone_x + 10, item_y + 5, 20, 20)
                            if checkbox_biblio_rect.collidepoint(event.pos):
                                biblio_id = bibliotheques[actual_index]['id']
                                # Toggle: ajouter ou retirer la bibliothèque
                                if biblio_id in bibliotheques_selectionnees:
                                    bibliotheques_selectionnees.discard(biblio_id)  # Retirer
                                else:
                                    bibliotheques_selectionnees.add(biblio_id)  # Ajouter
                                break
                    
                    if bouton_retour.collidepoint(event.pos):
                        return None
                    elif bouton_valider.collidepoint(event.pos):
                        try:
                            val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                        except Exception:
                            val = vitesse_actuelle
                        val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                        vitesse_affichee = str(val)
                        
                        try:
                            val_mots = int(total_mots_str) if total_mots_str else total_mots_actuel
                        except Exception:
                            val_mots = total_mots_actuel
                        val_mots = max(Donnees.TOTAL_MOTS_MIN, min(Donnees.TOTAL_MOTS_MAX, val_mots))
                        total_mots_affiche = str(val_mots)
                        
                        # Sauvegarder la dernière valeur pour le joueur
                        if joueur is not None:
                            try:
                                pseudo_j = joueur
                                val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                BaseDonnees.set_derniere_vitesse(pseudo_j, val_wpm)
                            except Exception:
                                pass
                        
                        return (int(val), reset_on_error, int(val_mots), list(bibliotheques_selectionnees))
                
                if event.type == pg.KEYDOWN:
                    if input_active:
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            try:
                                val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                            except Exception:
                                val = vitesse_actuelle
                            val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                            vitesse_affichee = str(val)
                            
                            try:
                                val_mots = int(total_mots_str) if total_mots_str else total_mots_actuel
                            except Exception:
                                val_mots = total_mots_actuel
                            val_mots = max(Donnees.TOTAL_MOTS_MIN, min(Donnees.TOTAL_MOTS_MAX, val_mots))
                            total_mots_affiche = str(val_mots)
                            
                            if joueur is not None:
                                try:
                                    pseudo_j = joueur
                                    val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                    BaseDonnees.set_derniere_vitesse(pseudo_j, val_wpm)
                                except Exception:
                                    pass
                            
                            return (int(val), reset_on_error, int(val_mots), list(bibliotheques_selectionnees))
                        elif event.key == pg.K_ESCAPE:
                            return None
                        elif event.key == pg.K_BACKSPACE:
                            vitesse_str = vitesse_str[:-1]
                        elif event.unicode.isdigit() and len(vitesse_str) < 3:
                            vitesse_str += event.unicode
                    elif input_mots_active:
                        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                            try:
                                val = int(vitesse_str) if vitesse_str else vitesse_actuelle
                            except Exception:
                                val = vitesse_actuelle
                            val = max(Donnees.VITESSE_POURCENTAGE_MIN, min(Donnees.VITESSE_POURCENTAGE_MAX, val))
                            vitesse_affichee = str(val)
                            
                            try:
                                val_mots = int(total_mots_str) if total_mots_str else total_mots_actuel
                            except Exception:
                                val_mots = total_mots_actuel
                            val_mots = max(Donnees.TOTAL_MOTS_MIN, min(Donnees.TOTAL_MOTS_MAX, val_mots))
                            total_mots_affiche = str(val_mots)
                            
                            if joueur is not None:
                                try:
                                    pseudo_j = joueur
                                    val_wpm = (val / 100.0) * Donnees.WPM_BASE_CONVERSION
                                    BaseDonnees.set_derniere_vitesse(pseudo_j, val_wpm)
                                except Exception:
                                    pass
                            
                            return (int(val), reset_on_error, int(val_mots), list(bibliotheques_selectionnees))
                        elif event.key == pg.K_ESCAPE:
                            return None
                        elif event.key == pg.K_BACKSPACE:
                            total_mots_str = total_mots_str[:-1]
                        elif event.unicode.isdigit() and len(total_mots_str) < 3:
                            total_mots_str += event.unicode
                    else:
                        if event.key == pg.K_ESCAPE:
                            return None
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            font_titre = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_TITRE)
            font_label = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_LABEL)
            font_input = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_INPUT)
            font_bouton = pg.font.Font(None, Donnees.PARAMS_FENETRE_POLICE_BOUTON)
            
            # === ZONE TITRE ===
            titre = font_titre.render("Paramètres", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH // 2 - titre.get_width() // 2, zone_titre_height // 2 - titre.get_height() // 2))
            
            # Ligne de séparation après le titre
            pg.draw.line(screen, Donnees.PARAMS_LIGNE_SEPARATION_COULEUR, 
                        (Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_titre_height - Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        (5 * Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_titre_height - Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            
            # === ZONE PARAMÈTRES ===
            
            # Paramètre 1 : Vitesse de défilement
            label_vitesse = font_label.render("Vitesse de défilement", True, Donnees.COULEUR_NOIR)
            screen.blit(label_vitesse, (label_x, param1_y + 10))
            
            # Input box vitesse
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, input_box)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR if not input_active else Donnees.PARAMS_INPUT_BOX_COULEUR_ACTIVE, 
                        input_box, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if input_active:
                texte_vitesse = font_input.render(vitesse_str + "|", True, Donnees.COULEUR_NOIR)
            else:
                texte_vitesse = font_input.render(vitesse_affichee + " %", True, (100, 100, 100))
            
            screen.blit(texte_vitesse, (input_box.centerx - texte_vitesse.get_width() // 2, 
                                        input_box.centery - texte_vitesse.get_height() // 2))
            
            # Paramètre 2 : Reset du mot après erreur
            label_reset = font_label.render("Reset du mot après erreur", True, Donnees.COULEUR_NOIR)
            screen.blit(label_reset, (label_x, param2_y + 10))
            
            # Checkbox
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, checkbox_rect)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, checkbox_rect, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if reset_on_error:
                # Checkmark
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE, 
                            (checkbox_rect.left + Donnees.PARAMS_CHECKMARK_MARGIN_LEFT, checkbox_rect.centery),
                            (checkbox_rect.centerx - Donnees.PARAMS_CHECKMARK_MARGIN_RIGHT, checkbox_rect.bottom - Donnees.PARAMS_CHECKMARK_MARGIN_BOTTOM), 
                            Donnees.PARAMS_CHECKMARK_EPAISSEUR)
                pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE,
                            (checkbox_rect.centerx - Donnees.PARAMS_CHECKMARK_MARGIN_RIGHT, checkbox_rect.bottom - Donnees.PARAMS_CHECKMARK_MARGIN_BOTTOM),
                            (checkbox_rect.right - Donnees.PARAMS_CHECKMARK_MARGIN_LEFT, checkbox_rect.top + Donnees.PARAMS_CHECKMARK_MARGIN_TOP), 
                            Donnees.PARAMS_CHECKMARK_EPAISSEUR)
            
            # Paramètre 3 : Nombre de mots par partie
            label_mots = font_label.render("Nombre de mots par partie", True, Donnees.COULEUR_NOIR)
            screen.blit(label_mots, (label_x, param3_y + 10))
            
            # Input box nombre de mots
            pg.draw.rect(screen, Donnees.COULEUR_BLANC, input_mots_box)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR if not input_mots_active else Donnees.PARAMS_INPUT_BOX_COULEUR_ACTIVE, 
                        input_mots_box, Donnees.PARAMS_INPUT_BOX_BORDURE)
            
            if input_mots_active:
                texte_mots = font_input.render(total_mots_str + "|", True, Donnees.COULEUR_NOIR)
            else:
                texte_mots = font_input.render(total_mots_affiche, True, (100, 100, 100))
            
            screen.blit(texte_mots, (input_mots_box.centerx - texte_mots.get_width() // 2, 
                                     input_mots_box.centery - texte_mots.get_height() // 2))
            
            # Paramètre 4 : Bibliothèque
            label_biblio = font_label.render("Bibliothèque", True, Donnees.COULEUR_NOIR)
            screen.blit(label_biblio, (label_x, param4_y - 5))
            
            # Afficher les bibliothèques avec scroll
            font_biblio = pg.font.Font(None, 28)
            for i, biblio in enumerate(bibliotheques[scroll_offset:scroll_offset + max_visible_items]):
                actual_index = i + scroll_offset
                item_y = biblio_zone_y + i * biblio_item_height
                
                # Checkbox (carré à cocher)
                checkbox_biblio_rect = pg.Rect(biblio_zone_x + 10, item_y + 5, 20, 20)
                pg.draw.rect(screen, Donnees.COULEUR_BLANC, checkbox_biblio_rect)
                pg.draw.rect(screen, Donnees.COULEUR_NOIR, checkbox_biblio_rect, 2)
                
                # Si sélectionné, afficher une checkmark
                if biblio['id'] in bibliotheques_selectionnees:
                    # Checkmark style V
                    pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE, 
                                (checkbox_biblio_rect.left + 4, checkbox_biblio_rect.centery),
                                (checkbox_biblio_rect.centerx - 2, checkbox_biblio_rect.bottom - 4), 
                                3)
                    pg.draw.line(screen, Donnees.COULEUR_VERT_FONCE,
                                (checkbox_biblio_rect.centerx - 2, checkbox_biblio_rect.bottom - 4),
                                (checkbox_biblio_rect.right - 4, checkbox_biblio_rect.top + 4), 
                                3)
                
                # Nom de la bibliothèque
                texte_biblio = font_biblio.render(biblio['nom'], True, Donnees.COULEUR_NOIR)
                screen.blit(texte_biblio, (biblio_zone_x + 40, item_y + 5))
            
            # Indicateur de scroll si nécessaire
            if len(bibliotheques) > max_visible_items:
                scroll_info = font_biblio.render(f"({scroll_offset + 1}-{min(scroll_offset + max_visible_items, len(bibliotheques))}/{len(bibliotheques)})", 
                                                 True, (120, 120, 120))
                screen.blit(scroll_info, (biblio_zone_x + biblio_zone_width - 80, param4_y - 5))
            
            # Ligne de séparation avant les boutons
            pg.draw.line(screen, Donnees.PARAMS_LIGNE_SEPARATION_COULEUR, 
                        (Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_boutons_y + Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        (5 * Donnees.WIDTH // Donnees.PARAMS_LIGNE_SEPARATION_RATIO, zone_boutons_y + Donnees.PARAMS_LIGNE_SEPARATION_OFFSET), 
                        Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            
            # === ZONE BOUTONS ===
            
            # Bouton Valider
            pg.draw.rect(screen, Donnees.PARAMS_BOUTON_COULEUR_VALIDER, bouton_valider)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_valider, Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            texte_valider = font_bouton.render("Valider", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_valider, (bouton_valider.centerx - texte_valider.get_width() // 2,
                                       bouton_valider.centery - texte_valider.get_height() // 2))
            
            # Bouton Retour
            pg.draw.rect(screen, Donnees.PARAMS_BOUTON_COULEUR_RETOUR, bouton_retour)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_retour, Donnees.PARAMS_LIGNE_SEPARATION_EPAISSEUR)
            texte_retour = font_bouton.render("Retour", True, Donnees.COULEUR_BLANC)
            screen.blit(texte_retour, (bouton_retour.centerx - texte_retour.get_width() // 2,
                                      bouton_retour.centery - texte_retour.get_height() // 2))
            
            pg.display.flip()
            clock.tick(Donnees.FPS)

    @staticmethod
    def _calculer_rect_niveau(index):
        """
        Calcule le rectangle d'un bouton de niveau. 
        NB : on a ajouté un _ pour indiquer que c'est une fonction interne à ce module.
        """
        largeur_totale = (Donnees.NB_NIVEAUX * Donnees.NIVEAU_BOUTON_TAILLE + 
                         (Donnees.NB_NIVEAUX - 1) * Donnees.NIVEAU_BOUTON_ESPACEMENT)
        start_x = (Donnees.WIDTH - largeur_totale) // 2
        y = Donnees.HEIGHT // 2 - Donnees.NIVEAU_BOUTON_TAILLE // 2
        
        return pg.Rect(
            start_x + index * (Donnees.NIVEAU_BOUTON_TAILLE + Donnees.NIVEAU_BOUTON_ESPACEMENT),
            y,
            Donnees.NIVEAU_BOUTON_TAILLE,
            Donnees.NIVEAU_BOUTON_TAILLE
        )

    @staticmethod
    def fenetre_niveau(screen, joueur=None, vitesse_par_defaut=None, reset_on_error_defaut=None, total_mots_defaut=None, monde_choisi=None, bibliotheque_defaut=None):
        """
        Affiche la fenêtre de sélection des niveaux avec un bouton paramètres.
        Retourne un tuple (niveau_selectionne, vitesse_pourcentage, reset_on_error, total_mots, bibliotheque).
        Retourne None si l'utilisateur appuie sur Échap (retour en arrière).
        Gère sa propre boucle jusqu'à ce qu'un niveau soit sélectionné.
        """
        clock = pg.time.Clock()
        niveau_selectionne = None
        niveau_survole = 0  # Index du niveau actuellement sélectionné au clavier (0-4)
        vitesse_pourcentage = vitesse_par_defaut if vitesse_par_defaut is not None else Donnees.VITESSE_POURCENTAGE_PAR_DEFAUT
        reset_on_error = reset_on_error_defaut if reset_on_error_defaut is not None else Donnees.RESET_ON_ERROR_PAR_DEFAUT
        total_mots = total_mots_defaut if total_mots_defaut is not None else Donnees.TOTAL_MOTS
        
        # Gérer la bibliothèque (convertir en liste si nécessaire)
        if bibliotheque_defaut is not None:
            if isinstance(bibliotheque_defaut, str):
                bibliotheque = [bibliotheque_defaut]
            else:
                bibliotheque = list(bibliotheque_defaut)
        else:
            biblio_active = BaseDonnees.BIBLIOTHEQUE_ACTIVE
            if isinstance(biblio_active, str):
                bibliotheque = [biblio_active]
            else:
                bibliotheque = list(biblio_active) if biblio_active else ["dinosaure"]
        
        # Charger le fond du monde sélectionné avec transparence
        fond_surface = None
        if monde_choisi is not None:
            try:
                from BaseDonnees import Univers
                chemin_background = Univers[monde_choisi]["background"]["chemin"]
                # Charger les images de fond (de 7 à 1, du plus éloigné au sol)
                fond_images = []
                for i in range(7, 0, -1):
                    chemin = Donnees.resource_path(chemin_background + f"{i}.png")
                    img = pg.image.load(chemin).convert_alpha()
                    # Redimensionner pour couvrir toute la fenêtre
                    img = pg.transform.scale(img, (Donnees.WIDTH, Donnees.HEIGHT))
                    fond_images.append(img)
                
                # Créer une surface combinée avec toutes les couches
                fond_surface = pg.Surface((Donnees.WIDTH, Donnees.HEIGHT))
                for img in fond_images:
                    fond_surface.blit(img, (0, 0))
                
                # Appliquer la transparence (alpha = 128 pour 50% de transparence)
                fond_surface.set_alpha(128)
            except Exception as e:
                print(f"Erreur lors du chargement du fond: {e}")
                fond_surface = None
        
        # Définir le bouton paramètres (en bas à gauche)
        btn_params = pg.Rect(
            30,
            Donnees.HEIGHT - 80,
            Donnees.NIVEAU_BOUTON_PARAMS_WIDTH,
            50
        )
        
        # Bouton Retour (en bas à droite)
        bouton_retour = pg.Rect(Donnees.WIDTH - 230, Donnees.HEIGHT - 80, 200, 50)
        
        while niveau_selectionne is None:
            events = pg.event.get()
            
            # Survol avec la souris
            mouse_pos = pg.mouse.get_pos()
            for i in range(Donnees.NB_NIVEAUX):
                rect = Menu._calculer_rect_niveau(i)
                if rect.collidepoint(mouse_pos):
                    niveau_survole = i
                    break
            
            ## Gestion des événements ##
            for event in events:
                # Event 1 : Quitter le jeu
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None  # Retour en arrière
                    
                    # Navigation au clavier
                    if event.key == pg.K_LEFT:
                        niveau_survole = (niveau_survole - 1) % Donnees.NB_NIVEAUX
                    elif event.key == pg.K_RIGHT:
                        niveau_survole = (niveau_survole + 1) % Donnees.NB_NIVEAUX
                    elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        niveau_selectionne = niveau_survole + 1
                        break
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    position = event.pos
                    
                    # Vérifier le clic sur le bouton retour
                    if bouton_retour.collidepoint(position):
                        return None
                    
                    # Vérifier le clic sur le bouton paramètres
                    if btn_params.collidepoint(position):
                        resultat = Menu.fenetre_parametres(screen, vitesse_pourcentage, reset_on_error, total_mots, joueur, bibliotheque)
                        if resultat is not None:
                            vitesse_pourcentage, reset_on_error, total_mots, bibliotheque = resultat
                    
                    # Event 2 : Clic sur un niveau
                    for i in range(Donnees.NB_NIVEAUX):
                        rect = Menu._calculer_rect_niveau(i)
                        if rect.collidepoint(position): # Test si le clic est dans le rectangle du niveau
                            niveau_selectionne = i + 1 # Le niveau a été sélectionné > on sort de la boucle
                            break
            
            ## Affichage ##
            # Affichage 1 : Fond
            screen.fill(Donnees.COULEUR_FOND)
            
            # Afficher le fond du monde sélectionné avec transparence
            if fond_surface is not None:
                screen.blit(fond_surface, (0, 0))
            
            font = pg.font.Font(None, Donnees.NIVEAU_TITRE_POLICE)
            font_small = pg.font.Font(None, Donnees.NIVEAU_POLICE_INFO)
            
            # Titre
            titre = font.render("Sélectionnez un niveau", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH//2 - titre.get_width()//2, Donnees.NIVEAU_TITRE_Y))
            
            # Affichage 2 : Boutons de niveaux
            for i in range(Donnees.NB_NIVEAUX):
                rect = Menu._calculer_rect_niveau(i)
                
                # Couleur de fond (surbrillance si sélectionné au clavier)
                couleur_fond = Donnees.NIVEAU_BOUTON_COULEUR_FOND
                if i == niveau_survole:
                    couleur_fond = (220, 220, 220)  # Couleur plus claire pour la sélection
                
                # Dessin du carré
                pg.draw.rect(screen, couleur_fond, rect)
                
                # Bordure plus épaisse si sélectionné
                epaisseur = Donnees.NIVEAU_BOUTON_EPAISSEUR_BORDURE
                if i == niveau_survole:
                    epaisseur = 5
                pg.draw.rect(screen, Donnees.NIVEAU_BOUTON_COULEUR_BORDURE, rect, epaisseur)
                
                # Numéro du niveau
                texte = font.render(str(i + 1), True, Donnees.NIVEAU_BOUTON_COULEUR_BORDURE)
                texte_rect = texte.get_rect(center=rect.center)
                screen.blit(texte, texte_rect)
            
            # Affichage 3 : Bouton paramètres (en bas à gauche)
            pg.draw.rect(screen, Donnees.COULEUR_BLEU_BOUTON, btn_params)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, btn_params, 3)
            texte_params = font_small.render("Paramètres", True, Donnees.COULEUR_BLANC)
            texte_params_rect = texte_params.get_rect(center=btn_params.center)
            screen.blit(texte_params, texte_params_rect)
            
            # Bouton Retour (en bas à droite)
            font_bouton = pg.font.Font(None, 40)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, Donnees.COULEUR_NOIR, bouton_retour, 3)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)
            
            # Affichage 4 : Vitesse actuelle (au-dessus du bouton paramètres)
            info_vitesse = font_small.render(f"Vitesse: {vitesse_pourcentage}%", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_vitesse, (Donnees.NIVEAU_INFO_MARGIN, Donnees.HEIGHT - 120))
            
            # Affichage 5 : Mode reset (au-dessus du bouton paramètres)
            reset_mode = "Reset: OUI" if reset_on_error else "Reset: NON"
            reset_color = Donnees.COULEUR_VERT_FONCE if reset_on_error else Donnees.COULEUR_ROUGE_FONCE
            info_reset = font_small.render(reset_mode, True, reset_color)
            screen.blit(info_reset, (Donnees.NIVEAU_INFO_MARGIN, Donnees.HEIGHT - 100))
            
            # Affichage 6 : Nombre de mots (au-dessus du bouton paramètres)
            info_mots = font_small.render(f"Mots: {total_mots}", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_mots, (Donnees.NIVEAU_INFO_MARGIN, Donnees.HEIGHT - 80))
            
            # Affichage 7 : Message navigation
            info_echap = font_small.render("Flèches: navigation | Entrée: valider", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_echap, (Donnees.WIDTH // 2 - info_echap.get_width() // 2, Donnees.HEIGHT - 30))
            
            pg.display.flip()
            clock.tick(Donnees.FPS)
        
        return niveau_selectionne, vitesse_pourcentage, reset_on_error, total_mots, bibliotheque

    @staticmethod
    def selection_monde(screen):
        """
        Affiche une fenêtre de sélection des mondes avec 4 carrés représentant :
        - Foret bleue
        - Foret violette
        - Vallée verte
        - Foret aux champignons
        
        Retourne la clé univers du monde sélectionné (str) ex: 'foret_bleue'.
        Retourne None si l'utilisateur appuie sur Échap (retour en arrière).
        """
        clock = pg.time.Clock()
        monde_selectionne = None
        monde_survole = 0  # Index du monde actuellement sélectionné au clavier (0-3)
        
        # Configuration des mondes avec leurs noms d'affichage et clés univers
        mondes = [
            {"nom": ["Forêt Bleue"], "cle": "foret_bleue", "couleur": (100, 150, 200)},
            {"nom": ["Forêt Violette"], "cle": "foret_violette", "couleur": (150, 100, 180)},
            {"nom": ["Vallée Verte"], "cle": "vallee_verte", "couleur": (100, 180, 100)},
            {"nom": ["Forêt", "Champignons"], "cle": "foret_au_champignon", "couleur": (200, 150, 100)}
        ]
        
        # Calcul de la position des carrés (2x2 grid)
        taille_carre = 150
        espacement = 50
        
        # Position de départ pour centrer la grille
        largeur_grille = 2 * taille_carre + espacement
        hauteur_grille = 2 * taille_carre + espacement
        start_x = (Donnees.WIDTH - largeur_grille) // 2
        start_y = (Donnees.HEIGHT - hauteur_grille) // 2 + 30  # Décalé vers le bas pour le titre
        
        # Créer les rectangles pour chaque monde
        rectangles_mondes = []
        for i in range(4):
            row = i // 2
            col = i % 2
            x = start_x + col * (taille_carre + espacement)
            y = start_y + row * (taille_carre + espacement)
            rectangles_mondes.append(pg.Rect(x, y, taille_carre, taille_carre))
        
        # Bouton Retour (en bas à droite)
        bouton_retour = pg.Rect(Donnees.WIDTH - 230, Donnees.HEIGHT - 80, 200, 50)
        
        while monde_selectionne is None:
            events = pg.event.get()
            
            # Survol avec la souris
            mouse_pos = pg.mouse.get_pos()
            for i, rect in enumerate(rectangles_mondes):
                if rect.collidepoint(mouse_pos):
                    monde_survole = i
                    break
            
            # Gestion des événements
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None  # Retour en arrière
                    
                    # Navigation au clavier (grille 2x2)
                    row = monde_survole // 2
                    col = monde_survole % 2
                    
                    if event.key == pg.K_LEFT:
                        col = (col - 1) % 2
                    elif event.key == pg.K_RIGHT:
                        col = (col + 1) % 2
                    elif event.key == pg.K_UP:
                        row = (row - 1) % 2
                    elif event.key == pg.K_DOWN:
                        row = (row + 1) % 2
                    elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        monde_selectionne = mondes[monde_survole]["cle"]
                        break
                    
                    monde_survole = row * 2 + col
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    position = event.pos
                    
                    # Vérifier le clic sur le bouton retour
                    if bouton_retour.collidepoint(position):
                        return None
                    
                    # Vérifier le clic sur un des carrés de monde
                    for i, rect in enumerate(rectangles_mondes):
                        if rect.collidepoint(position):
                            monde_selectionne = mondes[i]["cle"]
                            break
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Polices
            font_titre = pg.font.Font(None, 48)
            font_monde = pg.font.Font(None, 28)
            font_info = pg.font.Font(None, 24)
            
            # Titre
            titre = font_titre.render("Sélectionnez un monde", True, Donnees.COULEUR_NOIR)
            screen.blit(titre, (Donnees.WIDTH // 2 - titre.get_width() // 2, 50))
            
            # Dessiner les carrés des mondes
            for i, (rect, monde) in enumerate(zip(rectangles_mondes, mondes)):
                # Fond du carré avec la couleur du monde
                pg.draw.rect(screen, monde["couleur"], rect)
                
                # Bordure plus épaisse si sélectionné au clavier
                epaisseur = 3
                couleur_bordure = Donnees.COULEUR_NOIR
                if i == monde_survole:
                    epaisseur = 6
                    couleur_bordure = Donnees.COULEUR_BLANC  # Bordure blanche pour mettre en valeur
                
                pg.draw.rect(screen, couleur_bordure, rect, epaisseur)
                
                # Nom du monde (centré, sur plusieurs lignes si nécessaire)
                lignes_nom = monde["nom"]
                hauteur_ligne = 30
                nb_lignes = len(lignes_nom)
                offset_y = -(nb_lignes - 1) * hauteur_ligne // 2
                
                for j, ligne in enumerate(lignes_nom):
                    texte = font_monde.render(ligne, True, Donnees.COULEUR_BLANC)
                    y_pos = rect.centery + offset_y + j * hauteur_ligne
                    texte_rect = texte.get_rect(center=(rect.centerx, y_pos))
                    screen.blit(texte, texte_rect)
            
            # Message d'information Échap
            info_text = font_info.render("Échap: retour | Flèches: navigation | Entrée: valider", True, Donnees.COULEUR_GRIS_FONCE)
            screen.blit(info_text, (Donnees.WIDTH // 2 - info_text.get_width() // 2, Donnees.HEIGHT - 40))
            
            # Bouton Retour (en bas à droite)
            font_bouton = pg.font.Font(None, 40)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, (0, 0, 0), bouton_retour, 3)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)
            
            pg.display.flip()
            clock.tick(Donnees.FPS)
        
        return monde_selectionne

    @staticmethod
    def get_chemins_monde(cle_monde):
        """
        Retourne les chemins des images de fond et de sol pour un monde donné.
        
        Args:
            cle_monde: La clé univers du monde (ex: "foret_bleue", "foret_violette", etc.)
        
        Returns:
            Un dictionnaire contenant 'fond_skin' (liste) et 'sol_skin' (str)
        """
        from BaseDonnees import Univers
        
        # Utiliser directement la clé univers
        chemin_background = Univers[cle_monde]["background"]["chemin"]
        
        # Construire les chemins complets
        sol_skin = Donnees.resource_path(chemin_background + "1.png")
        # Fond avec parallaxe : images de 7 à 2 (du plus éloigné au plus proche)
        # L'image 1 est le sol, gérée par la classe Sol
        fond_skin = [Donnees.resource_path(chemin_background + f"{i}.png") for i in range(7, 1, -1)]
        
        return {
            "sol_skin": sol_skin,
            "fond_skin": fond_skin
        }

    @staticmethod
    def fenetre_vitesse(screen, default_wpm=40, joueur=None):
        """Affiche une petite fenêtre pour saisir la vitesse (mots par minute).
        Retourne un int (10-200) ou None si annulé.
        """
        import pygame as pg
        import BaseDonnees

        min_wpm = 10
        max_wpm = 200
        # Commencer avec une zone vide (l'utilisateur tapera la valeur)
        wpm_str = ''

        # Tenter de récupérer stats joueur si fourni
        moyenne = None
        derniere = None
        try:
            if joueur is not None:
                pseudo_j = joueur
                j = BaseDonnees.get_joueur(pseudo_j)
                if j is not None:
                    try:
                        moyenne = float(j.get('Vitesse_Moyenne_WPM', 0.0))
                    except Exception:
                        moyenne = None
                    try:
                        derniere = float(j.get('Derniere_Vitesse_WPM', 0.0))
                    except Exception:
                        derniere = None
        except Exception:
            moyenne = None
            derniere = None
        
        # Bouton Retour
        bouton_retour = pg.Rect(Donnees.WIDTH // 2 - 75, Donnees.HEIGHT - 120, 150, 40)

        clock = pg.time.Clock()
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_retour.collidepoint(event.pos):
                        return None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        try:
                            val = int(wpm_str) if wpm_str != '' else int(default_wpm)
                        except Exception:
                            val = int(default_wpm)
                        val = max(min_wpm, min(max_wpm, val))
                        # Sauvegarder la dernière valeur entrée pour le joueur si fourni
                        if joueur is not None:
                            try:
                                import BaseDonnees
                                pseudo_j = joueur
                                BaseDonnees.set_derniere_vitesse(pseudo_j, val)
                                derniere = float(val)
                                print(f"Enregistré dernière vitesse {val} WPM pour {pseudo_j}")
                            except Exception:
                                pass
                        return int(val)
                    if event.key == pg.K_ESCAPE:
                        return None
                    if event.key == pg.K_BACKSPACE:
                        wpm_str = wpm_str[:-1]
                    else:
                        ch = event.unicode
                        if ch.isdigit() and len(wpm_str) < 3:
                            if wpm_str == '0':
                                wpm_str = ch
                            else:
                                wpm_str += ch

            # Affichage simple
            screen.fill(Donnees.COULEUR_FOND)
            font_titre = pg.font.Font(None, 48)
            font_val = pg.font.Font(None, 44)
            font_info = pg.font.Font(None, 24)

            titre = font_titre.render("Réglage de la vitesse des mots", True, (0, 0, 0))
            screen.blit(titre, (Donnees.WIDTH//2 - titre.get_width()//2, 80))

            # Zone de saisie
            box_w, box_h = 240, 64
            box_rect = pg.Rect(Donnees.WIDTH//2 - box_w//2, Donnees.HEIGHT//2 - box_h//2, box_w, box_h)
            pg.draw.rect(screen, (255,255,255), box_rect)
            pg.draw.rect(screen, (0,0,0), box_rect, 2)

            # N'afficher rien si l'utilisateur n'a encore rien saisi
            display_val = wpm_str
            val_text = font_val.render(display_val, True, (0,0,0))
            screen.blit(val_text, (box_rect.x + 10, box_rect.y + box_h//2 - val_text.get_height()//2))

            label = font_info.render("mots par minutes", True, (0,0,0))
            screen.blit(label, (box_rect.right + 10, box_rect.y + box_h//2 - label.get_height()//2))

            info = font_info.render("Entrez un nombre puis Entrée (Échap pour annuler)", True, (50,50,50))
            screen.blit(info, (Donnees.WIDTH//2 - info.get_width()//2, Donnees.HEIGHT - 80))

            range_text = font_info.render(f"Plage: {min_wpm} - {max_wpm}", True, (80,80,80))
            rx = Donnees.WIDTH//2 - range_text.get_width()//2 - 120
            ry = Donnees.HEIGHT - 40
            screen.blit(range_text, (rx, ry))

            # Afficher uniquement la dernière valeur entrée (si disponible) à côté de la plage
            if derniere is not None:
                d = font_info.render(f"Dernière valeur entrée: {derniere:.0f}", True, (60,60,60))
                dx = rx + range_text.get_width() + 20
                dy = ry
                screen.blit(d, (dx, dy))
            
            # Bouton Retour
            font_bouton = pg.font.Font(None, 32)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, (0, 0, 0), bouton_retour, 2)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)

            pg.display.flip()
            clock.tick(30)

    @staticmethod
    def fenetre_menu_joueur(screen):
        """
        Affiche un menu pour choisir entre créer un nouveau joueur ou en charger un existant.
        Retourne "nouveau" ou "existant"
        """
        choix = None
        
        # Boutons
        bouton_nouveau = pg.Rect(Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 - 40, 200, 80)
        bouton_existant = pg.Rect(3 * Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 - 40, 200, 80)
        
        while choix is None:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_nouveau.collidepoint(event.pos):
                        choix = "nouveau"
                    elif bouton_existant.collidepoint(event.pos):
                        choix = "existant"
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Chasse aux Mots", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 80))
            screen.blit(titre, titre_rect)
            
            # Sous-titre
            font_sous_titre = pg.font.Font(None, 40)
            sous_titre = font_sous_titre.render("Êtes-vous un nouveau joueur?", True, (0, 0, 0))
            sous_titre_rect = sous_titre.get_rect(center=(Donnees.WIDTH // 2, 180))
            screen.blit(sous_titre, sous_titre_rect)
            
            # Bouton Nouveau joueur
            pg.draw.rect(screen, (100, 200, 100), bouton_nouveau)
            pg.draw.rect(screen, (0, 0, 0), bouton_nouveau, 3)
            texte_nouveau = font_sous_titre.render("Nouveau", True, (255, 255, 255))
            texte_nouveau_rect = texte_nouveau.get_rect(center=bouton_nouveau.center)
            screen.blit(texte_nouveau, texte_nouveau_rect)
            
            # Bouton Joueur existant
            pg.draw.rect(screen, (100, 150, 200), bouton_existant)
            pg.draw.rect(screen, (0, 0, 0), bouton_existant, 3)
            texte_existant = font_sous_titre.render("Existant", True, (255, 255, 255))
            texte_existant_rect = texte_existant.get_rect(center=bouton_existant.center)
            screen.blit(texte_existant, texte_existant_rect)
            
            pg.display.flip()
        
        return choix

    @staticmethod
    def fenetre_joueur(screen):
        """
        Affiche le menu d'entrée du pseudo du joueur.
        Retourne le pseudo lorsque l'utilisateur valide, ou None si Échap est pressé.
        """
        
        class InputBox:
            def __init__(self, x, y, w, h, text=''):
                self.rect = pg.Rect(x, y, w, h)
                self.color = (200, 200, 200)
                self.color_active = (255, 255, 255)
                self.color_inactive = (200, 200, 200)
                self.active = False
                self.text = text
                self.txt_surface = None
                self.update_text()
            
            def handle_event(self, event):
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                
                if event.type == pg.KEYDOWN:
                    if self.active:
                        if event.key == pg.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif event.key == pg.K_SPACE:
                            self.text += ' '
                        elif len(self.text) < 20:  # Limite à 20 caractères
                            self.text += event.unicode
                        self.update_text()
            
            def update_text(self):
                font = pg.font.Font(None, 32)
                self.txt_surface = font.render(self.text if self.text else 'Entrez votre pseudo...', True, (0, 0, 0))
            
            def draw(self, screen):
                screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 7))
                pg.draw.rect(screen, self.color, self.rect, 2)
            
            def get_text(self):
                return self.text.strip()
        
        
        # Initialisation de la boîte de saisie
        input_pseudo = InputBox(Donnees.WIDTH // 4, Donnees.HEIGHT // 2, 300, 40)
        
        # Bouton Valider
        bouton_valider = pg.Rect(Donnees.WIDTH // 2 - 75, Donnees.HEIGHT // 2 + 100, 150, 40)
        
        # Bouton Retour (en bas à droite)
        bouton_retour = pg.Rect(Donnees.WIDTH - 230, Donnees.HEIGHT - 80, 200, 50)
        
        entree_complete = False
        
        while not entree_complete:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                input_pseudo.handle_event(event)
                
                # Vérifier si le bouton Valider ou Retour est cliqué
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_valider.collidepoint(event.pos):
                        if input_pseudo.get_text():
                            entree_complete = True
                    elif bouton_retour.collidepoint(event.pos):
                        return None
                
                # Valider aussi avec la touche Entrée
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if input_pseudo.get_text():
                            entree_complete = True
                    elif event.key == pg.K_ESCAPE:
                        # Retourner None pour indiquer l'annulation
                        return None
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Bienvenue dans Chasse aux Mots!", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 80))
            screen.blit(titre, titre_rect)
            
            # Label
            font_label = pg.font.Font(None, 36)
            label_pseudo = font_label.render("Pseudo:", True, (0, 0, 0))
            screen.blit(label_pseudo, (Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2))
            
            # Boîte de saisie
            input_pseudo.draw(screen)
            
            # Bouton Valider
            pg.draw.rect(screen, (100, 200, 100), bouton_valider)
            bouton_texte = font_label.render("Valider", True, (255, 255, 255))
            bouton_texte_rect = bouton_texte.get_rect(center=bouton_valider.center)
            screen.blit(bouton_texte, bouton_texte_rect)
            
            # Bouton Retour (en bas à droite)
            font_bouton = pg.font.Font(None, 40)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, (0, 0, 0), bouton_retour, 3)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)
            
            # Message d'erreur si champ vide
            if any(event.type == pg.MOUSEBUTTONDOWN and bouton_valider.collidepoint(event.pos) 
                   for event in events) and not input_pseudo.get_text():
                message_erreur = font_label.render("Veuillez entrer un pseudo!", True, (255, 0, 0))
                screen.blit(message_erreur, (Donnees.WIDTH // 2 - 150, Donnees.HEIGHT - 70))
            
            # Message pour la touche Échap
            font_small = pg.font.Font(None, 28)
            message_echap = font_small.render("Échap : retour", True, (100, 100, 100))
            screen.blit(message_echap, (20, Donnees.HEIGHT - 35))
            
            pg.display.flip()
        
        # Retourner le pseudo du joueur
        return input_pseudo.get_text()

    @staticmethod
    def fenetre_confirmation_suppression(screen, pseudo):
        """
        Affiche une fenêtre de confirmation avec double vérification pour supprimer un joueur.
        Retourne True si l'utilisateur confirme, False sinon.
        """
        # Première confirmation
        confirmation1 = False
        bouton_oui = pg.Rect(Donnees.WIDTH // 4 - 75, Donnees.HEIGHT // 2 + 50, 150, 50)
        bouton_non = pg.Rect(3 * Donnees.WIDTH // 4 - 75, Donnees.HEIGHT // 2 + 50, 150, 50)
        
        while True:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_oui.collidepoint(event.pos):
                        confirmation1 = True
                        break
                    elif bouton_non.collidepoint(event.pos):
                        return False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
            
            if confirmation1:
                break
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 50)
            titre = font_titre.render("Supprimer ce profil ?", True, (200, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 100))
            screen.blit(titre, titre_rect)
            
            # Pseudo du joueur
            font_nom = pg.font.Font(None, 40)
            nom_texte = font_nom.render(f"{pseudo}", True, (0, 0, 0))
            nom_rect = nom_texte.get_rect(center=(Donnees.WIDTH // 2, 180))
            screen.blit(nom_texte, nom_rect)
            
            # Message d'avertissement
            font_msg = pg.font.Font(None, 30)
            msg1 = font_msg.render("Cette action est irréversible.", True, (100, 0, 0))
            msg2 = font_msg.render("Toutes les statistiques seront perdues.", True, (100, 0, 0))
            screen.blit(msg1, (Donnees.WIDTH // 2 - 200, 250))
            screen.blit(msg2, (Donnees.WIDTH // 2 - 220, 280))
            
            # Boutons
            pg.draw.rect(screen, (200, 100, 100), bouton_oui)
            pg.draw.rect(screen, (0, 0, 0), bouton_oui, 3)
            texte_oui = font_nom.render("Oui", True, (255, 255, 255))
            texte_oui_rect = texte_oui.get_rect(center=bouton_oui.center)
            screen.blit(texte_oui, texte_oui_rect)
            
            pg.draw.rect(screen, (100, 200, 100), bouton_non)
            pg.draw.rect(screen, (0, 0, 0), bouton_non, 3)
            texte_non = font_nom.render("Non", True, (255, 255, 255))
            texte_non_rect = texte_non.get_rect(center=bouton_non.center)
            screen.blit(texte_non, texte_non_rect)
            
            pg.display.flip()
        
        # Deuxième confirmation
        confirmation2 = False
        bouton_confirmer = pg.Rect(Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 + 50, 200, 50)
        bouton_annuler = pg.Rect(3 * Donnees.WIDTH // 4 - 100, Donnees.HEIGHT // 2 + 50, 200, 50)
        
        while True:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_confirmer.collidepoint(event.pos):
                        confirmation2 = True
                        break
                    elif bouton_annuler.collidepoint(event.pos):
                        return False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
            
            if confirmation2:
                break
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 50)
            titre = font_titre.render("Êtes-vous vraiment sûr ?", True, (200, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 100))
            screen.blit(titre, titre_rect)
            
            # Message final
            font_msg = pg.font.Font(None, 35)
            msg = font_msg.render("Dernière chance pour annuler !", True, (0, 0, 0))
            msg_rect = msg.get_rect(center=(Donnees.WIDTH // 2, 200))
            screen.blit(msg, msg_rect)
            
            # Boutons
            pg.draw.rect(screen, (200, 0, 0), bouton_confirmer)
            pg.draw.rect(screen, (0, 0, 0), bouton_confirmer, 3)
            texte_confirmer = font_titre.render("Confirmer", True, (255, 255, 255))
            texte_confirmer_rect = texte_confirmer.get_rect(center=bouton_confirmer.center)
            screen.blit(texte_confirmer, texte_confirmer_rect)
            
            pg.draw.rect(screen, (100, 200, 100), bouton_annuler)
            pg.draw.rect(screen, (0, 0, 0), bouton_annuler, 3)
            texte_annuler = font_titre.render("Annuler", True, (255, 255, 255))
            texte_annuler_rect = texte_annuler.get_rect(center=bouton_annuler.center)
            screen.blit(texte_annuler, texte_annuler_rect)
            
            pg.display.flip()
        
        return True

    @staticmethod
    def fenetre_confirmation_quitter(screen, pseudo=None, vitesse_defilement=None, reset_mots_actif=None):
        """
        Affiche une fenêtre de confirmation avant de quitter le jeu.
        Propose de sauvegarder les paramètres et avertit que la progression ne sera pas sauvegardée.
        
        Args:
            screen: L'écran pygame
            pseudo: Pseudo du joueur (optionnel, pour la sauvegarde des paramètres)
            vitesse_defilement: Vitesse actuelle en pourcentage (optionnel)
            reset_mots_actif: État du reset des mots (optionnel)
        
        Returns:
            str: 'quitter' pour quitter sans sauvegarder, 'sauvegarder' pour sauvegarder et quitter, 
                 'annuler' pour annuler et continuer
        """
        # Positions des boutons (3 boutons côte à côte)
        bouton_largeur = 180
        bouton_hauteur = 50
        espacement = 20
        total_largeur = 3 * bouton_largeur + 2 * espacement
        debut_x = (Donnees.WIDTH - total_largeur) // 2
        bouton_y = Donnees.HEIGHT // 2 + 100
        
        bouton_sauvegarder = pg.Rect(debut_x, bouton_y, bouton_largeur, bouton_hauteur)
        bouton_quitter = pg.Rect(debut_x + bouton_largeur + espacement, bouton_y, bouton_largeur, bouton_hauteur)
        bouton_annuler = pg.Rect(debut_x + 2 * (bouton_largeur + espacement), bouton_y, bouton_largeur, bouton_hauteur)
        
        # Vérifier si on peut sauvegarder les paramètres
        peut_sauvegarder = (pseudo is not None and vitesse_defilement is not None and reset_mots_actif is not None)
        
        while True:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    # Si l'utilisateur clique à nouveau sur la croix rouge, quitter directement
                    return 'quitter'
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_annuler.collidepoint(event.pos):
                        return 'annuler'
                    elif bouton_quitter.collidepoint(event.pos):
                        return 'quitter'
                    elif peut_sauvegarder and bouton_sauvegarder.collidepoint(event.pos):
                        # Sauvegarder les paramètres avant de quitter
                        import BaseDonnees
                        BaseDonnees.sauvegarder_parametres_joueur(pseudo, vitesse_defilement, reset_mots_actif)
                        return 'sauvegarder'
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return 'annuler'
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 56)
            titre = font_titre.render("Voulez-vous quitter ?", True, (200, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 80))
            screen.blit(titre, titre_rect)
            
            # Message d'avertissement
            font_msg = pg.font.Font(None, 32)
            msg1 = font_msg.render("Votre progression ne sera pas sauvegardée.", True, (100, 0, 0))
            msg1_rect = msg1.get_rect(center=(Donnees.WIDTH // 2, 150))
            screen.blit(msg1, msg1_rect)
            
            # Afficher ou pas le message sur la sauvegarde des paramètres
            if peut_sauvegarder:
                font_note = pg.font.Font(None, 30)
                msg2 = font_note.render("Sauvegarder vos paramètres avant de quitter ?", True, (0, 0, 0))
                msg2_rect = msg2.get_rect(center=(Donnees.WIDTH // 2, 210))
                screen.blit(msg2, msg2_rect)
            else:
                font_note = pg.font.Font(None, 28)
                msg2 = font_note.render("(Connectez-vous pour sauvegarder vos paramètres)", True, (120, 120, 120))
                msg2_rect = msg2.get_rect(center=(Donnees.WIDTH // 2, 210))
                screen.blit(msg2, msg2_rect)
            
            # Boutons
            font_bouton = pg.font.Font(None, 48)
            
            # Bouton Oui (vert, sauvegarder et quitter - seulement si possible)
            if peut_sauvegarder:
                pg.draw.rect(screen, (100, 200, 100), bouton_sauvegarder)
                pg.draw.rect(screen, (0, 0, 0), bouton_sauvegarder, 3)
                texte_oui = font_bouton.render("Oui", True, (255, 255, 255))
                texte_oui_rect = texte_oui.get_rect(center=bouton_sauvegarder.center)
                screen.blit(texte_oui, texte_oui_rect)
            else:
                # Bouton grisé si pas de joueur
                pg.draw.rect(screen, (150, 150, 150), bouton_sauvegarder)
                pg.draw.rect(screen, (100, 100, 100), bouton_sauvegarder, 3)
                texte_oui = font_bouton.render("Oui", True, (200, 200, 200))
                texte_oui_rect = texte_oui.get_rect(center=bouton_sauvegarder.center)
                screen.blit(texte_oui, texte_oui_rect)
            
            # Bouton Non (rouge, quitter sans sauvegarder)
            pg.draw.rect(screen, (200, 100, 100), bouton_quitter)
            pg.draw.rect(screen, (0, 0, 0), bouton_quitter, 3)
            texte_non = font_bouton.render("Non", True, (255, 255, 255))
            texte_non_rect = texte_non.get_rect(center=bouton_quitter.center)
            screen.blit(texte_non, texte_non_rect)
            
            # Bouton Annuler (bleu, continuer le jeu)
            pg.draw.rect(screen, (100, 150, 200), bouton_annuler)
            pg.draw.rect(screen, (0, 0, 0), bouton_annuler, 3)
            texte_annuler = font_bouton.render("Annuler", True, (255, 255, 255))
            texte_annuler_rect = texte_annuler.get_rect(center=bouton_annuler.center)
            screen.blit(texte_annuler, texte_annuler_rect)
            
            pg.display.flip()

    @staticmethod
    def fenetre_charger_joueur(screen):
        """
        Affiche une liste de joueurs existants pour en sélectionner un.
        Supporte le défilement avec la molette si la liste est longue.
        Permet de supprimer un profil avec la touche Suppr ou le clic droit.
        Retourne le pseudo du joueur sélectionné.
        """
        import BaseDonnees
        
        joueurs_list = []
        if BaseDonnees.dict_joueurs:
            joueurs_list = [j['pseudo'] for j in BaseDonnees.dict_joueurs.values()]
        
        if not joueurs_list:
            # Aucun joueur enregistré, revenir au menu
            screen.fill(Donnees.COULEUR_FOND)
            font = pg.font.Font(None, 48)
            texte = font.render("Aucun joueur enregistré!", True, (0, 0, 0))
            texte_rect = texte.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
            screen.blit(texte, texte_rect)
            pg.display.flip()
            pg.time.wait(2000)
            return None
        
        selected_index = 0
        scroll_offset = 0  # Décalage pour le défilement
        selection_complete = False
        escape_pressed = False
        
        # Bouton Retour (en bas à droite)
        bouton_retour = pg.Rect(Donnees.WIDTH - 230, Donnees.HEIGHT - 80, 200, 50)
        
        # Paramètres d'affichage
        item_height = 60
        zone_liste_y = 150  # Y de début de la liste
        zone_liste_height = Donnees.HEIGHT - zone_liste_y - 60  # Hauteur de la zone d'affichage
        max_items_visibles = zone_liste_height // item_height  # Nombre max d'éléments affichables
        
        while not selection_complete and not escape_pressed:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                # Gestion de la molette de la souris
                if event.type == pg.MOUSEWHEEL:
                    if event.y > 0:  # Molette vers le haut
                        scroll_offset = max(0, scroll_offset - 1)
                    else:  # Molette vers le bas
                        max_scroll = max(0, len(joueurs_list) - max_items_visibles)
                        scroll_offset = min(max_scroll, scroll_offset + 1)
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected_index = (selected_index - 1) % len(joueurs_list)
                        # Ajuster le scroll pour garder la sélection visible
                        if selected_index < scroll_offset:
                            scroll_offset = selected_index
                        
                    elif event.key == pg.K_DOWN:
                        selected_index = (selected_index + 1) % len(joueurs_list)
                        # Ajuster le scroll pour garder la sélection visible
                        if selected_index >= scroll_offset + max_items_visibles:
                            scroll_offset = selected_index - max_items_visibles + 1
                    
                    elif event.key == pg.K_RETURN:
                        selection_complete = True
                    
                    elif event.key == pg.K_ESCAPE:
                        escape_pressed = True
                    
                    elif event.key == pg.K_DELETE:
                        # Supprimer le joueur sélectionné
                        pseudo = joueurs_list[selected_index]
                        if Menu.fenetre_confirmation_suppression(screen, pseudo):
                            succes, message = BaseDonnees.supprimer_joueur(pseudo)
                            if succes:
                                # Recharger la liste
                                joueurs_list = [j['pseudo'] for j in BaseDonnees.dict_joueurs.values()]
                                if not joueurs_list:
                                    # Plus de joueurs
                                    screen.fill(Donnees.COULEUR_FOND)
                                    font = pg.font.Font(None, 48)
                                    texte = font.render("Tous les joueurs ont été supprimés!", True, (0, 0, 0))
                                    texte_rect = texte.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
                                    screen.blit(texte, texte_rect)
                                    pg.display.flip()
                                    pg.time.wait(2000)
                                    return None
                                # Ajuster la sélection
                                selected_index = min(selected_index, len(joueurs_list) - 1)
                                scroll_offset = min(scroll_offset, max(0, len(joueurs_list) - max_items_visibles))
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Vérifier le clic sur le bouton retour
                    if bouton_retour.collidepoint(event.pos):
                        escape_pressed = True
                        break
                    
                    # Calculer les rectangles visibles
                    joueur_rects = []
                    for i in range(scroll_offset, min(scroll_offset + max_items_visibles, len(joueurs_list))):
                        display_index = i - scroll_offset
                        joueur_rect = pg.Rect(Donnees.WIDTH // 4, zone_liste_y + display_index * item_height, 
                                            Donnees.WIDTH // 2, item_height - 10)
                        joueur_rects.append((i, joueur_rect))
                    
                    # Clic gauche : sélectionner
                    if event.button == 1:
                        for i, rect in joueur_rects:
                            if rect.collidepoint(event.pos):
                                selected_index = i
                                selection_complete = True
                    
                    # Clic droit : supprimer
                    elif event.button == 3:
                        for i, rect in joueur_rects:
                            if rect.collidepoint(event.pos):
                                pseudo = joueurs_list[i]
                                if Menu.fenetre_confirmation_suppression(screen, pseudo):
                                    succes, message = BaseDonnees.supprimer_joueur(pseudo)
                                    if succes:
                                        # Recharger la liste
                                        joueurs_list = [j['pseudo'] for j in BaseDonnees.dict_joueurs.values()]
                                        if not joueurs_list:
                                            # Plus de joueurs
                                            screen.fill(Donnees.COULEUR_FOND)
                                            font = pg.font.Font(None, 48)
                                            texte = font.render("Tous les joueurs ont été supprimés!", True, (0, 0, 0))
                                            texte_rect = texte.get_rect(center=(Donnees.WIDTH // 2, Donnees.HEIGHT // 2))
                                            screen.blit(texte, texte_rect)
                                            pg.display.flip()
                                            pg.time.wait(2000)
                                            return None
                                        # Ajuster la sélection
                                        selected_index = min(selected_index, len(joueurs_list) - 1)
                                        scroll_offset = min(scroll_offset, max(0, len(joueurs_list) - max_items_visibles))
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, 60)
            titre = font_titre.render("Sélectionner un joueur", True, (0, 0, 0))
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, 50))
            screen.blit(titre, titre_rect)
            
            # Indicateur de scroll si nécessaire
            if len(joueurs_list) > max_items_visibles:
                font_scroll = pg.font.Font(None, 25)
                scroll_info = font_scroll.render(f"({scroll_offset + 1}-{min(scroll_offset + max_items_visibles, len(joueurs_list))} / {len(joueurs_list)})", 
                                                True, (100, 100, 100))
                screen.blit(scroll_info, (Donnees.WIDTH // 2 - 50, 110))
            
            # Liste des joueurs visibles
            font_joueur = pg.font.Font(None, 40)
            
            for i in range(scroll_offset, min(scroll_offset + max_items_visibles, len(joueurs_list))):
                display_index = i - scroll_offset
                pseudo = joueurs_list[i]
                
                couleur = (100, 200, 100) if i == selected_index else (200, 200, 200)
                joueur_rect = pg.Rect(Donnees.WIDTH // 4, zone_liste_y + display_index * item_height, 
                                    Donnees.WIDTH // 2, item_height - 10)
                
                pg.draw.rect(screen, couleur, joueur_rect)
                pg.draw.rect(screen, (0, 0, 0), joueur_rect, 2)
                
                texte_joueur = font_joueur.render(f"{pseudo}", True, (0, 0, 0))
                texte_rect = texte_joueur.get_rect(center=joueur_rect.center)
                screen.blit(texte_joueur, texte_rect)
            
            # Instructions
            font_info = pg.font.Font(None, 25)
            info1 = font_info.render("Haut/Bas ou molette: naviguer | Entree ou clic gauche: valider", True, (100, 100, 100))
            info2 = font_info.render("Suppr ou clic droit: supprimer | Esc: retour", True, (100, 100, 100))
            screen.blit(info1, (20, Donnees.HEIGHT - 50))
            screen.blit(info2, (20, Donnees.HEIGHT - 25))
            
            # Bouton Retour (en bas à droite)
            font_bouton = pg.font.Font(None, 40)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, (0, 0, 0), bouton_retour, 3)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)
            
            pg.display.flip()
        
        if escape_pressed:
            return None
        
        # Retourner le joueur sélectionné
        pseudo = joueurs_list[selected_index]
        return pseudo

    @staticmethod
    def menu_selection_joueur(screen):
        """
        Gère le menu complet de sélection/création d'un joueur.
        Retourne le pseudo une fois qu'un joueur valide est sélectionné.
        """
        import BaseDonnees
        import sys
        
        joueur_valide = False
        pseudo_joueur = None
        
        while not joueur_valide:
            # Afficher le menu de choix
            choix = Menu.fenetre_menu_joueur(screen)
            
            if choix == "nouveau":
                # Créer un nouveau joueur
                while True:
                    result = Menu.fenetre_joueur(screen)
                    
                    # Si l'utilisateur a appuyé sur Échap, retourner au menu de choix
                    if result is None:
                        break
                    
                    pseudo = result
                    succes, message = BaseDonnees.ajouter_joueur(pseudo)
                    
                    if succes:
                        pseudo_joueur = pseudo
                        joueur_valide = True
                        print(f"Bienvenue {pseudo}! (Nouveau joueur créé)")
                        break
                    else:
                        # Le joueur existe déjà - afficher message et revenir au choix
                        screen.fill(Donnees.COULEUR_FOND)
                        font = pg.font.Font(None, Donnees.MENU_JOUEUR_POLICE_ERREUR)
                        font_small = pg.font.Font(None, Donnees.MENU_JOUEUR_POLICE_INFO)
                        
                        texte_erreur = font.render(message, True, Donnees.MENU_JOUEUR_COULEUR_ERREUR)
                        texte_retry = font_small.render("Appuyez sur une touche pour continuer...", True, Donnees.COULEUR_NOIR)
                        
                        screen.blit(texte_erreur, (Donnees.WIDTH // 2 - Donnees.MENU_JOUEUR_ERREUR_OFFSET_X, Donnees.HEIGHT // 2 - Donnees.MENU_JOUEUR_ERREUR_OFFSET_Y))
                        screen.blit(texte_retry, (Donnees.WIDTH // 2 - Donnees.MENU_JOUEUR_INFO_OFFSET_X, Donnees.HEIGHT // 2 + Donnees.MENU_JOUEUR_INFO_OFFSET_Y))
                        pg.display.flip()
                        
                        # Attendre une touche
                        en_attente = True
                        while en_attente:
                            for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    sys.exit()
                                if event.type == pg.KEYDOWN:
                                    en_attente = False
                        break
            
            elif choix == "existant":
                # Charger un joueur existant
                result = Menu.fenetre_charger_joueur(screen)
                
                if result is not None:
                    pseudo_joueur = result
                    joueur_valide = True
                    print(f"Bienvenue {pseudo_joueur}! (Joueur existant)")
                # else: retourner au menu de choix
        
        return pseudo_joueur

    @staticmethod
    def fenetre_afficher_stats_joueur(screen, pseudo):
        """
        Affiche les statistiques du joueur courant.
        """
        joueur = BaseDonnees.get_joueur(pseudo)
        
        if joueur is None:
            return
        
        # Récupérer les statistiques calculées depuis l'historique
        stats = BaseDonnees.get_statistiques_joueur(pseudo)
        
        if stats is None:
            return
        
        # Générer le graphique
        graphique_path = Menu.generer_graphique_stats(pseudo)
        graphique_surface = None
        
        if graphique_path and os.path.exists(graphique_path):
            try:
                graphique_surface = pg.image.load(graphique_path)
                # Redimensionner le graphique pour qu'il s'adapte à l'écran
                graphique_width = Donnees.WIDTH - 100
                graphique_height = int(graphique_surface.get_height() * (graphique_width / graphique_surface.get_width()))
                graphique_surface = pg.transform.smoothscale(graphique_surface, (graphique_width, graphique_height))
            except Exception as e:
                print(f"[ERROR] Impossible de charger le graphique: {e}")
                graphique_surface = None
        
        # Bouton Retour
        bouton_retour = pg.Rect(Donnees.WIDTH // 2 - 100, Donnees.HEIGHT - 100, 200, 50)
        
        attente_stats = True
        while attente_stats:
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        attente_stats = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if bouton_retour.collidepoint(event.pos):
                        attente_stats = False
            
            # Affichage
            screen.fill(Donnees.COULEUR_FOND)
            
            # Titre
            font_titre = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_TITRE)
            titre = font_titre.render("Profil du Joueur", True, Donnees.COULEUR_NOIR)
            titre_rect = titre.get_rect(center=(Donnees.WIDTH // 2, Donnees.STATS_JOUEUR_TITRE_Y))
            screen.blit(titre, titre_rect)
            
            # Infos du joueur
            font_info = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_INFO)
            font_label = pg.font.Font(None, Donnees.STATS_JOUEUR_POLICE_LABEL)
            
            y_offset = Donnees.STATS_JOUEUR_STATS_Y
            
            # Pseudo
            joueur_nom = font_info.render(f"{joueur['pseudo']}", True, Donnees.STATS_JOUEUR_COULEUR_TITRE)
            screen.blit(joueur_nom, (Donnees.WIDTH // 2 - Donnees.STATS_FIN_STATS_OFFSET_X, y_offset))
            
            y_offset += Donnees.STATS_JOUEUR_LINE_HEIGHT + Donnees.STATS_JOUEUR_SECTION_SPACING
            
            # Statistiques calculées depuis l'historique
            nb_parties = stats['nb_parties']
            mots_reussis = stats['mots_reussis_total']
            vitesse_moyenne = stats['vitesse_moyenne_wpm']
            erreurs_total = stats['erreurs_total']
            
            stat_text = [
                f"Parties jouées: {nb_parties}",
                f"Mots réussis (total): {mots_reussis}",
                f"Vitesse moyenne: {vitesse_moyenne:.2f} caractères/s",
                f"Erreurs (total): {erreurs_total}"
            ]
            
            for stat in stat_text:
                texte = font_label.render(stat, True, Donnees.COULEUR_NOIR)
                screen.blit(texte, (Donnees.WIDTH // 4, y_offset))
                y_offset += Donnees.STATS_JOUEUR_LINE_HEIGHT
            
            # Afficher le graphique si disponible
            if graphique_surface:
                y_offset += 30  # Espacement avant le graphique
                graphique_x = (Donnees.WIDTH - graphique_surface.get_width()) // 2
                screen.blit(graphique_surface, (graphique_x, y_offset))
            
            # Bouton Retour
            font_bouton = pg.font.Font(None, 40)
            pg.draw.rect(screen, (200, 100, 100), bouton_retour)
            pg.draw.rect(screen, (0, 0, 0), bouton_retour, 3)
            texte_retour = font_bouton.render("Retour", True, (255, 255, 255))
            texte_retour_rect = texte_retour.get_rect(center=bouton_retour.center)
            screen.blit(texte_retour, texte_retour_rect)
            
            pg.display.flip()
