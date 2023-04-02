from utilities import *
from encryption import *
from decryption import *
from MITM import *

from time import time

if __name__ == "__main__":

    """
    vect = [("000000", "000000"), ("ffffff", "000000"), ("000000", "ffffff"), ("f955b9", "d1bd2d")]

    t0 = time()
    for tuple in vect:
        msg, master = tuple
        print(msg, master, encrypt(msg, master))
    t1 = time()
    print("déchiffrement :", t1-t0)
    """

    t0 = time()
    keys = generate_all_keys(24)
    t1 = time()
    print("generer les clés :", t1-t0)

    t0 = time()

    lm = [(encrypt("ea82ec", key), key) for key in keys]
    lc = [(decrypt("4b8784", key), key) for key in keys]

    t1 = time()
    print("remplissage de lm et lc :", t1-t0)

    t0 = time()
    lm.sort()
    lc.sort()
    t1 = time()
    print("triage lm et lc :", t1-t0)

    t0 = time()
    equal = []
    llm = len(lm)
    llc = len(lc)

    if llm != llc:
        raise ValueError("LLM et LLC n'ont pas la même taille.")

    lm_count = 0
    lc_count = 0

    while(lm_count != llm and lc_count != llc):
        lm_msg, lm_key = lm[lm_count]
        lc_msg, lc_key = lc[lc_count]

        if lm_msg == lc_msg:
            equal.append((lm_key, lc_key))
            
            if lm_count <= lc_count:
                lm_count += 1
            elif lm_count > lc_count:
                lc_count += 1
            else:
                raise ValueError("Problème de comparaison entre lm_count et lc_count, ({} : {}).".format(lm_count, lc_count))


        elif lm_msg < lc_msg:
            lm_count += 1
        elif lm_msg > lc_msg:
            lc_count += 1
        else:
            raise ValueError("Problème de comparaison entre le message chiffré et le message déchiffré, ({} : {}).".format(lm_msg, lc_msg))
    t1 = time()
    print("recherche des mêmes messages lm et lc :", t1-t0)

    for couple in equal:
        k1, k2 = couple
        print(k1, k2)