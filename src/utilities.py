def bin4_to_hex(word):
    if len(word) != 4:
        return -1
    
    return hex(int(word, 2))[2:]

def bin24_to_hex_tar(word, target):
    lword = len(word)
    if type(word) != str or type(target) != int:
        return -1
    elif lword != 24:
        return -1
    elif lword/4 < target:
        return -1
    
    start = (target - 1) * 4
    split = word[start:start+4]

    return bin4_to_hex(split)
    

def bin24_to_hex(word):
    string = str()
    split = [word[i:i+4] for i in range(0, 24, 4)]

    for splited in split:
        string += bin4_to_hex(splited)
    
    return string

def hex_to_bin4(word):
    return format(bin(int(word, 16)))[2:].zfill(4)

def print_index(word):
    for i in range(len(word)):
        print("{}:{} ".format(i, word[i]), end='')
    print("")