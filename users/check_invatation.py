import numpy as np

def check_invatation_code(code:str):
    # hash_codes = np.load("users/hash.npy", allow_pickle=True)
    # return True if code in hash_codes else False
    if code == "gnetchat":
        return True
    else:
        return False

def delete_invatation_code(code:str):
    hash_codes = np.load("users/hash.npy", allow_pickle=True)
    hash_codes = hash_codes[hash_codes != code]
    np.save("users/hash.npy", hash_codes)
