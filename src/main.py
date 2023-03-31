import encryption as enc
import utilities as ut

if __name__ == "__main__":

    msg = "010010101001001110011010"
    key = "010101111100011111100010"

    xored = enc.sub_xor(msg, key)
    