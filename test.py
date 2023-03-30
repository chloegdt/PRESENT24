from chiffrement import chiffrement
from dechiffrement import dechiffrement
#from opti import *
from cadencement_cle import cadencement_cle


def test():
    messages_clairs =  ["000000", "ffffff", "000000", "f955b9"]
    cles_maitres =     ["000000", "000000", "ffffff", "d1bd2d"]
    messages_chiffes = ["bb57e6", "739293", "1b56ce", "47a929"]

    print("clair  | clé    | chiffré | dechiffré")
    for i in range(4):
        cle_maitre = int(cles_maitres[i], 16)
        sous_cles = cadencement_cle(cle_maitre)
        clair = int(messages_clairs[i], 16)
        chiffre = chiffrement(clair, sous_cles)
        dechiffre = dechiffrement(chiffre, sous_cles)
        print(f"{clair:06x} | {cle_maitre:06x} | {chiffre:06x}  | {dechiffre:06x}")

if __name__ == "__main__":
    test()
