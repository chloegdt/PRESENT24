from chiffrement import chiffrement
from dechiffrement import dechiffrement
#from opti import *
from cadencement_cle import cadencement_cle


def test():
    messages_clairs =  ["000000", "ffffff", "000000", "f955b9"]
    cles_maitres =     ["000000", "000000", "ffffff", "d1bd2d"]
    messages_chiffes = ["bb57e6", "739293", "1b56ce", "47a929"]

    print("       |        | chiffré | chiffré |          ")
    print(" clair |   clé  | attendu | obtenu  | dechiffré")
    print("-------+--------+---------+---------+----------")
    for i in range(4):
        cle_maitre = int(cles_maitres[i], 16)
        sous_cles = cadencement_cle(cle_maitre)
        clair = int(messages_clairs[i], 16)
        chiffe_attendu = int(messages_chiffes[i], 16)
        chiffre_obtenu = chiffrement(clair, sous_cles)
        dechiffre = dechiffrement(chiffre_obtenu, sous_cles)
        print(f"{clair:06x} | {cle_maitre:06x} | {chiffe_attendu:06x}  | {chiffre_obtenu:06x}  | {dechiffre:06x}")

if __name__ == "__main__":
    test()
