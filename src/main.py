from utilities import *
from encryption import *
from decryption import *
from MITM import *

from time import time

def save_in_file(save, path):
    with open(path, 'w') as file:
        file.write('\n'.join('{} : {}'.format(keys[0], keys[1]) for keys in save))

if __name__ == "__main__":
    found = MITM("ea82ec", "4b8784", 8)