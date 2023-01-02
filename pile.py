class pile:
    def __init__(self):
        """Création de la liste des cartes posées aux milieu"""
        self.carte_milieu = []
        
    def poser(self, carte):
        """Ajouter la carte posée à la liste des cartes aux milieu"""
        self.carte_milieu.append(carte)
        
    def recuperer(self, joueur, paquetJoueur):
        """Donner les cartes du milieu au joueur"""
        for i in range(len(self.carte_milieu)):
            paquetJoueur.ajouter(joueur,self.carte_milieu.pop(),"en dessous")
            
    def sommet(self):
        """Rechercher l'emplacement d'une carte précise"""
        if self.carte_milieu == []:
            return None
        return self.carte_milieu[-1]
            
    def lenPaquetMilieu(self):
        """Savoir la longueur des cartes aux milieu"""
        return len(self.carte_milieu)