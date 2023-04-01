import utilities as ut
import encryption as enc
import decryption as dec
import MITM

import time

if __name__ == "__main__":
    lm = []
    lc = []

    t0 = time.time()
    keys = MITM.generate_all_keys(24)
    t1 = time.time()
    print("generer les clés :", t1-t0)

    t0 = time.time()
    for key in keys:
        lm.append(enc.encrypt("ea82ec", key))
        lc.append(dec.decrypt("4b8784", key))
    t1 = time.time()
    print("remplissage de lm et lc :", t1-t0)

    t0 = time.time()
    lm.sort()
    lc.sort()
    t1 = time.time()
    print("triage lm et lc :", t1-t0)