from carte import*
from jeu_de_carte import*
from pile import*
from file import*
from random import randint
import pygame, sys
import time

#Setup de la fenetre
pygame.init()
pygame.display.set_caption('Bataille Corse')
icon = pygame.image.load("assets/images/icon.png")
pygame.display.set_icon(icon)
width = 900
height = 600
screen = pygame.display.set_mode((width,height))

#Setup de l'arriere plan
bg = pygame.image.load("assets/images/background.jpg")
bg = pygame.transform.scale(bg, (width,height))

#Police et couleur
font_big = pygame.font.Font("assets/font/arial.ttf", 50)
font_high = pygame.font.Font("assets/font/arial.ttf", 40)
font_medium = pygame.font.Font("assets/font/arial.ttf", 35)
font_small = pygame.font.Font("assets/font/arial.ttf", 30)
font_tiny = pygame.font.Font("assets/font/arial.ttf", 20)
text_col = (255,255,255)


#Setup des cartes
card_bc = pygame.image.load("assets/images/carte_background.png")
carte_img = {}

#setup des sons
pygame.mixer.Channel(0).play(pygame.mixer.Sound("assets/sound/music/mainmenu_music.mp3"))
pygame.mixer.Channel(0).set_volume(0.5)


# Attente entre les événements
wait_between_card = 1

# Import des cartes
for couleur in "Carreau","Coeur","Pique","Trèfle":
    for valeur in range(2,15):
        if valeur == 14:
            valeur = "As"
        if valeur == 13:
            valeur = "Roi"
        if valeur == 12:
            valeur = "Dame"
        if valeur == 11:
            valeur = "Valet"
        rep = f"assets/images/{couleur}/{valeur}.png"
        img = pygame.image.load(rep)
        img = pygame.transform.scale(img, (110,154))
        carte_img[f"{couleur}_{valeur}"] = img

# Setup du jeu

gamestate = "PLAY"
action_player = "main_menu"
carte_milieu = pile()
winner = 0



def draw_text(text, font, text_col, x, y):
    """Afficher un text sur la fenetre"""
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
    
def main_menu(action_player):
    """Le menu principal"""
    if action_player == "main_menu":
        draw_text("Bataille Corse", font_big, text_col, 300,280)
        draw_text("Commencez", font_medium, text_col, 350,380)
        card_1 = card_bc
        card_2 = card_bc
        card_1 = pygame.transform.rotate(card_1, 25)
        card_2 = pygame.transform.rotate(card_2, -25)
        screen.blit(card_1,(300,20))
        screen.blit(card_2,(380,20))
    if action_player == "nbjoueur_selector":
        draw_text("Combien de joueurs voulez-vous ?", font_high, text_col, 150,50)
        draw_text("← Retour", font_medium, text_col, 10,550)
        y = 120
        for i in range(1,4):
            draw_text(str(i+1), font_high, text_col, 435,y)
            y += 80
            
    if action_player == "parier_joueur":
        draw_text("Sur quel joueur pariez-vous ?", font_high, text_col, 190,50)
        draw_text("← Retour", font_medium, text_col, 10,550)
        y = 120
        for i in range(0,nbjoueur):
            draw_text(str(i+1), font_high, text_col, 435,y)
            y += 80

def ingame():
    """Affichage des informations à propos des joueurs"""
    global carte_milieu
    card_player = pygame.image.load("assets/images/carte_background_small.png")
    for i in range(nbjoueur):
        if paquetJoueur.lenPaquet(i) != 0:
            if joueur_parier == i:
                col = (253,189,66)
            else:
                col = text_col
            if i == 0:
                screen.blit(card_player,(400,20))
                draw_text("Joueur 1", font_small, col, 540,80)
                draw_text(f"{paquetJoueur.lenPaquet(i)} cartes", font_tiny, text_col, 540,120)
            if i == 1:
                screen.blit(card_player,(400,430))
                draw_text("Joueur 2", font_small, col, 540,490)
                draw_text(f"{paquetJoueur.lenPaquet(i)} cartes", font_tiny, text_col, 540,530)
            if i == 2:
                card_player = pygame.transform.rotate(card_player, 90)
                screen.blit(card_player,(20,250))
                draw_text("Joueur 3", font_small, col, 45,200)
                draw_text(f"{paquetJoueur.lenPaquet(i)} cartes", font_tiny, text_col, 45,170)
                card_player = pygame.transform.rotate(card_player, -90)
            if i == 3:
                card_player = pygame.transform.rotate(card_player, -90)
                screen.blit(card_player,(730,250))
                draw_text("Joueur 4", font_small, col, 750,200)
                draw_text(f"{paquetJoueur.lenPaquet(i)} cartes", font_tiny, text_col, 750,170)
                
def message_ingame(joueur, type, carte_pose):
    """Information des coups des joueurs et des événements"""
    global carte_milieu
    screen.blit(bg, (0,0))
    if type == "playing":
        draw_text(f"Le joueur {joueur} joue", font_tiny, text_col, 390,390)
    if type == "gain_card":
        draw_text(f"Le joueur {joueur} gagne les cartes", font_tiny, text_col, 330,390)
        pygame.mixer.Channel(5).play(pygame.mixer.Sound("assets/sound/sound_effect/picking_card.wav"))
    if type == "eliminated":
        draw_text(f"Le joueur {joueur} est éliminé !", font_tiny, text_col, 390,390)
    if type == "same_card":
        draw_text(f"Le joueur {joueur} a tapé le paquet en premier !", font_tiny, text_col, 310,390)
    if type == "special_card":
        draw_text(f"Le joueur {joueur} a pioché une figure ou as", font_tiny, text_col, 310,390)
    if type == "special_card_success":
        draw_text(f"Le joueur {joueur} a réussi à pioché une figure ou as", font_tiny, text_col, 310,390)
    if type == "special_card_failed":
        draw_text(f"Le joueur {joueur} a échoué ses tentatives", font_tiny, text_col, 310,390)
    if carte_milieu.lenPaquetMilieu() != 0:
        screen.blit(carte_img[f"{carte_pose.getCouleur()}_{carte_pose.getValeur()}"],(400,220))
    draw_text(f"{carte_milieu.lenPaquetMilieu()} cartes", font_tiny, text_col, 300,285)
    ingame()
    pygame.display.flip()




while gamestate == "PLAY":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamestate = "STOP"
        if event.type== pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse=pygame.mouse.get_pos()
            # Boutton commencez
            if mouse[0] in range(350,350+210) and mouse[1] in range(380,380+35):
                if action_player == "main_menu":
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/sound_effect/button_click.wav"))
                    action_player = "nbjoueur_selector"
            # Retour
            if mouse[0] in range(10,10+150) and mouse[1] in range(550,550+40):
                if action_player == "nbjoueur_selector":
                    action_player = "main_menu"
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/sound_effect/button_click.wav"))
                if action_player == "parier_joueur":
                    action_player = "nbjoueur_selector"
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/sound_effect/button_click.wav"))
            # Selection parie joueur
            if action_player == "parier_joueur":
                y = 120
                for i in range(0,nbjoueur):
                    if mouse[0] in range(435,435+30) and mouse[1] in range(y,y+40):
                        if action_player == "parier_joueur":
                            paquetJoueur = jeuDeCarte.distribution(nbjoueur)
                            joueur_parier = i
                            pygame.mixer.pause()
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/sound_effect/button_click.wav"))
                            pygame.mixer.Channel(2).play(pygame.mixer.Sound("assets/sound/music/ingame_music.mp3"), -1)
                            pygame.mixer.Channel(2).set_volume(0.5)
                            action_player = "in-game"
                    y += 80
            # Selection nombre de joueurs
            if action_player == "nbjoueur_selector":
                y = 120
                for i in range(1,4):
                    if mouse[0] in range(435,435+30) and mouse[1] in range(y,y+40):
                        if action_player == "nbjoueur_selector":
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sound/sound_effect/button_click.wav"))
                            nbjoueur = i+1
                            action_player = "parier_joueur"
                    y += 80
            
    screen.blit(bg, (0,0))
    main_menu(action_player)
    if action_player != "in-game":
        pygame.display.flip()
    if action_player == "in-game":
        for joueur in range(paquetJoueur.lenPaquetAll()):
            if paquetJoueur.lenPaquet(joueur) != 0:
                time.sleep(wait_between_card)
                winner = joueur+1
                lenJoueur = paquetJoueur.lenPaquet(joueur) + carte_milieu.lenPaquetMilieu()
                if lenJoueur != 52:
                    carte_pose = paquetJoueur.depiler(joueur)
                    ancienne_carte = carte_milieu.sommet()
                    carte_milieu.poser(carte_pose)
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound("assets/sound/sound_effect/card_swip.wav"))
                    message_ingame(joueur+1, "playing", carte_pose)
                    if carte_milieu.lenPaquetMilieu() > 1:
                        if ancienne_carte.getValeur() == carte_pose.getValeur():
                            random_joueur = jeuDeCarte.carte_meme_valeur(nbjoueur, paquetJoueur)
                            time.sleep(2)
                            message_ingame(random_joueur+1, "same_card", carte_pose)
                            pygame.mixer.Channel(4).play(pygame.mixer.Sound("assets/sound/sound_effect/tap_card.wav"))
                            carte_milieu.recuperer(random_joueur, paquetJoueur)
                            time.sleep(2.1)
                            message_ingame(random_joueur+1, "gain_card", carte_pose)
                            time.sleep(1.5)
                    if type(carte_pose.getValeur()) == str:
                        message_ingame(joueur+1, "special_card", carte_pose)
                        time.sleep(1.3)
                        adversaire = jeuDeCarte.joueur_suivant(joueur, paquetJoueur)
                        if carte_pose.getValeur() == "As":
                            tentative = 4
                        elif carte_pose.getValeur() == "Roi":
                            tentative = 3
                        elif carte_pose.getValeur() == "Dame":
                            tentative = 2
                        elif carte_pose.getValeur() == "Valet":
                            tentative = 1
                        while tentative >= 1:
                            if paquetJoueur.lenPaquet(adversaire) > 0:
                                time.sleep(1.7)
                                carte_pose = paquetJoueur.depiler(adversaire)
                                ancienne_carte = carte_milieu.sommet()
                                carte_milieu.poser(carte_pose)
                                pygame.mixer.Channel(3).play(pygame.mixer.Sound("assets/sound/sound_effect/card_swip.wav"))
                                message_ingame(adversaire+1, "playing", carte_pose)
                                if ancienne_carte.getValeur() == carte_pose.getValeur():
                                    random_joueur = jeuDeCarte.carte_meme_valeur(nbjoueur, paquetJoueur)
                                    time.sleep(2)
                                    message_ingame(random_joueur+1, "same_card", carte_pose)
                                    pygame.mixer.Channel(4).play(pygame.mixer.Sound("assets/sound/sound_effect/tap_card.wav"))
                                    carte_milieu.recuperer(random_joueur, paquetJoueur)
                                    tentative = 0
                                    time.sleep(2.1)
                                    message_ingame(random_joueur+1, "gain_card", carte_pose)
                                    time.sleep(1.5)
                                else:
                                    if type(carte_pose.getValeur()) == str:
                                        message_ingame(adversaire+1, "special_card_success", carte_pose)
                                        carte_milieu.recuperer(adversaire, paquetJoueur)
                                        tentative = 0
                                        time.sleep(2.1)
                                        message_ingame(adversaire+1, "gain_card", carte_pose)
                                        time.sleep(1.5)
                                    else:
                                        if tentative == 1:
                                            message_ingame(adversaire+1, "special_card_failed", carte_pose)
                                            carte_milieu.recuperer(joueur, paquetJoueur)
                                            time.sleep(2.1)
                                            message_ingame(joueur+1, "gain_card", carte_pose)
                                            time.sleep(1.5)
                                        tentative -= 1
                            else:
                                adversaire = jeuDeCarte.joueur_suivant(adversaire, paquetJoueur)
                else:
                    gamestate = "STOP"

    
 


if carte_milieu.lenPaquetMilieu() != 0:
    carte_milieu.recuperer(winner-1, paquetJoueur)
    
screen.blit(bg, (0,0))
draw_text(f"Le joueur {winner} a gagné !", font_big, text_col, 250,250)
if joueur_parier+1 == winner:
    draw_text(f"Vous avez parié sur le bon joueur !", font_medium, text_col, 200,310)
else:
    draw_text(f"Vous n'aviez pas parié sur le bon joueur...", font_medium, text_col, 200,310)
pygame.display.flip()
time.sleep(5)
pygame.quit()
                        


