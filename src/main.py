import encryption as enc
import utilities as ut

if __name__ == "__main__":
    vect = [("000000", "000000"), ("ffffff", "000000"), ("000000", "ffffff"), ("f955b9", "d1bd2d")]
    
    for tuple in vect:
        msg, master = tuple
        
        print(msg, master, enc.encryp(msg, master))

    print("exemple =", ut.bin_to_hex(enc.sub_xor(ut.hex_to_bin("fb54b3"), ut.hex_to_bin("400355"))))