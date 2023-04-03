def bin4_to_hex(word):
    if len(word) != 4:
        raise ValueError("Le nombre donné ne contient pas exactement 4 bits")
    
    return hex(int(word, 2))[2:]

def bin_to_hex(word):
    lword = len(word)
    split = [word[i:i+4] for i in range(0, lword, 4)]
    
    return "".join([bin4_to_hex(splited) for splited in split])

def bin_tar(word, target):
    if type(word) != str or type(target) != int:
        raise TypeError("Le type de la cible ou du mot n'est pas valide")
    elif 0 < len(word)/4 < target:
        raise ValueError("Le valeur de la cible n'est pas valide, min : 0 / max: {}".format(type(word)))
    
    start = (target - 1) * 4
    split = word[start:start+4]

    return split

def hex_to_bin4(word):
    return format(bin(int(word, 16)))[2:].zfill(4)

def hex_to_bin(word):
    lword = len(word)
    
    return "".join([hex_to_bin4(word[i]) for i in range(lword)])

def print_index(word):
    for i in range(len(word)):
        print("{}:{} ".format(i, word[i]), end='')
    print("")