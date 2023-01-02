class Carte:
    def __init__(self, c, v):
        self.couleur = c
        self.valeur = v
    def getValeur(self):
        if self.valeur == 11:
            return "Valet"
        if self.valeur == 12:
            return "Dame"
        if self.valeur == 13:
            return "Roi"
        if self.valeur == 14:
            return "As"
        return self.valeur
    def getCouleur(self):
        return self.couleur
    def getProperties(self):
        return str(self.getValeur()) + " de " + self.couleur