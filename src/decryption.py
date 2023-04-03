from utilities import bin_to_hex, hex_to_bin4, hex_to_bin
from encryption import cadence, sub_xor

def substite_reverse(state):
    sbox = ['5', 'e', 'f', '8', 'c', '1', '2', 'd', 'b', '4', '6', '3', '0', '7', '9', 'a']

    hexa = bin_to_hex(state)
    lhexa = len(hexa)

    return "".join(([hex_to_bin4(sbox[int(hexa[i], 16)]) for i in range(lhexa)]))

def permute_reverse(state):
    if type(state) != str:
        raise TypeError("Le type du l'état n'est pas validé, donné {}.".format(type(state)))
    elif len(state) != 24:
        raise ValueError("La taille de l'état n'est pas valide.")
    
    array = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22 ,5 ,11, 17 ,23]

    return "".join([state[index] for index in array])

def decrypt(message, master_key):
    state = hex_to_bin(message)
    sub_keys = cadence(master_key)

    state = sub_xor(state, sub_keys[10])

    for i in range(9, -1, -1):
        state = permute_reverse(state)
        state = substite_reverse(state)
        state = sub_xor(state, sub_keys[i])

    print(message, master_key, bin_to_hex(state), flush=True)

    return bin_to_hex(state)