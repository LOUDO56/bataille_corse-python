from carte import*
import random
from file import*
from random import randint

class jeuDeCarte:
    def distribution(nbjoueur):
        """Fonction permettant d'initialiser le paquet de cartes en les distribuants ensuite aux joueurs"""
        paquetDeCarte = [] # création du parquet de cartes
        for c in "Trèfle", "Coeur", "Pique", "Carreau":
            for v in range(2,15):
                paquetDeCarte.append(Carte(c,v))
        random.shuffle(paquetDeCarte) # mélange
        paquetJoueur = file(nbjoueur) # création des listes pour réparties les cartes aux joueurs
        distribution = int(52/nbjoueur) # calcul pour savoir combien de cartes seront répartie aux joueurs
        joueur = 0 # index pour gérer les distributions de cartes
        for carte in paquetDeCarte: # on parcours la liste des paquet des cartes
            paquetJoueur.ajouter(joueur,carte,"au dessus") # distribution de la première carte du paquet au joueur
            joueur += 1
            if joueur >= nbjoueur:
                joueur = 0
        return paquetJoueur
    
    def joueur_suivant(adversaire, paquetJoueur):
        adversaire += 1
        if adversaire > paquetJoueur.lenPaquetAll()-1:
            adversaire =  0
        while paquetJoueur.lenPaquet(adversaire) == 0:
            adversaire += 1
            if adversaire > paquetJoueur.lenPaquetAll()-1:
                adversaire = 0
        return adversaire
    
    def carte_meme_valeur(nbjoueur, paquetJoueur):
        random_joueur = randint(0,nbjoueur-1)
        while paquetJoueur.lenPaquet(random_joueur) == 0:
            random_joueur = randint(0,nbjoueur-1)
        return random_joueur

