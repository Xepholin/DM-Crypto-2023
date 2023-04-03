from utilities import bin_to_hex
from encryption import encrypt
from decryption import decrypt

from itertools import product, chain
from multiprocessing import Process, Manager
from time import time

def generate_all_keys(size_key):
    return list(map(bin_to_hex, ["".join(i) for i in product("01", repeat=size_key)]))

def chunks(l, n):
    lengh = len(l)
    return [l[i:i+n] for i in range(0, lengh, n)]

def slice_generate_all_keys(start, stop, size_key, save):
    save.append([bin_to_hex(bin(i)[2:].zfill(size_key)) for i in range(start, stop)])

def slice_encrypt(message, keys_slice, save):
    save.append([(encrypt(message, key), key) for key in keys_slice])

def slice_decrypt(message, keys_slice, save):
    save.append([(decrypt(message, key), key) for key in keys_slice])

def multi_generate_keys(nb_core):
    t0 = time()

    manager = Manager()
    keys = manager.list()
    part = int(2**24 / nb_core)
    process_keys = [Process(target=slice_generate_all_keys, args=[i, part + i, 24, keys]) for i in range(0, 2**24, part)]

    for proc in process_keys:
        proc.start()
    
    for proc in process_keys:
        proc.join()
    
    keys = list(chain.from_iterable(keys))
    manager.shutdown()

    t1 = time()
    print("nb de clés:", len(keys))
    print("génération des clés: {} sec".format(t1-t0))

    return keys

def multi_enc_dec(couple1, couple2, keys_slice):
    t2 = time()
    m1, c1 = couple1
    m2, c2 = couple2
    
    manager = Manager()
    lm1 = manager.list()
    lc1 = manager.list()
    lm2 = manager.list()
    lc2 = manager.list()

    process_list = []

    for sliced in keys_slice:
        p1 = Process(target=slice_encrypt, args=[m1, sliced, lm1])
        process_list.append(p1)
        p1.start()
        p2 = Process(target=slice_decrypt, args=[c1, sliced, lc1])
        process_list.append(p2)
        p2.start()

        p3 = Process(target=slice_decrypt, args=[m2, sliced, lm2])
        process_list.append(p2)
        p3.start()

        p4 = Process(target=slice_decrypt, args=[c2, sliced, lc2])
        process_list.append(p2)
        p4.start()

    for proc in process_list:
        proc.join()

    lm1 = list(chain.from_iterable(lm1))
    lc1 = list(chain.from_iterable(lc1))
    lm2 = list(chain.from_iterable(lm2))
    lc2 = list(chain.from_iterable(lc2))

    print("taille des 2 listes du couple1:", len(lm1), ":", len(lc1))
    print("taille des 2 listes du couple2:", len(lm2), ":", len(lc2))
    manager.shutdown()

    t3 = time()
    print("création des 4 listes: {} sec".format(t3-t2))

    return lm1, lc1, lm2, lc2

def find_equal_list(lm, lc):
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

    return equal


def MITM(couple1, couple2, nb_core):
    
    keys = multi_generate_keys(nb_core)

    chunk_size = int(len(keys) / nb_core)
    keys_slice = chunks(keys, chunk_size)

    lm1, lc1, lm2, lc2 = multi_enc_dec(couple1, couple2, keys, nb_core, keys_slice)

    t4 = time()

    lm1.sort()
    lc1.sort()
    lm2.sort()
    lc2.sort()

    t5 = time()
    print("triage des listes: {} sec".format(t5-t4))

    list_couple1 = find_equal_list(lm1, lc1)
    list_couple2 = find_equal_list(lm2, lc2)

    equal = set(list_couple1).intersection(list_couple2)
    
    return equal