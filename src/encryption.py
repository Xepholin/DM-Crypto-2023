from utilities import *

def sub_xor(state, key):
    if type(state) != str or type(key) != str:
        raise TypeError("Le type du l'état ou de la clé n'est pas valide.")
    
    lstate = len(state)
    lkey = len(key)

    if lstate != lkey:
        raise ValueError("La taille des 2 nombres sont différents {} != {}.".format(lstate, lkey))

    return "".join([str(int(state[i], 2) ^ int(key[i], 2)) for i in range(lstate)])

def substite(state):
    sbox = ['c', '5', '6', 'b', '9', '0', 'a', 'd', '3', 'e', 'f', '8', '4', '7', '1', '2']

    hexa = bin_to_hex(state)
    lhexa = len(hexa)

    return "".join([hex_to_bin4(sbox[int(hexa[i], 16)]) for i in range(lhexa)])

def permute(state):
    if type(state) != str:
        raise TypeError("Le type du l'état n'est pas validé, donné {}.".format(type(state)))
    elif len(state) != 24:
        raise ValueError("La taille de l'état n'est pas valide.")
    
    array = [0, 4, 8, 12, 16, 20, 1, 5, 9, 13, 17, 21, 2, 6, 10, 14, 18, 22, 3, 7, 11, 15, 19, 23]

    return "".join([state[index] for index in array])

def add_0(state):
    miss = 20 - len(state)

    return "".join((state, "".join(['0' for i in range(miss)])))

def cadence(key):
    register = hex_to_bin(add_0(key))
    
    lregister = len(register)
    sub_keys = []

    for i in range(1, 12):
        sub_keys.append(register[40:64])
        
        register = "".join([register[(j+61)%80] for j in range(lregister)])

        register = substite(bin_tar(register, 1)) + register[4:]

        round = str(bin(i))[2:].zfill(5)
        register = "".join((register[:60], sub_xor(register[60:65], round), register[65:]))

    return sub_keys

def encrypt(message, master_key):
    state = hex_to_bin(message)
    sub_keys = cadence(master_key)

    for i in range(10):
        state = sub_xor(state, sub_keys[i])
        state = substite(state)
        state = permute(state)

    print(message, master_key, bin_to_hex(sub_xor(state, sub_keys[10])), flush=True)

    return bin_to_hex(sub_xor(state, sub_keys[10]))