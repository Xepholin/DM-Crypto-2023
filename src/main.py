from utilities import *
from encryption import *
from decryption import *
from MITM import *

from time import time

if __name__ == "__main__":


    t =  encrypt("ea82ec", "0cd434")
    m2 = encrypt(t, "38fa70")

    print(m2)

    t =  encrypt("113da5", "0cd434")
    m2 = encrypt(t, "38fa70")

    print(m2)
    
    """
    t0 = time()
    keys = generate_all_keys(24)
    t1 = time()
    print("generer les clés :", t1-t0)

    t0 = time()

    lm1 = [(encrypt("ea82ec", key), key) for key in keys]
    lc1 = [(decrypt("4b8784", key), key) for key in keys]
    lm2 = [(encrypt("113da5", key), key) for key in keys]
    lc2 = [(decrypt("8b0074", key), key) for key in keys]
    

    t1 = time()
    print("remplissage de lm et lc :", t1-t0)

    t0 = time()
    lm1.sort()
    lc1.sort()
    lm2.sort()
    lc2.sort()
    t1 = time()
    print("triage lm et lc :", t1-t0)

    t0 = time()
    equal1 = []
    llm1 = len(lm1)
    llc1 = len(lc1)

    if llm1 != llc1:
        raise ValueError("LLM1 et LLC1 n'ont pas la même taille.")

    lm1_count = 0
    lc1_count = 0

    while(lm1_count != llm1 and lc1_count != llc1):
        lm1_msg, lm1_key = lm1[lm1_count]
        lc1_msg, lc1_key = lc1[lc1_count]

        if lm1_msg == lc1_msg:
            equal1.append((lm1_key, lc1_key))
            
            if lm1_count <= lc1_count:
                lm1_count += 1
            elif lm1_count > lc1_count:
                lc1_count += 1
            else:
                raise ValueError("Problème de comparaison entre lm1_count et lc1_count, ({} : {}).".format(lm1_count, lc1_count))


        elif lm1_msg < lc1_msg:
            lm1_count += 1
        elif lm1_msg > lc1_msg:
            lc1_count += 1
        else:
            raise ValueError("Problème de comparaison entre le message chiffré et le message déchiffré, ({} : {}).".format(lm1_msg, lc1_msg))
    t1 = time()
    print("recherche des mêmes messages lm1 et lc1 :", t1-t0)

    t0 = time()
    equal2 = []
    llm2 = len(lm2)
    llc2 = len(lc2)

    if llm2 != llc2:
        raise ValueError("LLM2 et LLC2 n'ont pas la même taille.")

    lm2_count = 0
    lc2_count = 0

    while(lm2_count != llm2 and lc2_count != llc2):
        lm2_msg, lm2_key = lm1[lm2_count]
        lc2_msg, lc2_key = lc1[lc2_count]

        if lm2_msg == lc2_msg:
            equal2.append((lm2_key, lc2_key))
            
            if lm2_count <= lc2_count:
                lm2_count += 1
            elif lm2_count > lc2_count:
                lc2_count += 1
            else:
                raise ValueError("Problème de comparaison entre lm2_count et lc2_count, ({} : {}).".format(lm2_count, lc2_count))


        elif lm2_msg < lc2_msg:
            lm2_count += 1
        elif lm2_msg > lc2_msg:
            lc2_count += 1
        else:
            raise ValueError("Problème de comparaison entre le message chiffré et le message déchiffré, ({} : {}).".format(lm2_msg, lc2_msg))
    t1 = time()
    print("recherche des mêmes messages lm2 et lc2 :", t1-t0)

    equal = set(equal1).intersection(equal2)

    with open("save.txt", 'w') as file:
        file.write('\n'.join('{} : {}'.format(keys[0], keys[1]) for keys in equal))
    """