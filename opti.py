#####################################################################################################
## Code optimisé des fonctions de chiffrement et de dechiffrement pour l'attaque                   ##
## Ne pas diviser les fonctions en plusieurs sous-fonctions rend l'execution deux fois plus rapide ##
#####################################################################################################

try: # essaie d'importer le module de compilation
    from numba import njit
except ImportError:
    print("numba module not installed: 'pip install numba'")
    exit(-1)


@njit
def chiffrement(message, sous_cles) -> int:
    """chiffrement par bloc PRESENT24 d'un message clair de 24 bits avec une liste de 11 sous clés de 24 bits"""
    boite_s = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    liste_permut = [6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17]
    for i in range(10):
        ## xor du message avec la sous clé Ki ##
        message = message ^ sous_cles[i]

        ## substitution du message ##
        nouveau_message = boite_s[message & 0xf]
        for j in range(1, 6):
            message = message >> 4
            nouveau_message = nouveau_message | (boite_s[message & 0xf] << (4*j))
        message = nouveau_message

        ## on permute le message (voir la fonction de permutation) ##
        nouveau_message = nouveau_message & (1 | (1 << 23))
        for i, j in enumerate(liste_permut, 1):
            if message & (1 << i): nouveau_message = nouveau_message | (1 << j)
        message = nouveau_message
        
    return message ^ sous_cles[-1]


@njit
def dechiffrement(chiffre: int or str, sous_cles: list[int]) -> int:
    """dechiffrement par bloc PRESENT24 d'un message chiffré de 24 bits
    avec une liste de 11 sous clés de 24 bits"""
    liste_permut = [6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17]
    boite_si = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]

    chiffre = chiffre ^ sous_cles[-1]
    for k in range(9, -1, -1): # de 9 à 0
        ## on permute le message (voir la fonction de permutation_inverse) ##
        nouveau_chiffre = chiffre & (1 | (1 << 23))
        for j, i in enumerate(liste_permut, 1): ### j et i inversés (différence avec la fonction permutatoin) ###
            if chiffre & (1 << i): nouveau_chiffre = nouveau_chiffre | (1 << j)
        chiffre = nouveau_chiffre
        ## substitution du message ##
        nouveau_chiffre = boite_si[nouveau_chiffre & 0xf]
        for j in range(1, 6):
            chiffre = chiffre >> 4
            nouveau_chiffre = nouveau_chiffre | (boite_si[chiffre & 0xf] << (4*j))

        ## xor du message avec la sous clé Ki ##
        chiffre = nouveau_chiffre ^ sous_cles[k]

    return chiffre
