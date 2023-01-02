from pile import*



class file:
    def __init__(self, nbjoueur):
        """Création des paquets des joueurs"""
        self.paquetJoueur = [[] for i in range(nbjoueur)]
    
    def ajouter(self, joueur, carte, type):
        """Sert à empiler les cartes sur le paquet du joueur et d'ajouter les cartes du milieu en dessous du
        paquet du joueur"""
        if type == "au dessus":
            self.paquetJoueur[joueur].append(carte)
        if type == "en dessous":
            #Pour ajouter les cartes du milieu en dessous du paquet de carte du joueur
            self.paquetJoueur[joueur].insert(0,carte)
            
    def depiler(self, joueur):
        """Supprime la première carte du joueur et le renvoie"""
        return self.paquetJoueur[joueur].pop()
    
    def lenPaquet(self,joueur):
        """Sert à savoir le nombres de cartes d'un joueur"""
        return len(self.paquetJoueur[joueur])
    
    def lenPaquetAll(self):
        """Sert à savoir le nombres de paquet"""
        return len(self.paquetJoueur)
