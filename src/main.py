import utilities as ut
import encryption as enc
import decryption as dec

if __name__ == "__main__":
    vect = [("bb57e6", "000000"), ("739293", "000000"), ("1b56ce", "ffffff"), ("47a929", "d1bd2d")]

    for tuple in vect:
        msg, master = tuple
        print(msg, master, dec.decrypt(msg, master))

    print("exemple =", ut.bin_to_hex(enc.sub_xor(ut.hex_to_bin("fb54b3"), ut.hex_to_bin("400355"))))