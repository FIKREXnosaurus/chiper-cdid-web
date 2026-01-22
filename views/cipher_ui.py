import streamlit as st
import os
import time

from cipher.encrypt import encrypt
from cipher.decrypt import decrypt
from cipher.config import CARS, CHARSET, MODULO

# ======================================================
# VEHICLE DATA (gunakan path relatif saja)
# ======================================================
VEHICLE_DATA = {
    "FTV": {
        "name": "2012 Fortuner TRD",
        "thumb": "assets/thumbs/fortuner.png",
        "image": "assets/full/fortuner.png",
    },
    "A91": {
        "name": "2017 Xpander Sport",
        "thumb": "assets/thumbs/xpander.png",
        "image": "assets/full/xpander.png",
    },
    "D56": {
        "name": "2014 Pajero Sport",
        "thumb": "assets/thumbs/pajero_d56.png",
        "image": "assets/full/pajero_d56.png",
    },
    "N15": {
        "name": "2017 Pajero Sport",
        "thumb": "assets/thumbs/pajero_n15.png",
        "image": "assets/full/pajero_n15.png",
    },
}

# ======================================================
# UI Components
# ======================================================
def vehicle_gallery():
    st.subheader("🚘 Database Kendaraan Cipher")
    cols = st.columns(len(VEHICLE_DATA))
    for col, (key, data) in zip(cols, VEHICLE_DATA.items()):
        with col:
            thumb_path = data["thumb"]
            st.image(thumb_path, width=180)
            st.caption(data["name"])
            st.caption(f"Engine: {key}")

def engine_selector():
    st.subheader("⚙️ Pilih Cipher Engine (Key 1)")
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
        image_path = data["image"]
        st.write(f"Engine image path: {image_path}")
        st.write(f"Image exists: {os.path.isfile(image_path)}")
        st.image(image_path, width=600)

    with col2:
        st.success(f"Engine Aktif: {engine_key}")
        st.caption(data["name"])
        st.markdown("### ⚙️ Gear Shifting")
        for i, g in enumerate(CARS[engine_key], start=1):
            st.markdown(f"Gear {i}: `{g}`")
        st.markdown("### 🔑 Cipher Key 2")
        st.code(CARS[engine_key])

    return engine_key

# ======================================================
# PAGE
# ======================================================
def cipher_page():
    st.title("Encrypt / Decrypt")

    vehicle_gallery()
    engine_key = engine_selector()

    with st.form("cipher_form"):
        mode = st.radio("Mode", ["Encrypt", "Decrypt"])
        label = "Plaintext Input" if mode == "Encrypt" else "Ciphertext Input"
        text = st.text_area(label, placeholder="HELLO123")
        show_process = st.checkbox("Show cipher computation steps")
        submit = st.form_submit_button("Execute")

    if not submit:
        return

    clean = text.replace(" ", "").upper()

    if not clean:
        st.warning("Input text cannot be empty.")
        return

    if show_process:
        st.subheader("Cipher Process")
        visualize_process(
            clean,
            engine_key,
            mode="encrypt" if mode == "Encrypt" else "decrypt"
        )

    st.subheader("Result")
    result = encrypt(text, engine_key) if mode == "Encrypt" else decrypt(text, engine_key)
    st.code(result)
