#!usr/bin/python3
########################################################################
## Code pour le déchiffrement par bloc PRESENT24 d'un message chiffré ##
########################################################################

def permutation_inverse(registre: int) -> int:
    """Couche linéaire : permutation inverse bit-à-bit"""
    liste_permut = [6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17]
    # on récupère les bits 0 et 23 du registre d'entrée que l'on met dans un nouveau registre car
    # ils ne sont pas permutés.
    nouveau_registre = registre & (1 | (1 << 23))

    # i la position du bit à permuter; j <=> P(i) la position où mettre le bit à permuter
    for j, i in enumerate(liste_permut, 1): ### j et i inversés (différence avec la fonction permutatoin) ###
        if registre & (1 << i): # si le bit à la postion i vaut 1 alors
            # on met un 1 à la position j dans le nouveau registre
            nouveau_registre = nouveau_registre | (1 << j)
        # sinon on laisse le 0 à la position j
    
    return nouveau_registre


def substitution_inverse(registre: int) -> int:
    """Substituion inverse 4 bits par 4 bits"""
    boite_si = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]

    # on applique la boite si sur les 4 premiers bits
    nouveau_registre = boite_si[registre & 0xf]
    for j in range(1, 6):
        # on decale le registre de 4 bits vers la droite
        registre = registre >> 4

        # on réapplique la boite si sur les 4 premiers bits
        #que l'on met à la bonne place dans le registre
        nouveau_registre = nouveau_registre | (boite_si[registre & 0xf] << (4*j))

    return nouveau_registre


def dechiffrement(chiffre: int or str, sous_cles: list[int]) -> int:
    """dechiffrement par bloc PRESENT24 d'un message chiffré de 24 bits
    avec une liste de 11 sous clés de 24 bits"""
    # verifie que la taille du message est d'au maximum 24 bits
    if chiffre > 0xffffff:
        print("Le chiffré fait plus de 24 bits.")
        return 0

    chiffre = chiffre ^ sous_cles[-1]
    for i in range(9, -1, -1): # de 9 à 0
        ## on permute le message (voir la fonction de permutation_inverse) ##
        chiffre = permutation_inverse(chiffre)
        
        ## substitution du message ##
        chiffre = substitution_inverse(chiffre)

        ## xor du message avec la sous clé Ki ##
        chiffre = chiffre ^ sous_cles[i]

    return chiffre


if __name__ == '__main__':
    import sys
    from cadencement_cle import cadencement_cle

    # recuperation du message chiffré et de la clé donnés en argument par l'utilisateur
    chiffre = int(sys.argv[1], 16)
    cle = int(sys.argv[2], 16)

    print(f"Déchiffrement PRESENT24 du message chiffré {chiffre:06x} avec la clé {cle:06x}")
    # creation de la liste de sous clés grace au cadencement de clé
    sous_cles = cadencement_cle(cle)

    # déchiffrement du message
    clair = dechiffrement(chiffre, sous_cles)
    print(f"Le message clair est {clair:06x}.")
