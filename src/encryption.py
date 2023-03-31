import utilities as ut

def sub_xor(state, key):
    if type(state) != str or type(key) != str:
        return -1

    lstate = len(state)
    lkey = len(key)

    if lstate != lkey:
        return -1
    
    result = str()

    for i in range(lstate):
        xored = int(state[i], 2) ^ int(key[i], 2)
        result += str(xored)

    return result

def substitution(state):
    hexa = ut.bin24_to_hex(state)

    if hexa == -1:
        raise ValueError("Une erreur s'est produit pour la conversion en hexadécimal.")
    
    result = str()

    for i in range(len(hexa)):
        match hexa[i]:
            case '0':
                result += ut.hex_to_bin4('c')
            case '1':
                result += ut.hex_to_bin4('5')
            case '2':
                result += ut.hex_to_bin4('6')
            case '3':
                result += ut.hex_to_bin4('b')
            case '4':
                result += ut.hex_to_bin4('9')
            case '5':
                result += ut.hex_to_bin4('0')
            case '6':
                result += ut.hex_to_bin4('a')
            case '7':
                result += ut.hex_to_bin4('d')
            case '8':
                result += ut.hex_to_bin4('3')
            case '9':
                result += ut.hex_to_bin4('e')
            case 'a':
                result += ut.hex_to_bin4('f')
            case 'b':
                result += ut.hex_to_bin4('8')
            case 'c':
                result += ut.hex_to_bin4('4')
            case 'd':
                result += ut.hex_to_bin4('7')
            case 'e':
                result += ut.hex_to_bin4('1')
            case 'f':
                result += ut.hex_to_bin4('2')
            case _:
                return -1
            
    return result

def permutation(state):
    array = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17, 23]
    result = str()

    for index in array:
        result += state[index]

    return result
