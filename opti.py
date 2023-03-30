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
        #nouveau_message = nouveau_message & (1 | (1 << 23))
        #for i, j in enumerate(liste_permut, 1):
        #    if message & (1 << i): nouveau_message = nouveau_message | (1 << j)
        #message = nouveau_message
        r = message
        message = r&(1 | (1 << 23))|(r&0x2)<<5|(r&0x4)<<10|(r&0x8)<<15|(r&0x10)>>3|(r&0x20)<<2|(r&0x40)<<7|(r&0x80)<<12|(r&0x100)>>6|(r&0x200)>>1|(r&0x400)<<4|(r&0x800)<<9|(r&0x1000)>>9|(r&0x2000)>>4|(r&0x4000)<<1|(r&0x8000)<<6|(r&0x10000)>>12|(r&0x20000)>>7|(r&0x40000)>>2|(r&0x80000)<<3|(r&0x100000)>>15|(r&0x200000)>>10|(r&0x400000)>>5
        
    return message ^ sous_cles[-1]


@njit
def dechiffrement(chiffre: int or str, sous_cles: list[int]) -> int:
    """dechiffrement par bloc PRESENT24 d'un message chiffré de 24 bits
    avec une liste de 11 sous clés de 24 bits"""
    boite_si = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]

    chiffre = chiffre ^ sous_cles[-1]
    for k in range(9, -1, -1): # de 9 à 0
        ## on permute le message (voir la fonction de permutation_inverse) ##
        #nouveau_chiffre = chiffre & (1 | (1 << 23))
        #for j, i in enumerate(liste_permut, 1): ### j et i inversés (différence avec la fonction permutatoin) ###
        #    if chiffre & (1 << i): nouveau_chiffre = nouveau_chiffre | (1 << j)
        #chiffre = nouveau_chiffre
        r = chiffre
        chiffre=r&(1 | (1 << 23))|(r&0x40)>>5|(r&0x1000)>>10|(r&0x40000)>>15|(r&0x2)<<3|(r&0x80)>>2|(r&0x2000)>>7|(r&0x80000)>>12|(r&0x4)<<6|(r&0x100)<<1|(r&0x4000)>>4|(r&0x100000)>>9|(r&0x8)<<9|(r&0x200)<<4|(r&0x8000)>>1|(r&0x200000)>>6|(r&0x10)<<12|(r&0x400)<<7|(r&0x10000)<<2|(r&0x400000)>>3|(r&0x20)<<15|(r&0x800)<<10|(r&0x20000)<<5
        
        ## substitution du message ##
        nouveau_chiffre = boite_si[chiffre & 0xf]
        for j in range(1, 6):
            chiffre = chiffre >> 4
            nouveau_chiffre = nouveau_chiffre | (boite_si[chiffre & 0xf] << (4*j))

        ## xor du message avec la sous clé Ki ##
        chiffre = nouveau_chiffre ^ sous_cles[k]

    return chiffre
