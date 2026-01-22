from .config import CARS, CHARSET, MODULO, clean_text

def decrypt(ciphertext, key1):
    if key1 not in CARS:
        return "Error: Mobil tidak ditemukan dalam database!"
    
    speeds = CARS[key1]
    num_gears = len(speeds)
    ciphertext = clean_text(ciphertext)
    plaintext = ""

    for i, char in enumerate(ciphertext):
        if char in CHARSET:
            c_index = CHARSET.index(char)
            s = speeds[i % num_gears]
            p_index = (c_index - s) % MODULO
            plaintext += CHARSET[p_index]

    return plaintext
