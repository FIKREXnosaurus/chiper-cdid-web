import streamlit as st
import time
import os

from cipher.encrypt import encrypt
from cipher.decrypt import decrypt
from cipher.config import CARS, CHARSET, MODULO

# ======================================================
# VEHICLE UI DATA (update path gambar sesuai instruksi)
# ======================================================
VEHICLE_DATA = {
    "FTV": {
        "name": "2012 Fortuner TRD",
        "thumb": "assets/fortuner.png",
        "image": "assets/fortuner_full.png",
    },
    "A91": {
        "name": "2017 Xpander Sport",
        "thumb": "assets/xpander.png",
        "image": "assets/xpander_full.png",
    },
    "D56": {
        "name": "2014 Pajero Sport",
        "thumb": "assets/pajero_d56.png",
        "image": "assets/pajero_d56_full.png",
    },
    "N15": {
        "name": "2017 Pajero Sport",
        "thumb": "assets/pajero_n15.png",
        "image": "assets/pajero_n15_full.png",
    },
}

# ======================================================
# VISUALIZATION FUNCTIONS
# ======================================================
def visualize_encrypt_process(text, engine_key):
    speeds = CARS[engine_key]
    log_box = st.empty()
    gear_box = st.empty()
    log = ""

    for i, char in enumerate(text):
        if char not in CHARSET:
            continue

        gear_index = i % len(speeds)
        speed = speeds[gear_index]

        p_index = CHARSET.index(char)
        c_index = (p_index + speed) % MODULO
        c_char = CHARSET[c_index]

        # Log
        log += (
            f"Step {i+1}\n"
            f"Plaintext : {char} (Index {p_index})\n"
            f"Gear      : {gear_index+1}\n"
            f"Speed     : {speed}\n"
            f"Cipher    : ({p_index} + {speed}) mod 36 = {c_index} → {c_char}\n\n"
        )

        log_box.code(log)

        # Gear Highlight
        gear_text = "### ⚙️ Gear Shifting\n"
        for g, val in enumerate(speeds):
            if g == gear_index:
                gear_text += f"➡️ **Gear {g+1}: `{val}` (ACTIVE)**\n"
            else:
                gear_text += f"Gear {g+1}: `{val}`\n"
        gear_box.markdown(gear_text)

        time.sleep(0.3)


def visualize_decrypt_process(text, engine_key):
    speeds = CARS[engine_key]
    log_box = st.empty()
    gear_box = st.empty()
    log = ""

    for i, char in enumerate(text):
        if char not in CHARSET:
            continue

        gear_index = i % len(speeds)
        speed = speeds[gear_index]

        c_index = CHARSET.index(char)
        p_index = (c_index - speed) % MODULO
        p_char = CHARSET[p_index]

        # Log
        log += (
            f"Step {i+1}\n"
            f"Ciphertext: {char} (Index {c_index})\n"
            f"Gear      : {gear_index+1}\n"
            f"Speed     : {speed}\n"
            f"Plaintext : ({c_index} - {speed}) mod 36 = {p_index} → {p_char}\n\n"
        )

        log_box.code(log)

        # Gear Highlight
        gear_text = "### ⚙️ Gear Shifting\n"
        for g, val in enumerate(speeds):
            if g == gear_index:
                gear_text += f"➡️ **Gear {g+1}: `{val}` (ACTIVE)**\n"
            else:
                gear_text += f"Gear {g+1}: `{val}`\n"
        gear_box.markdown(gear_text)

        time.sleep(0.3)

# ======================================================
# UI COMPONENTS
# ======================================================
def vehicle_gallery():
    st.subheader("Database Kendaraan Cipher")
    cols = st.columns(len(VEHICLE_DATA))
    for col, (key, data) in zip(cols, VEHICLE_DATA.items()):
        with col:
            # Debug check
            if not os.path.isfile(data["thumb"]):
                st.warning(f"Thumbnail not found: {data['thumb']}")
            else:
                st.image(data["thumb"], width=180)

            st.caption(data["name"])
            st.caption(f"Engine: {key}")


def engine_selector():
    st.subheader("Pilih Cipher Engine (Key 1)")
    labels = {
        f"{key} — {data['name']}": key
        for key, data in VEHICLE_DATA.items()
    }
    label = st.selectbox("Engine", list(labels.keys()))
    engine_key = labels[label]
    data = VEHICLE_DATA[engine_key]

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        # Debug check
        if not os.path.isfile(data["image"]):
            st.warning(f"Engine image not found: {data['image']}")
        else:
            st.image(data["image"], width=600)

    with col2:
        st.success(f"Engine Aktif: {engine_key}")
        st.caption(data["name"])
        st.markdown("Gear Shifting")
        for i, g in enumerate(CARS[engine_key], start=1):
            st.markdown(f"Gear {i}: `{g}`")
        st.markdown("Cipher Key 2")
        st.code(CARS[engine_key])

    return engine_key

# ======================================================
# PAGES
# ======================================================
def cipher_page():
    st.title("Encrypt / Decrypt")

    vehicle_gallery()
    engine_key = engine_selector()

    with st.form("cipher_form"):
        text = st.text_area("Masukkan teks", placeholder="HELLO123")
        mode = st.radio("Mode", ["Encrypt", "Decrypt"])
        show_process = st.checkbox("Tampilkan proses cipher", value=False)
        submit = st.form_submit_button("Proses Cipher")

    if submit:
        clean = text.replace(" ", "").upper()

        if clean == "":
            st.warning("Teks tidak boleh kosong")
        else:
            if show_process:
                st.subheader("Proses Cipher")
                if mode == "Encrypt":
                    visualize_encrypt_process(clean, engine_key)
                else:
                    visualize_decrypt_process(clean, engine_key)

            st.subheader("Hasil Akhir")
            if mode == "Encrypt":
                result = encrypt(text, engine_key)
            else:
                result = decrypt(text, engine_key)
            st.code(result)
