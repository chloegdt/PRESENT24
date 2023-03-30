#!usr/bin/python3
####################################################################
## Code pour le chiffrement par bloc PRESENT24 d'un message clair ##
####################################################################


def permutation(registre: int) -> int:
    """Couche linéaire : permutation bit-à-bit"""
    liste_permut = [6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17]
    # on récupère les bits 0 et 23 du registre d'entrée que l'on met dans un nouveau registre car
    # ils ne sont pas permutés.
    nouveau_registre = registre & (1 | (1 << 23))

    # i la position du bit à permuter; j <=> P(i) la position où mettre le bit à permuter
    for i, j in enumerate(liste_permut, 1):
        if registre & (1 << i): # si le bit à la postion i vaut 1 alors
            # on met un 1 à la position j dans le nouveau registre
            nouveau_registre = nouveau_registre | (1 << j)
        # sinon on laisse le 0 à la position j
    
    return nouveau_registre


def substitution(registre: int) -> int:
    """Substitution 4 bits par 4 bits"""
    boite_s = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    # on subsitue les 4 premiers bits du message que l'on garde en mémoire
    nouveau_registre = boite_s[registre & 0xf]
    for j in range(1, 6):
        # on deplace les 4 prochains bits au niveau des bits de poids faible
        registre = registre >> 4

        # on subsitue ensuite ces bits grâce à la boite de substitution
        # que l'on ajoute au nouveau message à la bonne place
        nouveau_registre = nouveau_registre | (boite_s[registre & 0xf] << (4*j))

    return nouveau_registre


def chiffrement(message, sous_cles) -> int:
    """chiffrement par bloc PRESENT24 d'un message clair de 24 bits avec une liste de 11 sous clés de 24 bits"""
    # verifie que la taille du message est d'au maximum 24 bits
    if message > 0xffffff:
        print("Le message fait plus de 24 bits.")
        return

    # commence les 10 tours
    for i in range(10):
        ## xor du message avec la sous clé Ki ##
        message = message ^ sous_cles[i]

        ## substitution du message ##
        message = substitution(message)
        
        ## on permute le message (voir la fonction de permutation) ##
        message = permutation(message)

    # on finit par renvoyer le xor du message avec la dernière sous clé, c'est à dire le chiffré
    return message ^ sous_cles[-1]


if __name__ == "__main__":
    import sys
    from cadencement_cle import cadencement_cle

    if len(sys.argv) < 2:
        print("Deux arguments sont nécessaires :")
        print(" - Le message clair en hexadecimal (precedé ou non de 0x)")
        print(" - La clé en hexadecimal (precedé ou non de 0x)")
        print("exemple : python3 chiffrement.py 0xaf34e 32c")
        exit(1)

    # recuperation du message clair et de la clé donnés en argument par l'utilisateur
    clair = int(sys.argv[1], 16)
    cle = int(sys.argv[2], 16)

    print(f"Chiffrement PRESENT24 du message clair {clair:06x} avec la clé {cle:06x}")
    # creation de la liste de sous clés grace au cadencement de clé
    sous_cles = cadencement_cle(cle)

    # chiffrement du message
    chiffre = chiffrement(clair, sous_cles)
    print(f"Le chiffré est {chiffre:06x}.")
