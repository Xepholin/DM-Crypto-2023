import utilities as ut

def sub_xor(state, key):
    if type(state) != str:
        raise TypeError("Le type du l'état n'est pas validé, donné {}.".format(type(state)))
    elif type(key) != str:
        raise TypeError("Le type de la clé n'est pas validé, donné {}.".format(type(key)))
    
    lstate = len(state)
    lkey = len(key)

    if lstate != lkey:
        raise ValueError("La taille des 2 nombres sont différents.".format)
    
    result = str()

    for i in range(lstate):
        result += str(int(state[i], 2) ^ int(key[i], 2))

    return result

def substite(state):
    sbox = ['c', '5', '6', 'b', '9', '0', 'a', 'd', '3', 'e', 'f', '8', '4', '7', '1', '2']
    result = str()

    hexa = ut.bin_to_hex(state)
    lhexa = len(hexa)

    for i in range(lhexa):
        result += ut.hex_to_bin4(sbox[int(hexa[i], 16)])

    return result

def permute(state):
    if type(state) != str:
        raise TypeError("Le type du l'état n'est pas validé, donné {}.".format(type(state)))
    elif len(state) != 24:
        raise ValueError("La taille de l'état n'est pas valide.")
    
    array = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17, 23]
    result = str()

    for index in array:
        result += state[index]

    return result

def add_0(state):
    miss = 20 - len(state)

    for _ in range(miss):
        state += '0'
    
    return state

def cadence(key):
    register = ut.hex_to_bin(add_0(key))
    
    lregister = len(register)
    sub_keys = []

    for i in range(1, 12):
        sub_keys.append(register[40:64])

        temp_key = str()

        for j in range(lregister):
            temp_key += register[(j+61)%80]
        
        register = temp_key

        register = substite(ut.bin_tar(register, 1)) + register[4:]

        round = str(bin(i))[2:].zfill(5)
        register = register[:60] + sub_xor(register[60:65], round) + register[65:]

    return sub_keys

def encryp(message, master_key):
    state = ut.hex_to_bin(message)
    sub_keys = cadence(master_key)

    for i in range(10):
        state = sub_xor(state, sub_keys[i])
        state = substite(state)
        state = permute(state)

    return ut.bin_to_hex(sub_xor(state, sub_keys[10]))