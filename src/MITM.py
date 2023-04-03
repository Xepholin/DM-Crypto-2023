from utilities import bin_to_hex
from encryption import encrypt
from decryption import decrypt

from itertools import product, chain
from multiprocessing import Process, Manager
from time import time

def generate_all_keys(start, stop, size_key, save):
    save.append([bin_to_hex(bin(i)[2:].zfill(size_key)) for i in range(start, stop)])

def generate_all_keys2(size_key):
    return list(map(bin_to_hex, ["".join(i) for i in product("01", repeat=size_key)]))

def chunks(l, n):
    lengh = len(l)
    return [l[i:i+n] for i in range(0, lengh, n)]

def slice_encrypt(message, keys_slice, save):
    save.append([(encrypt(message, key), key) for key in keys_slice])

def slice_decrypt(message, keys_slice, save):
    save.append([(decrypt(message, key), key) for key in keys_slice])

def MITM(clair, chiffre, nb_core):
    t0 = time()

    manager = Manager()
    keys = manager.list()
    part = int(2**24 / nb_core)
    process_keys = [Process(target=generate_all_keys, args=[i, part + i, 24, keys]) for i in range(0, 2**24, part)]

    for proc in process_keys:
        proc.start()
    
    for proc in process_keys:
        proc.join()
    
    keys = list(chain.from_iterable(keys))
    manager.shutdown()

    """
    with Manager() as manager:
        keys = manager.list()
        part = int(2**24 / nb_core)
        process_keys = [Process(target=generate_all_keys, args=[i, part + i, 24, keys]) for i in range(0, 2**24, part)]

        for proc in process_keys:
            proc.start()
        
        for proc in process_keys:
            proc.join()
        
        keys = list(chain.from_iterable(keys))
    """
    print("nb de clés:", len(keys))
    t1 = time()
    print("génération des clés: {} sec".format(t1-t0))

    t2 = time()
    
    manager_lm = Manager()
    manager_lc = Manager()
    lm = manager_lm.list()
    lc = manager_lc.list()
    process_list = []

    chunk_size = int(len(keys) / nb_core)
    keys_slice = chunks(keys, chunk_size)

    for sliced in keys_slice:
        p1 = Process(target=slice_encrypt, args=[clair, sliced, lm])
        process_list.append(p1)
        p1.start()
        p2 = Process(target=slice_decrypt, args=[chiffre, sliced, lc])
        process_list.append(p2)
        p2.start()

    for proc in process_list:
        proc.join()

    lm = list(chain.from_iterable(lm))
    lc = list(chain.from_iterable(lc))

    print("taille des 2 listes", len(lm), len(lc))
    manager_lm.shutdown()
    manager_lc.shutdown()

    t3 = time()
    print("création des 2 listes: {} sec".format(t3-t2))

    t4 = time()
    lm.sort()
    lc.sort()
    t5 = time()
    print("triage des listes: {} sec".format(t5-t4))

    t6 = time()
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
    t7 = time()
    print("recherche des mêmes messages: {} sec".format(t7-t6))
    print("il y a {} messages qui sont identiques".format(len(equal)))
    print("")
    print("temps total: {} sec".format(t7-t0))

    return equal