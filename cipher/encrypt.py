from .config import CARS, CHARSET, MODULO, clean_text


def encrypt(plaintext, key1):
    if key1 not in CARS:
        return "Error: Mobil tidak ditemukan dalam database!"
    
    speeds = CARS[key1]
    num_gears = len(speeds)
    plaintext = clean_text(plaintext)
    ciphertext = ""

    for i, char in enumerate(plaintext):
        if char in CHARSET:
            p_index = CHARSET.index(char)
            # Ambil speed berdasarkan rotasi gear
            s = speeds[i % num_gears]
            # Rumus Enkripsi
            c_index = (p_index + s) % MODULO
            ciphertext += CHARSET[c_index]
        else:
            # Mengabaikan karakter yang tidak terdaftar (simbol dll)
            continue
            
    return ciphertext

# UI Sederhana
if __name__ == "__main__":
    print("=== CTC-36 ENCRYPTOR ===")
    msg = input("Masukkan pesan: ")
    k1 = input("Masukkan Key 1 (FTV/A91/D56/N15): ").upper()
    
    hasil = encrypt(msg, k1)
    print(f"\nCiphertext ({k1}): {hasil}")