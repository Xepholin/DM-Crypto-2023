## La fonction convertit "word", un nombre en base 2, puis retourne le même nombre en base 16 (en retirant 0x).
def bin4_to_hex(word):
    if len(word) != 4:
        raise ValueError("Le nombre donné ne contient pas exactement 4 bits, {}".format(word))
    
    return hex(int(word, 2))[2:]


## La fonction renvoie une chaîne de caractère, qui est le résultat final du passage d'un nombre en base 2 en base 16.
def bin_to_hex(word):
    return ''.join([bin4_to_hex(word[i:i+4]) for i in range(0, len(word), 4)])


## Renvoie une partie du nombre en base 2, la partie renvoyée est ("target"x4)e bits suivants
def bin_tar(word, target):
    if type(word) != str or type(target) != int:
        raise TypeError("Le type de la cible ou du mot n'est pas valide")
    elif 0 < len(word)/4 < target:
        raise ValueError("Le valeur de la cible n'est pas valide, min : 0 / max: {}".format(type(word)))
    
    start = (target - 1) * 4
    split = word[start:start+4]

    return split


## La fonction convertit "word", une chaîne de caractère d'un nombre en base 16, pour le renvoyer en base 2
def hex_to_bin(word):
    bin_str = ""
    
    for c in word:
        num = int(c, 16)
        for i in range(3, -1, -1):
            bin_str += str((num >> i) & 1)  # Insère les bits les plus à gauche en premier dans "bin_str"

    return bin_str