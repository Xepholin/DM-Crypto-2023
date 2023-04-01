import itertools

import utilities as ut

def generate_all_keys(size_key):
    return list(map(ut.bin_to_hex, ["".join(i) for i in itertools.product("01", repeat=size_key)]))

def generate_all_keys2(size_key):
    keys = []

    for i in range(2**size_key):
        keys.append(str(ut.bin_to_hex(bin(i)[2:].zfill(size_key))))

    return keys
