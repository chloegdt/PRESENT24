#!usr/bin/python3
###########################################################
## Attaque par le milieu contre le chiffrement PRESENT24 ##
###########################################################

from opti import chiffrement, dechiffrement
from cadencement_cle import cadencement_cle
from time import time
try:
    from numba import njit, objmode
except ImportError:
    print("numba module not installed: pip install numba")
    exit(-1)


@njit
def creation_listes(clair, chiffre):
    """
    creation des listes contenant tous les messages intermediaires
    (chiffrement du clair et dechiffrement du chiffre)
    avec toutes les cles possibles
    les listes sont chaqunes composées de 2^24 tuples
    de la forme (message_intermediaire, cle_utilise pour obtenir ce message)
    """
    # initialisation
    liste_m = []
    liste_c = []
    cmpt = 0

    for cle in range(0xffffff+1):
        # calcul des sous cles
        sous_cles = cadencement_cle(cle)

        # chiffrement du clair pour obtenir le message intermediaire
        liste_m.append((chiffrement(clair, sous_cles), cle))

        # dechiffrement du chiffre pour obtenir le message intermediaire
        liste_c.append((dechiffrement(chiffre, sous_cles), cle))

        # mise a jour de la bar de chargement pour l'utilisateur
        if cle%1000000 == 0:
            with objmode(): print("[", "#"*cmpt, " "*(17-cmpt), "]", sep='', end='\r')
            cmpt += 1

    print("[#################]")
    return liste_m, liste_c


@njit
def verif_cles(k1, k2, clair, chiffre, liste_cles):
    """verifie que chiffre = 2PRESENT24_k1,k2(clair)"""
    # creation des sous cles
    sous_cles_k1 = cadencement_cle(k1)
    sous_cles_k2 = cadencement_cle(k2)

    # double chiffrement du message clair avec les sous cles
    chiffre_test = chiffrement(chiffrement(clair, sous_cles_k1), sous_cles_k2)

    # verifie si on obtient le chiffre attendu
    if chiffre_test == chiffre:
        liste_cles.append((k1, k2))


@njit
def cherche_elements_communs(liste1, liste2, clair, chiffre):
    """
    cherche les elements communs de deux listes triées par ordre croissant
    du premier element de leur tuple
    """
    # initialisation
    liste_cles = [(0, 0) for _ in range(0)] # liste vide qui contiendra un tuple de deux entiers
    idx1 = 0 # indice de la liste liste1
    idx2 = 0 # indice de la liste liste2
    cmpt = 0 # statut de la barre de chargement
    nbr_elements_communs = 0

    # barre de chargement
    with objmode(): print("[                 ]", end='\r')
    
    while idx1<len(liste1) and idx2<len(liste2):
        # les messages intermediaires sont les memes
        if liste1[idx1][0] == liste2[idx2][0]:
            # on teste les cles
            verif_cles(liste1[idx1][1], liste2[idx2][1], clair, chiffre, liste_cles)
            nbr_elements_communs += 1

            # on regarde si les prochains elements de liste1 ont le meme message intermediaire
            i = 1
            while (idx1 + i) < len(liste1) and liste1[idx1+i][0] == liste2[idx2][0]:
                verif_cles(liste1[idx1+i][1], liste2[idx2][1], clair, chiffre, liste_cles)
                nbr_elements_communs += 1
                i += 1

            # on regarde si les prochains elements de liste2 ont le meme message intermediaire
            i = 1
            while (idx2 + i) < len(liste2) and liste1[idx1][0] == liste2[idx2+i][0]:
                verif_cles(liste1[idx1][1], liste2[idx2+i][1], clair, chiffre, liste_cles)
                nbr_elements_communs += 1
                i += 1
            idx1 += 1
            idx2 += 1

        # on incremente l'indice de la liste qui a le plus petit message intermediaire
        elif liste1[idx1][0] > liste2[idx2][0]:
            idx2 += 1
        else: idx1 += 1

        # mise a jour de la barre de chargement
        if (idx1+idx2)%2000000 == 0:
            with objmode(): print("[", "#"*cmpt, " "*(17-cmpt), "]", sep='', end='\r')
            cmpt += 1

    print("[#################]")
    with objmode: print(nbr_elements_communs, end='')
    return liste_cles


@njit
def attaque(clair1, chiffre1, clair2, chiffre2):
    """
    implementation de l'attaque par le milieu contre 2PRESENT24
    avec deux couples clair-chiffre afin de trouver touts les couples de cles possibles
    """
    # creation des listes Lm et Lc
    with objmode(): print("Début de l'attaque avec le message clair :", hex(clair1), "et le chiffré :", hex(chiffre1))
    print("Création des listes...")
    with objmode(start="f8", debut_attaque="f8"): start = time(); debut_attaque = time()
    liste_m, liste_c = creation_listes(clair1, chiffre1)
    with objmode(start="f8"): print("Listes crées en", time() - start, "secondes.\n"); start = time()

    # trie de la liste Lc
    liste_c.sort(key=lambda x: x[0])
    with objmode(start="f8"): print("Liste_m triée en", time() - start, "secondes."); start = time()
    
    # trie de la list Lm
    liste_m.sort(key=lambda x: x[0])
    with objmode(start="f8"): print("Liste_c triée en", time() - start, "secondes.\n"); start = time()

    # recherche des elements communs
    # et verification de ces derniers avec le deuxieme couple clair-chiffre
    with objmode(): print("Suite de l'attaque avec le message clair :", hex(clair2), "et le chiffré :", hex(chiffre2))
    print("Recherche et test des elements communs entre les deux listes...")
    liste_cles = cherche_elements_communs(liste_m, liste_c, clair2, chiffre2)
    with objmode(): print(" elements communs trouvés et testés en", time() - start, "secondes.\n")

    print(len(liste_cles), "couple(s) de clés trouvé(s) :")
    for couple in liste_cles:
        with objmode(): print("k1 =", hex(couple[0]), "| k2 =", hex(couple[1]))
    with objmode(): print("Attaque terminée en", time() - debut_attaque, "secondes.")


def main():
    """gestion des arguments"""
    import sys
    
    if len(sys.argv) == 1:
        print("Aucun argument trouvé :")
        print(" '-c' pour utilisé les couples clair-chiffé de Chloé GODET")
        print(" '-m' pour utilisé les couples clair-chiffé de Marwane GROSJACQUES")
        print(" '[clair1] [chiffre1] [clair2] [chiffre2]' pour lancer une attaque sur deux couples au choix")
        print()
        print("Exemples :")
        print(" 'python3 attaque.py -c'")
        print(" 'python3 attaque.py -m'")
        print(" 'python3 attaque.py 36ca6c 0ded87 a92a08 d68fb5'")
        exit(1)

    # lancement de l'attaque sur les couples clair-chiffre de Chloé GODET
    if sys.argv[1] == "-c":
        attaque(0x4efbd3, 0x9c45fa, 0xfdd4e0, 0x4ae29b) # Chloé

    # lancement de l'attaque sur les couples clair-chiffre de Marwane GROSJACQUES
    elif sys.argv[1] == "-m":
        attaque(0x0c1a0d, 0x783e29, 0x8556cc, 0x5e51d4) # Marwane

    # lancement de l'attaque sur deux couples clair-chiffre au choix
    else: 
        clair1 = int(sys.argv[1], 16)
        chiffre1 = int(sys.argv[2], 16)
        clair2 = int(sys.argv[3], 16)
        chiffre2 = int(sys.argv[4], 16)
        attaque(clair1, chiffre1, clair2, chiffre2)

if __name__ == "__main__":
    main()
