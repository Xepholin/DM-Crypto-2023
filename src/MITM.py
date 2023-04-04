from utilities import bin_to_hex
from encryption import encrypt
from decryption import decrypt

from itertools import product, chain
from multiprocessing import Process, Manager, Queue
from time import time

## Génère toutes les combinaisons de clé possible sur "size_key" bits en base 2
def generate_all_keys(size_key):
    return list(map(bin_to_hex, ["".join(i) for i in product("01", repeat=size_key)]))


## Divise la liste "l" en "n" morceaux
def chunks(l, n):
    lengh = len(l)
    return [l[i:i+n] for i in range(0, lengh, n)]


## La fonction génère les nombres en fonction l'intervalles "start", puis transforme chaque nombre en chaîne de caractère représentée en base 2
# Cette fonction est utilisée pour la parallélisation, elle ajoute le résultat dans "save"
def slice_generate_all_keys(start, stop, size_key, save):
    save.put([bin_to_hex(bin(i)[2:].zfill(size_key)) for i in range(start, stop)])


## La fonction chiffre un message avec l'aide de plusieurs clés situées dans "key_slice"
# Cette fonction est utilisée pour la parallélisation, elle ajoute le résultat dans "save"
# On se retrouve avec une liste de tuple (message chiffré, clé utilisée)
def slice_encrypt(message, keys_slice, save):
    save.put([(encrypt(message, key), key) for key in keys_slice])


## La fonction déchiffre un message avec l'aide de plusieurs clés situées dans "key_slice"
# Cette fonction est utilisée pour la parallélisation, elle ajoute le résultat dans "save"
# On se retrouve avec une liste de tuple (message déchiffré, clé utilisée)
def slice_decrypt(message, keys_slice, save):
    save.put([(decrypt(message, key), key) for key in keys_slice])


## Cette fonction est la partie principale pour la génération des combinaisons sur n bits.
# Utilisation du parallélisme afin d'accélerer le programme, elle prend en argument "nb_core" afin de déterminer le nombre de tâche au total.
def multi_generate_keys(nb_core):
    manager = Manager()
    keys_queue = manager.Queue()    # Variable pour sauvegarder le résulat des fonctions données au Process
    keys = []
    part = int((2**24) / nb_core)
    process_keys = [Process(target=slice_generate_all_keys, args=[i, part + i, 24, keys_queue]) for i in range(0, 2**24, part)]     # Liste des tâches, ici la génération des clés possibles, en fonction d'un intervalle

    for proc in process_keys:
        proc.start()

    for proc in process_keys:
        proc.join()

    while not keys_queue.empty():
        keys.extend(keys_queue.get())

    return keys


## Cette fonction cherche les éléments égaux dans 2 listes.
# Elle compare au fur et à mesure les listes en fonction de la valeur actuelle des 2.
def find_equal_list(lm, lc):
    equal = []
    llm = len(lm)
    llc = len(lc)

    if llm != llc:
        raise ValueError("LLM et LLC n'ont pas la même taille.")

    lm_count = 0
    lc_count = 0

    ## Début des comparaisons
    while(lm_count != llm and lc_count != llc):
        lm_msg, lm_key = lm[lm_count]
        lc_msg, lc_key = lc[lc_count]

        if lm_msg == lc_msg:
            equal.append((lm_key, lc_key))
            
            ## Monte dans une des 2 liste en fonction du résultat de comparaison
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


## Cette fonction est utilisé pour chiffrer et déchiffrer un couple clair-chiffré.
# Elle ajoute les 2 liste finales dans "save"
def enc_dec(couple, keys_slice, save):
    m1, c1 = couple

    lm = []
    lc = []

    process_list = []
    manager = Manager()
    result_lm = manager.Queue()
    result_lc = manager.Queue()

    for sliced in keys_slice:
        p1 = Process(target=slice_encrypt, args=[m1, sliced, result_lm])
        process_list.append(p1)
        p1.start()

        p2 = Process(target=slice_decrypt, args=[c1, sliced, result_lc])
        process_list.append(p2)
        p2.start()

    for proc in process_list:
        proc.join()

    ## Ajoute le resultat des tâches dans "lm" et "lc"
    while not result_lm.empty():
        lm.extend(result_lm.get())
    while not result_lc.empty():
        lc.extend(result_lc.get())

    manager.shutdown()

    save.put((lm, lc))


## Cette fonction est la fonction de l'attaque par le milieu du chiffrement PRESENT24.
def MITM(couple1, couple2):
    m1, c1 = couple1
    m2, c2 = couple2
    if len(m1) != len(c1) or len(m2) != len(c2) or len(c1) != len(m2):
        raise ValueError("Les couples clairs-chiffrés n'ont pas la meme taille.")
    
    keys = multi_generate_keys(8)

    if (len(keys) / 8)%1 != 0:
        raise ValueError("La taille du tableau contenant toutes les clés possibles ne donne pas une valeur entière en divisant par le nombre de coeur pour la parallélisation.")

    chunk_size = int(len(keys) / 8)
    keys_slice = chunks(keys, chunk_size)   # Sépare la liste de toutes les clés possibles en plusieurs morceaux

    manager = Manager()
    c1 = manager.Queue()
    c2 = manager.Queue()

    p1 = Process(target=enc_dec, args=[couple1, keys_slice, c1])
    p2 = Process(target=enc_dec, args=[couple2, keys_slice, c2])
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

    lm1, lc1 = c1.get()
    lm2, lc2 = c2.get()

    manager.shutdown()

    lm1.sort()
    lc1.sort()
    lm2.sort()
    lc2.sort()

    list_couple1 = find_equal_list(lm1, lc1)
    list_couple2 = find_equal_list(lm2, lc2)

    equal = set(list_couple1).intersection(list_couple2)
    
    return equal