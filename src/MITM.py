from utilities import bin_to_hex
from encryption import encrypt
from decryption import decrypt

from itertools import product
from multiprocessing import Process, Manager

def generate_all_keys(size_key):
    return [str(bin_to_hex(bin(i)[2:].zfill(size_key))) for i in range(2**size_key)]

def generate_all_keys2(size_key):
    return list(map(bin_to_hex, ["".join(i) for i in product("01", repeat=size_key)]))

def chunks(l, n):
    lengh = len(l)
    return [l[i:i+n] for i in range(0, lengh, n)]

def slice_encrypt(message, keys_slice, return_list):
    return_list = [(encrypt(message, key), key) for key in keys_slice]

def slice_decrypt(message, keys_slice, return_list):
    return_list = [(decrypt(message, key), key) for key in keys_slice]

def MITM(clair, chiffre):
    keys = generate_all_keys(24)

    manager_enc = Manager()
    lm = manager_enc.list()

    manager_dec = Manager()
    lc = manager_dec.list()

    chunk_size = len(keys) / 4
    keys_slice = chunks(keys, chunk_size)
    process = []

    for sliced in keys_slice:
        p = Process(target=slice_encrypt, args=(clair, sliced, lc))
        process.append(p)
        p.start()
        p = Process(target=slice_decrypt, args=(clair, sliced, lm))
        process.append(p)
        p.start()

    for proc in process:
        proc.join()

    for proc in process:
        proc.join()

    lm.sort()
    lc.sort()

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

    return equal