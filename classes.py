# -*- coding: Utf-8 -*

#Classes du jeu de INDIANA JONES : Les aventuriers de l'arche perdue

import pygame
from pygame.locals import *
from constantes import *

class Niveau:
	#Classe permettant de créer un niveau
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0


	def generer(self):
		#Méthode permettant de générer le niveau en fonction du fichier.
		#On crée une liste générale, contenant une liste par ligne à afficher

		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau


	def afficher(self, fenetre):
		#Méthode permettant d'afficher le niveau en fonction
		#de la liste de structure renvoyée par generer()
		
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load(img_mur).convert()
		depart = pygame.image.load(img_depart).convert_alpha()
		arrivee = pygame.image.load(img_arrivee).convert_alpha()
		artefact1 = pygame.image.load(img_artefact1).convert_alpha()
		artefact2 = pygame.image.load(img_artefact2).convert_alpha()
		artefact3 = pygame.image.load(img_artefact3).convert_alpha()

		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == 'd':		   #d = Départ
					fenetre.blit(depart, (x,y))
				elif sprite == 'a':		   #a = Arrivée
					fenetre.blit(arrivee, (x,y))
				elif sprite == 'x':			#x = artefact 1
					fenetre.blit(artefact1, (x,y))
				elif sprite == 'y':			#y = artefact 2
					fenetre.blit(artefact2, (x,y))
				elif sprite == 'z':			#z = artefact 3
					fenetre.blit(artefact3, (x,y))
				num_case += 1
			num_ligne += 1



class Perso:

	def __init__(self, droite, gauche, haut, bas, niveau):
		#Sprites du personnage
		self.droite = pygame.image.load(ij_droite).convert_alpha()
		self.gauche = pygame.image.load(ij_gauche).convert_alpha()
		self.haut = pygame.image.load(ij_haut).convert_alpha()
		self.bas = pygame.image.load(ij_bas).convert_alpha()

		#Sprites de l'éclairage
		self.dist0 = pygame.image.load(black_25).convert_alpha() #Carré noir avec 25% de transparence
		self.dist1 = pygame.image.load(black_50).convert_alpha() #Carré noir avec 50% de transparence
		self.dist2 = pygame.image.load(black_100).convert() #Carré noir a 100%
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau


	def deplacer(self, direction):
		#Methode permettant de deplacer le personnage
		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.droite

		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.gauche

		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.haut

		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.bas

	def eclairage(self, fenetre):
		num_ligne = 0
		#On parcourt la liste du niveau
		for ligne in self.niveau.structure:
			num_case = 0
			#On parcourt les listes de lignes
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				#On vérifie que cette case n'est pas dans un rayon de 2 cases autour du perso
				if x + (2 * taille_sprite) < self.x or x - (2 * taille_sprite) > self.x or y + (2 * taille_sprite) < self.y or y - (2 * taille_sprite) > self.y :
					#On affiche un carré noir
					fenetre.blit(self.dist2, (x, y))
				num_case += 1
			num_ligne += 1

		#Affichage de la "fleur" de lumière

		# 11111
		# 10001   1 = Teinte avec 50% de transparence
		# 10*01   0 = Teinte avec 25% de transparence
		# 10001   * = Perso (Ne rien afficher dessus)
		# 11111

		#Ajout de la teinte noire avec 25% de transparence autour du perso
		fenetre.blit(self.dist0, (self.x, self.y + (1 * taille_sprite)))
		fenetre.blit(self.dist0, (self.x, self.y - (1 * taille_sprite)))
		fenetre.blit(self.dist0, (self.x + (1 * taille_sprite), self.y))
		fenetre.blit(self.dist0, (self.x - (1 * taille_sprite), self.y))
		fenetre.blit(self.dist0, (self.x + (1 * taille_sprite), self.y + (1 * taille_sprite)))
		fenetre.blit(self.dist0, (self.x - (1 * taille_sprite), self.y + (1 * taille_sprite)))
		fenetre.blit(self.dist0, (self.x + (1 * taille_sprite), self.y - (1 * taille_sprite)))
		fenetre.blit(self.dist0, (self.x - (1 * taille_sprite), self.y - (1 * taille_sprite)))

		#Ajout de la teinte noire avec 50% de transparence autour de la teinte précédente
		fenetre.blit(self.dist1, (self.x, self.y + (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x, self.y - (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (2 * taille_sprite), self.y))
		fenetre.blit(self.dist1, (self.x - (2 * taille_sprite), self.y))
		fenetre.blit(self.dist1, (self.x - (2 * taille_sprite), self.y - (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x - (2 * taille_sprite), self.y + (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (2 * taille_sprite), self.y - (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (2 * taille_sprite), self.y + (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x - (1 * taille_sprite), self.y - (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (1 * taille_sprite), self.y - (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x - (2 * taille_sprite), self.y - (1 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x - (2 * taille_sprite), self.y + (1 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x - (1 * taille_sprite), self.y + (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (1 * taille_sprite), self.y + (2 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (2 * taille_sprite), self.y - (1 * taille_sprite)))
		fenetre.blit(self.dist1, (self.x + (2 * taille_sprite), self.y + (1 * taille_sprite)))
