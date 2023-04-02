from itertools import product

from utilities import bin_to_hex

def generate_all_keys(size_key):
    return [str(bin_to_hex(bin(i)[2:].zfill(size_key))) for i in range(2**size_key)]

def generate_all_keys2(size_key):
    return list(map(bin_to_hex, ["".join(i) for i in product("01", repeat=size_key)]))