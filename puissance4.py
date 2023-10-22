"""
PUISSANCE 4
MENU VALENTIN
"""
import pygame as py
import time

# Initialiser pygame
py.init()

# JEUX DE COULEURS
BLANC: tuple = (255, 255, 255)
ROUGE: tuple = (255, 0, 0)
JAUNE: tuple = (255, 255, 0)
NOIR: tuple = (0, 0, 0)
BLEU: tuple = (0, 0, 255)
# POLICE
POLICE = py.font.SysFont("arial", 20, bold=True, italic=False)

# Taille de la fenêtre
SCREEN = py.display.set_mode((800, 800))
# Couleur de fond en blanc
SCREEN.fill((255, 255, 255))


class Couleur:
    __rgb: tuple

    def __init__(self):
        self.__rgb = BLANC


    def getRGB(self) -> tuple:
        return self.__rgb

    def setRGB(self, couleur: tuple):
        self.__rgb = couleur



class Pion:
    __posI: int
    __posJ: int
    __couleur: Couleur

    def __init__(self, posI: int, posJ: int):
        self.__posI = posI
        self.__posJ = posJ
        self.__couleur = Couleur()


    def getCouleur(self) -> Couleur:
        return self.__couleur

    def getPosition(self) -> tuple:
        return self.__posI, self.__posJ


class Plateau:
    __plateau: list

    def __init__(self):
        self.__plateau = [[Pion(i, j) for j in range(7)] for i in range(6)]
        self.__cmpt = 1


    def getPlateau(self) -> list:
        return self.__plateau

    def getPion(self, posI, posJ) -> Pion:
        return self.__plateau[posI][posJ]

    def trouverEmplacementLibre(self, posJ: int) -> int:
        if self.getPion(0, posJ).getCouleur().getRGB() != BLANC: # emplacement déjà occupé
            print("je suis occupé")
            return -1
        else:
            cmpt = 1
            # le but est de parcourir chaque ligne tant que la couleur est blanche
            for cmpt in range(1, 6):
                couleurRGB = self.getPion(cmpt, posJ).getCouleur().getRGB()
                if couleurRGB != BLANC:
                    cmpt -= 1
                    break
            return cmpt

    def verifierVictoire(self, posI: int, posJ: int, couleur: tuple) -> bool:
        self.__cmpt = 1
        i, j = posI, posJ
        # On regarde du pion vers le côté gauche
        while j > 0:
            res = self.regarderConditionVictoire(i, j - 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                j -= 1
            else:
                break
        # On regarde du pion vers le côté droit
        i, j = posI, posJ
        while j < 6:
            res = self.regarderConditionVictoire(i, j + 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                j += 1
            else:
                break
        # Réinitialisation du compteur
        self.__cmpt = 1
        # On regarde en bas du pion
        i, j = posI, posJ
        while i < 5:
            res = self.regarderConditionVictoire(i + 1, j, couleur)
            if res == 1:
                return True
            elif res == 0:
                i += 1
            else:
                break
        # Réinitialisation du compteur
        self.__cmpt = 1
        # on regarde à la diagone gauche haut
        i, j = posI, posJ
        while i > 0 and j > 0:
            res = self.regarderConditionVictoire(i - 1, j - 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                i -= 1
                j -= 1
            else:
                break
        # On regarde à la diagonale droite bas
        i, j = posI, posJ
        while i < 5 and j < 6:
            res = self.regarderConditionVictoire(i + 1, j + 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                i += 1
                j += 1
            else:
                break
        # Réinitialisation du compteur
        self.__cmpt = 1
        # On regarde à la diagonale gauche bas
        i, j = posI, posJ
        while i < 5 and j > 0:
            res = self.regarderConditionVictoire(i + 1, j - 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                i += 1
                j -= 1
            else:
                break
        # On regarde à la diagonale droite haut
        i, j = posI, posJ
        while i > 0 and j < 6:
            res = self.regarderConditionVictoire(i - 1, j + 1, couleur)
            if res == 1:
                return True
            elif res == 0:
                i -= 1
                j += 1
            else:
                break
        return False


    def regarderConditionVictoire(self, posI: int, posJ: int, couleur: tuple) -> int:
        if self.getPion(posI, posJ).getCouleur().getRGB() == couleur:
            self.__cmpt += 1
            if self.__cmpt == 4:
                return 1
            else:
                return 0
        else:
            return -1

    def verifExAEquo(self) -> bool:
        for i in range(7):
            if self.getPion(0, i).getCouleur().getRGB() == BLANC:
                return False
        return True


    def printPlateau(self):
        traits = " " # cela correspond à un demi espace
        for i in range(7):
            traits += "--"
        print(traits)
        for i in range(6):
            listePion = "|"
            for j in range(7):
                if self.getPion(i,j).getCouleur().getRGB() == BLANC:
                    listePion += " |"
                elif self.getPion(i,j).getCouleur().getRGB() == JAUNE:
                    listePion += "J|"
                else:
                    listePion += "R|"
                if j == 6:
                    print(listePion)
        print(traits)



class Affichage:
    def __init__(self, plateau: Plateau):
        self.__emplacementTexte = (100, 100)
        self.__texteJeu = "Au tour du joueur jaune"
        self.__label = POLICE.render(self.__texteJeu, True, NOIR)
        self.__matPions = []
        self.__plateau = plateau
        self.__ecartement = 90
        self.__tailleCercle = 40



    def afficherTexte(self):
        self.__label = POLICE.render(self.__texteJeu, True, NOIR)
        py.draw.rect(SCREEN, BLANC, (self.__emplacementTexte[0], self.__emplacementTexte[1], self.__label.get_width() +
                                     250, self.__label.get_height()))
        SCREEN.blit(self.__label, self.__emplacementTexte)


    def actualiserTexte(self, isAuTourDuJaune: bool):
        if isAuTourDuJaune:
            self.__texteJeu = "Au tour du joueur jaune"
        else:
            self.__texteJeu = "Au tour du joueur rouge"
        self.afficherTexte()
        py.display.flip()

    def texteFinDeJeu(self, couleurGagnant: tuple):
        if couleurGagnant == JAUNE:
            self.__texteJeu = "Le joueur jaune a gagné!"
        elif couleurGagnant == ROUGE:
            self.__texteJeu = "Le joueur rouge a gagné!"
        else:
            self.__texteJeu = "Ex aequo!"
        self.afficherTexte()
        py.display.flip()


    def afficherPlateau(self):
        py.draw.rect(SCREEN, BLEU, (50, 165, 98 * 7, 98 * 6))


    def afficherPions(self):
        posX = 120
        posY = 150
        colonnes = len(self.__plateau.getPlateau()[0])
        lignes = len(self.__plateau.getPlateau())

        for i in range(lignes):
            posY+= self.__ecartement
            l = []
            for j in range(colonnes):
                # dessiner un cercle transparant avec un contour noir
                py.draw.circle(SCREEN, NOIR, (posX, posY), self.__tailleCercle, 3)
                # dessiner un cercle blanc
                l.append(py.draw.circle(SCREEN, self.__plateau.getPion(i, j).getCouleur().getRGB(), (posX, posY),
                                        self.__tailleCercle - 3, 0))
                if j == colonnes - 1:
                    posX = 120
                    self.__matPions.append(l)
                else:
                    posX += self.__ecartement



    def getMatricePions(self) -> list:
        return self.__matPions

    def setPion(self, posI: int, posJ: int, rgb: tuple):
        posXY = self.convertirPosMatriceEnPosEcran(posI, posJ)
        self.__matPions[posI][posJ] = py.draw.circle(SCREEN, rgb, (posXY[1], posXY[0]), self.__tailleCercle - 3, 0)
        py.display.flip()

    def convertirPosMatriceEnPosEcran(self, posI: int, posJ: int) -> tuple:
        return 240 + posI * self.__ecartement, 120 + posJ * self.__ecartement

    def convertirPosEcranEnPosMatrice(self, posX: float, posY:float) -> tuple:
        return int(round(((posY - 240) / self.__ecartement), 0)), int(round((posX - 120) / self.__ecartement, 0))

    def initialiserAffichagePlateau(self):
        self.afficherPlateau()
        self.afficherPions()
        self.afficherTexte()
        py.display.flip()



class Jeu:
    __isAuTourDuJaune: bool
    __affichage: Affichage
    __plateau: Plateau

    def __init__(self):
        self.__isAuTourDuJaune = True
        self.__plateau = Plateau()
        self.__affichage = Affichage(self.__plateau)
        self.__aUnGagnant = False
        self.__aUnAExoquo = False

        running = True
        mettreAJourEcran = False


        self.__affichage.initialiserAffichagePlateau()

        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False

                # permet d'économiser les ressources en mettant à jour le plateau uniquement s'il y a une action
                # utilisateur (click de souris ou frappe de clavier)
                if event.type == py.MOUSEBUTTONDOWN or event.type == py.KEYUP:
                    if event.type == py.MOUSEBUTTONDOWN:
                        if self.actionSouris():
                            mettreAJourEcran = True
                    elif event.type == py.KEYUP:
                        if self.actionClavier(event):
                            mettreAJourEcran = True

            if mettreAJourEcran:
                py.display.update()
                mettreAJourEcran = False
                if self.__aUnGagnant:
                    running = False
                    if self.__isAuTourDuJaune:
                        self.__affichage.texteFinDeJeu(JAUNE)
                    else:
                        self.__affichage.texteFinDeJeu(ROUGE)
                elif self.__aUnAExoquo:
                    running = False
                    self.__affichage.texteFinDeJeu(())
                else:
                    self.__isAuTourDuJaune = not self.__isAuTourDuJaune
                    self.__affichage.actualiserTexte(self.__isAuTourDuJaune)
        time.sleep(10) # 15 secondes pour que le jeu se ferme
        py.quit()



    def actionSouris(self) -> bool:
        mouseX, mouseY = py.mouse.get_pos()
        for listeCercles in self.__affichage.getMatricePions():
            for cercle in listeCercles:
                if cercle.collidepoint(mouseX, mouseY):
                    j = self.__affichage.convertirPosEcranEnPosMatrice(mouseX, mouseY)[1]
                    return self.placerPion(j)


    def actionClavier(self, event: py.event.Event) -> bool:
        if event.dict.get('key') == 49:
            return self.placerPion(0)
        elif event.dict.get('key') == 50:
            return self.placerPion(1)
        elif event.dict.get('key') == 51:
            return self.placerPion(2)
        elif event.dict.get('key') == 52:
            return self.placerPion(3)
        elif event.dict.get('key') == 53:
            return self.placerPion(4)
        elif event.dict.get('key') == 54:
            return self.placerPion(5)
        elif event.dict.get('key') == 55:
            return self.placerPion(6)

    def placerPion(self, j: int) -> bool:
        i = self.__plateau.trouverEmplacementLibre(j)
        if i == -1:
            return False
        elif self.__isAuTourDuJaune:
            couleur = JAUNE
        else:
            couleur = ROUGE
        self.__plateau.getPion(i, j).getCouleur().setRGB(couleur)
        self.__affichage.setPion(i, j, couleur)
        self.__aUnGagnant = self.__plateau.verifierVictoire(i, j, couleur)
        self.__aUnAExoquo = self.__plateau.verifExAEquo()
        self.__plateau.printPlateau()
        return True



Jeu()