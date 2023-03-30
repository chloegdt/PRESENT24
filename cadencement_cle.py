try:
    from numba import njit
except ImportError:
    print("numba module not installed: pip install numba")
    exit(-1)

@njit
def cadencement_cle(cle_maitre):
    """docstring""" 
    boite_s = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    # on cree le registre k en deplaçant la cle vers les bits de poids fort 
    k = [cle_maitre << 16, 0]
    
    sous_cles = [0]
    for i in range(1,11):
        # on met a jour le registre
        # 1ere etape : pivotement de 61 positions vers la gauche 
        # [k79k78...k40][k39...k1k0]
        # [k18k17...k59][k58...k20k19]
        x = k[1] << 21 | k[0] >> 19
        y = k[0] << 21 | k[1] >> 19
        k[0] = x & 0xffffffffff
        k[1] = y & 0xffffffffff

        # 2eme etape : substitution
        x = k[0] >> 36
        x = boite_s[x]
        x = x << 36
        k[0] = k[0] & 0x0fffffffff
        k[0] = k[0] ^ x

        # 3ème étape : xor avec le numéro du tour
        i = i << 15
        k[1] = k[1] ^ i

        # extraction de la sous clé
        sous_cles.append(k[1] >> 16)

    return sous_cles
