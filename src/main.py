from utilities import *
from encryption import *
from decryption import *
from MITM import *

import sys

## Sauvegarde les éléments de "save" dans un fichier qui a pour chemin "path".
# Cette fonction est là pour enregistrer les couples (k1, k2) trouvés.
def save_in_file(save, path):
    with open(path, 'w') as file:
        file.write('\n'.join('{} : {}'.format(keys[0], keys[1]) for keys in save))


if __name__ == "__main__":
    if sys.argv[1] == "enc":
        if (len(sys.argv) != 4):
            print("error : missing command line arguments (expected 3) given", len(sys.argv)-1)
        
        print("Message chiffré:", encrypt(sys.argv[2], sys.argv[3]))
    
    if sys.argv[1] == "dec":
        if (len(sys.argv) != 4):
            print("error : missing command line arguments (expected 3) given", len(sys.argv)-1)
        
        print("Message déchiffré:", decrypt(sys.argv[2], sys.argv[3]))
    
    if sys.argv[1] == "mitm":
        if (len(sys.argv) != 6):
            print("error : missing command line arguments (expected 5) given", len(sys.argv)-1)
        
        found = MITM((sys.argv[2], sys.argv[3]), (sys.argv[4], sys.argv[5]))
        print("Les clés sont présentes dans le fichier save.txt.")
        save_in_file(found, "save.txt")