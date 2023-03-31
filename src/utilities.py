def bin4_to_hex(word):
    if len(word) != 4:
        raise ValueError("Le nombre donné ne contient pas exactement 4 bits")
    
    return hex(int(word, 2))[2:]

def bin_to_hex(word):
    string = str()
    lword = len(word)
    split = [word[i:i+4] for i in range(0, lword, 4)]

    for splited in split:
        string += bin4_to_hex(splited)
    
    return string

def bin_tar(word, target):
    if type(word) != str:
        raise TypeError("Le type du mot n'est pas validé, donné {}".format(type(word)))
    elif type(target) != int:
        raise TypeError("Le type de la cible n'est pas validé, donné {}".format(type(target)))
    elif 0 < len(word)/4 < target:
        raise ValueError("Le valeur de la cible n'est pas bon, min : 0 / max: {}".format(type(word)))
    
    start = (target - 1) * 4
    split = word[start:start+4]

    return split

def hex_to_bin4(word):
    return format(bin(int(word, 16)))[2:].zfill(4)

def hex_to_bin(word):
    lword = len(word)
    result = str()

    for i in range(lword):
        result += hex_to_bin4(word[i])
    
    return result

def print_index(word):
    for i in range(len(word)):
        print("{}:{} ".format(i, word[i]), end='')
    print("")