#!usr/bin/python3
################################################
## Attaque 'Meet in the middle' du 2PRESENT24 ##
################################################

#from opti import chiffrement, dechiffrement
from opti2 import *
from cadencement_cle import cadencement_cle
from time import time
try:
    from numba import njit, objmode
except ImportError:
    print("numba module not installed: pip install numba")
    exit(-1)


@njit
def creation_listes(clair, chiffre):
    liste_m = []
    liste_c = []
    cmpt = 0
    #print("[", " "*17, "]", end='\r')
    for cle in range(0xffffff+1):
        sous_cles = cadencement_cle(cle)
        liste_m.append((chiffrement(clair, sous_cles), cle))
        liste_c.append((dechiffrement(chiffre, sous_cles), cle))
        if cle%1000000 == 0:
            with objmode(): print("[", "#"*cmpt, " "*(17-cmpt), "]", sep='', end='\r')
            cmpt += 1

    print("[#################]")
    return liste_m, liste_c


@njit
def verif_cles(k1, k2, clair, chiffre, liste_cles):
    """doc"""
    sous_cles_k1 = cadencement_cle(k1)
    sous_cles_k2 = cadencement_cle(k2)
    chiffre_test = chiffrement(chiffrement(clair, sous_cles_k1), sous_cles_k2)
    if chiffre_test == chiffre:
        liste_cles.append((k1, k2))


@njit
def cherche_elements_communs(liste1, liste2, clair, chiffre):
    """docstring"""
    liste_cles = [(0, 0) for _ in range(0)]
    idx1 = 0
    idx2 = 0
    cmpt = 0
    nbr_elements_communs = 0
    with objmode(): print("[                 ]", end='\r')
    while idx1<len(liste1) and idx2<len(liste2):
        if liste1[idx1][0] == liste2[idx2][0]:
            verif_cles(liste1[idx1][1], liste2[idx2][1], clair, chiffre, liste_cles)
            nbr_elements_communs += 1
            i = 1
            while (idx1 + i) < len(liste1) and liste1[idx1+i][0] == liste2[idx2][0]:
                verif_cles(liste1[idx1+i][1], liste2[idx2][1], clair, chiffre, liste_cles)
                nbr_elements_communs += 1
                i += 1
            i = 1
            while (idx2 + i) < len(liste1) and liste1[idx1][0] == liste2[idx2+i][0]:
                verif_cles(liste1[idx1][1], liste2[idx2+i][1], clair, chiffre, liste_cles)
                nbr_elements_communs += 1
                i += 1
            idx1 += 1
            idx2 += 1
        elif liste1[idx1][0] > liste2[idx2][0]:
            idx2 += 1
        else:
            idx1 += 1

        if (idx1+idx2)%2000000 == 0:
            with objmode(): print("[", "#"*cmpt, " "*(17-cmpt), "]", sep='', end='\r')
            cmpt += 1

    print("[#################]")
    with objmode: print(nbr_elements_communs, end='')
    return liste_cles


@njit
def attaque(clair1, chiffre1, clair2, chiffre2):
    """doc"""
    with objmode():
        print("Début de l'attaque avec le message clair :", hex(clair1), "et le chiffré :", hex(chiffre1))
    print("Création des listes...")
    with objmode(start="f8", debut_attaque="f8"):
        start = time()
        debut_attaque = time()
    liste_m, liste_c = creation_listes(clair1, chiffre1)
    with objmode(start="f8"):
        print("Listes crées en", time() - start, "secondes.\n")
        start = time()

    liste_c.sort(key=lambda x: x[0])
    with objmode(start="f8"):
        print("Liste_m triée en", time() - start, "secondes.")
        start = time()
    
    liste_m.sort(key=lambda x: x[0])
    with objmode(start="f8"):
        print("Liste_c triée en", time() - start, "secondes.\n")
        start = time()
        print("Suite de l'attaque avec le message clair :", hex(clair2), "et le chiffré :", hex(chiffre2))
    print("Recherche et test des elements communs entre les deux listes...")
    liste_cles = cherche_elements_communs(liste_m, liste_c, clair2, chiffre2)
    with objmode():
        print(" elements communs trouvés et testés en", time() - start, "secondes.\n")

    print(len(liste_cles), "couple(s) de clés trouvé(s) :")
    for couple in liste_cles:
        with objmode():
            print("k1 =", hex(couple[0]), "| k2 =", hex(couple[1]))
    with objmode():
        print("Attaque terminée en", time() - debut_attaque, "secondes.")


def main():
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

    if sys.argv[1] == "-c":
        attaque(0x4efbd3, 0x9c45fa, 0xfdd4e0, 0x4ae29b) # Chloé
    elif sys.argv[1] == "-m":
        attaque(0x0c1a0d, 0x783e29, 0x8556cc, 0x5e51d4) # Marwane
    else:
        clair1 = int(sys.argv[1], 16)
        chiffre1 = int(sys.argv[2], 16)
        clair2 = int(sys.argv[3], 16)
        chiffre2 = int(sys.argv[4], 16)
        attaque(clair1, chiffre1, clair2, chiffre2)

if __name__ == "__main__":
    main()
