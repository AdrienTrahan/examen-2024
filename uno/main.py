
import random

class Carte:
    noms = ["Passe ton tour", "Change de bord", "+2", "+4", "Change de couleur"]
    couleurs = ["\x1b[0;30;41mrouge\x1b[0m", "\x1b[0;30;43mjaune\x1b[0m", "\x1b[0;30;44mbleu\x1b[0m", "\x1b[1;30;42mvert\x1b[0m"]
    def __init__(self):
        self.couleur = random.randint(0, 3)
        self.valeur = random.randint(1, 14)
        # 10 = block | 11 = change | 12 = +2 | 13 = +4
    @staticmethod
    def genererCarteNormale():
        carteChoisie = Carte()
        while (carteChoisie.valeur > 9):
            carteChoisie = Carte()
        return carteChoisie

    def obtenirNom(self, afficherCouleur=False):
        nom = self.valeur if self.valeur <= 9 else self.noms[self.valeur - 10]
        couleur = f" ({self.couleurs[self.couleur]})" if (self.valeur < 13 or afficherCouleur) else ""
        return f"{nom}{couleur}"

    def estCarteCompatible(self, cartePosee):
        return (self.couleur == cartePosee.couleur) or (self.valeur == cartePosee.valeur) or (cartePosee.valeur >= 13)
    
    @staticmethod
    def demanderCouleur():
        try:
            for i in range(len(Carte.couleurs)):
                print(f"{i + 1}. {Carte.couleurs[i]}")
            numeroCouleur = int(input("Couleur choisie: "))
            if (numeroCouleur < 1 or numeroCouleur > len(Carte.couleurs)):
                raise Exception;
            return numeroCouleur - 1
        except:
            print("Couleur invalide")
            return Carte.demanderCouleur()
        

class Paquet:
    def __init__(self):
        self.carte = Carte.genererCarteNormale();

    def estJeuPossible(self, main):
        for carte in main.cartes:
            if (self.carte.estCarteCompatible(carte)):
                return True
        return False
    
    def jouer(self, carte, jeu):
        if (carte.valeur > 9):
            match carte.valeur:
                case 10:
                    jeu.circuler()
                    print(f"Tour de joueur {jeu.joueurAJouer + 1} passé")
                case 11:
                    jeu.changerBord()
                    print(f"Le jeu change de bord!")
                case 12:
                    jeu.joueurs[jeu.prochainJoueur()].main.ajouterCarte()
                    jeu.joueurs[jeu.prochainJoueur()].main.ajouterCarte()
                case 13:
                    for _ in range(4):
                        jeu.joueurs[jeu.prochainJoueur()].main.ajouterCarte()
                    carte.couleur = Carte.demanderCouleur()
                case 14:
                    carte.couleur = Carte.demanderCouleur()
        self.carte = carte

class Jeu:
    joueurs = []
    jouerAJouer = 0;
    orientation = 1;
    def __init__(self, tailleInitiale=7):
        self.paquet = Paquet()
        self.nombreJoueur = self.demanderNombreJoueur();
        for _ in range(self.nombreJoueur):
            self.joueurs.append(Joueur(tailleInitiale))

        self.stack = Paquet()
        while (min([len(joueur.main.cartes) for joueur in self.joueurs]) != 0):
            print(f"\nCarte: {self.paquet.carte.obtenirNom(afficherCouleur=True)}")
            print(f"\nTour de joueur {self.jouerAJouer + 1}")
            self.joueurs[self.jouerAJouer].joue(self)
            self.circuler();
        for i in range(len(self.joueurs)):
            if (len(self.joueurs[i].main.cartes) == 0):
                print(f"Joueur {i + 1} remporte")
    
    def circuler(self):
        self.jouerAJouer += self.orientation;
        self.jouerAJouer %= len(self.joueurs);

    def changerBord(self):
        self.orientation *= -1;

    def demanderNombreJoueur(self):
        try:
            nombreJoueur = int(input("Nombre de joueurs: "))
            if (nombreJoueur <= 1):
                raise Exception;
            return nombreJoueur
        except:
            print("Nombre invalide.")
            return self.demanderNombreJoueur()
        
    def prochainJoueur(self):
        return (self.jouerAJouer + self.orientation) % self.nombreJoueur

class Main:
    def __init__(self, taille):
        self.cartes = []
        for _ in range(taille):
            self.ajouterCarte()
            
    def ajouterCarte(self):
        self.cartes.append(Carte())
    
    def afficherCartes(self, jeu):
        for i in range(len(self.cartes)):
            carteValideDebut = "" if jeu.paquet.carte.estCarteCompatible(self.cartes[i]) else "\x1b[5;30;40m"
            carteValideFin = "" if jeu.paquet.carte.estCarteCompatible(self.cartes[i]) else "\x1b[0m"
            print(f"{i + 1}. {carteValideDebut}{self.cartes[i].obtenirNom()}{carteValideFin}")

    def trierMain(self):
        self.cartes.sort(key=lambda carte: (carte.couleur, carte.valeur))

class Joueur:
    def __init__(self, taille):
        self.main = Main(taille);

    def joue(self, jeu):
        if (jeu.paquet.estJeuPossible(self.main)):
            self.main.trierMain();
            numerosValides = [i for i, carte in enumerate(self.main.cartes) if jeu.paquet.carte.estCarteCompatible(carte)]
            print(f"Vos cartes: ({len(self.main.cartes)})")
            self.main.afficherCartes(jeu);
            numeroCarte = self.demanderCarte(numerosValides);
            jeu.paquet.jouer(self.main.cartes[numeroCarte], jeu)
            del self.main.cartes[numeroCarte]
        else:
            print("Jeu impossible. Carte pigée")
            self.main.ajouterCarte()
        
    def demanderCarte(self, numerosValides):
        try:
            numeroCarte = int(input("Carte choisie: ")) - 1;
            if (numeroCarte < 0 or numeroCarte >= len(self.main.cartes) or (numeroCarte not in numerosValides)):
                raise Exception;
            return numeroCarte
        except:
            print("Numéro de carte invalide.")
            return self.demanderCarte(numerosValides)
    


jeu = Jeu()
