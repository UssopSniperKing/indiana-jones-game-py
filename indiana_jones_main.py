
#!/usr/bin/python3

# -*- coding: Utf-8 -*


#Jeu INDIANA JONES : Les aventuriers de l'arche perdue
#Jeu dans lequel on doit deplacer Indiana jusqu'a l'arche d'alliance a travers un labyrinthe.
#Script Python
#Fichiers : indiana_jones_main.py, classes.py, constantes.py, niveaux + images


import pygame
import time
from pygame.locals import *
from classes import *
from constantes import *

#Initialisation du module pygame
pygame.init()

#Definition du mode de deplacement en fonction de la constante mv_mode
if mv_mode == "DEFAULT":

    mv_haut = K_UP
    mv_bas = K_DOWN
    mv_gauche = K_LEFT
    mv_droite = K_RIGHT

elif mv_mode == "CUSTOM":

    mv_haut = K_w
    mv_bas = K_s
    mv_gauche = K_a
    mv_droite = K_d

#Police principale
main_font = pygame.font.Font(Bebas, 13)

#Ouverture de la fenetre Pygame 450x480
fenetre = pygame.display.set_mode((450, 480))

#Icone
icone = pygame.image.load(ij_bas)
pygame.display.set_icon(icone)

#Titre
pygame.display.set_caption(titre_fenetre)

#Musique
pygame.mixer.music.load(theme_principal)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume_theme_principal)

#BOUCLE PRINCIPALE
continuer = 1

while continuer:

    #Chargement et affichage de l'ecran d'accueil
    accueil = pygame.image.load(img_accueil).convert()
    fenetre.blit(accueil, (0,0))

    #Rafraichissement
    pygame.display.flip()

    #On remet ces variables sur 1 pour chaque tour de boucle
    continuer_jeu = 1
    continuer_accueil = 1
    continuer_victoire = 1


    #BOUCLE D'ACCUEIL
    while continuer_accueil:

        #Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        #Boucle permettant l'Ã©coute des commandes utilisateur
        for event in pygame.event.get():


            #Si l'utilisateur quitte, on met les variables de boucle a 0 pour n'en parcourir aucune et fermer
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:

                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
                continuer_victoire = 0

                #Variable de choix du niveau
                choix = 0

            elif event.type == KEYDOWN:

                #Lancement du niveau 1
                if event.key == K_F1:

                    continuer_accueil = 0   #On quitte l'accueil
                    choix = lv1             #On definit le niveau a charger

                #Lancement du niveau 2
                elif event.key == K_F2:

                    continuer_accueil = 0
                    choix = lv2

                # Lancement du niveau 3
                elif event.key == K_F3:

                    continuer_accueil = 0
                    choix = lv3

                # Lancement du niveau 4
                elif event.key == K_F4:

                    continuer_accueil = 0
                    choix = lv4

                # Lancement du niveau 5
                elif event.key == K_F5:

                    continuer_accueil = 0
                    choix = lv5

                # Lancement du niveau 6
                elif event.key == K_F6:

                    continuer_accueil = 0
                    choix = lv6

                # Lancement du niveau dev
                elif event.key == K_F12:

                    continuer_accueil = 0
                    choix = dev_level

    #on verifie que le joueur a bien fait un choix de niveau pour ne pas charger s'il quitte
    if choix != 0:

        #Chargement du fond
        fond = pygame.image.load(img_fond).convert()

        #Generation d'un niveau a partir d'un fichier
        niveau = Niveau(choix)
        niveau.generer()
        niveau.afficher(fenetre)

        #Creation d'Indiana Jones
        ij = Perso(ij_droite, ij_gauche, ij_haut, ij_bas, niveau)


    #Deplacement du perso en continu
    pygame.key.set_repeat(100, 50)

    #Variables des artefacts secondaires
    artefact_dict = {
                     "artefact1_trouve" : False,
                     "artefact2_trouve" : False,
                     "artefact3_trouve" : False,
                    }

    #Images Artefact
    Art1 = pygame.image.load(img_artefact1).convert_alpha()
    Art2 = pygame.image.load(img_artefact2).convert_alpha()
    Art3 = pygame.image.load(img_artefact3).convert_alpha()

    #Temps
    start_time = time.time()

    #BOUCLE DE JEU
    while continuer_jeu:

        #Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        #Boucle permettant l'ecoute des commandes utilisateur
        for event in pygame.event.get():

            #Si l'utilisateur quitte, on met la variable qui continue le jeu et la variable generale a 0 pour fermer la fenetre
            if event.type == QUIT:

                continuer_jeu = 0
                continuer = 0
                continuer_victoire = 0

            elif event.type == KEYDOWN:

                if event.key == mv_droite:    #Touches de deplacement vers la droite

                    ij.deplacer('droite')

                elif event.key == mv_gauche:    #Touches de deplacement vers la gauche

                    ij.deplacer('gauche')

                elif event.key == mv_haut:      #Touches de deplacement vers le haut

                    ij.deplacer('haut')

                elif event.key == mv_bas:       #Touches de deplacement vers le bas

                    ij.deplacer('bas')


        #Affichages aux nouvelles positions
        fenetre.blit(fond, (0,0))
        niveau.afficher(fenetre)
        fenetre.blit(ij.direction, (ij.x, ij.y)) #ij.direction = l'image dans la bonne direction

        #Evenements propres a une case
        if niveau.structure[ij.case_y][ij.case_x] == 'x':       #Artefact 1 trouve

            artefact_dict["artefact1_trouve"] = True

        elif niveau.structure[ij.case_y][ij.case_x] == 'y':     #Artefact 2 trouve

            artefact_dict["artefact2_trouve"] = True

        elif niveau.structure[ij.case_y][ij.case_x] == 'z':     #Artefact 3 trouve

            artefact_dict["artefact3_trouve"] = True

        elif niveau.structure[ij.case_y][ij.case_x] == 'a':     #Case d'arrivee

            continuer_jeu = 0


        #Affichage sur la fenetre si l'artefact est trouve
        for key, value in artefact_dict.items():

            if key == "artefact1_trouve" and value:

                fenetre.blit(Art1, (284, 450))

            if key == "artefact2_trouve" and value:

                fenetre.blit(Art2, (346, 448))
            if key == "artefact3_trouve" and value:
                fenetre.blit(Art3, (406, 449))

        #Eclairage brouillard
        ij.eclairage(fenetre)
        #Rafraichissement
        pygame.display.flip()

    #Timer
    stop_time = time.time()
    play_time = int(stop_time - start_time)

    #Objectif compteur
    objectif = 0
    i = True

    #BOUCLE MENU VICTOIRE
    while continuer_victoire:

        #Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        #Affichage de l'image du menu de victoire
        victoire = pygame.image.load(img_victoire).convert()
        fenetre.blit(victoire,(0,0))

        while i:
            for key, value in artefact_dict.items():

                if key == "artefact1_trouve" and value:
                    objectif = objectif + 1
                if key == "artefact2_trouve" and value:
                    objectif = objectif + 1
                if key == "artefact3_trouve" and value:
                    objectif = objectif + 1
            i = False

        #Affichage du compteur d'artefacts
        R_objectif = main_font.render("ARTEFACT(s) " + str(objectif) + "/3", 1,  (255, 187, 0))
        fenetre.blit(R_objectif, (333, 445))

        #Affichage de "arche 1/1"
        M_objectif = main_font.render("ARCHE D'ALLIANCE 1/1", 1, (255, 187, 0))
        fenetre.blit(M_objectif, (333, 460))

        #Affichage du temps
        timer_label = main_font.render(str(play_time) + " SECONDES", 1, (255,187,0))
        fenetre.blit(timer_label, (23, 451))

        #Rafraichissement
        pygame.display.flip()

        #Boucle permettant l'ecoute des commandes utilisateur
        for event in pygame.event.get():

            #Si l'utilisateur quitte, on met les variables de boucle a 0 pour n'en parcourir aucune et fermer
            if event.type == QUIT :

                continuer_accueil = 0
                continuer_jeu = 0
                continuer_victoire = 0
                continuer = 0

            elif event.type == KEYDOWN and event.key == K_SPACE:

                continuer_jeu = 0
                continuer_victoire = 0
            
pygame.quit()
