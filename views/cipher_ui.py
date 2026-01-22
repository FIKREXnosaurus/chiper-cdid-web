import streamlit as st
import time

from cipher.encrypt import encrypt
from cipher.decrypt import decrypt
from cipher.config import CARS, CHARSET, MODULO

# ======================================================
# VEHICLE UI DATA
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
# VISUALIZATION CORE (VERTICAL FLOW)
# ======================================================
def visualize_process(text, engine_key, mode="encrypt"):
    speeds = CARS[engine_key]

    log_container = st.container()
    gear_container = st.container()

    log_box = log_container.empty()
    gear_box = gear_container.empty()

    log = ""

    for i, char in enumerate(text):
        if char not in CHARSET:
            continue

        gear_index = i % len(speeds)
        speed = speeds[gear_index]

        idx = CHARSET.index(char)

        if mode == "encrypt":
            result_index = (idx + speed) % MODULO
            result_char = CHARSET[result_index]
            calc = f"({idx} + {speed}) mod 36"
            label_in, label_out = "Plaintext", "Ciphertext"
        else:
            result_index = (idx - speed) % MODULO
            result_char = CHARSET[result_index]
            calc = f"({idx} - {speed}) mod 36"
            label_in, label_out = "Ciphertext", "Plaintext"

        # Update log (TOP)
        log += (
            f"Step {i+1}\n"
            f"{label_in} : {char} (Index {idx})\n"
            f"Gear      : {gear_index+1}\n"
            f"Speed     : {speed}\n"
            f"{label_out}: {calc} = {result_index} → {result_char}\n\n"
        )
        log_box.code(log)

        # Update gear shifting (BOTTOM)
        gear_text = "### Gear Shifting Status\n"
        for g, val in enumerate(speeds):
            marker = "▶" if g == gear_index else " "
            gear_text += f"{marker} Gear {g+1}: `{val}`\n"
        gear_box.markdown(gear_text)

        time.sleep(0.25)

# ======================================================
# UI COMPONENTS
# ======================================================
def vehicle_gallery():
    st.subheader("Database Kendaraan Cipher")
    cols = st.columns(len(VEHICLE_DATA))

    for col, (key, data) in zip(cols, VEHICLE_DATA.items()):
        with col:
            st.image(data["thumb"], width=180)
            st.caption(data["name"])
            st.caption(f"Engine Code: {key}")

def engine_selector():
    st.subheader("Cipher Engine Selection")

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
        st.image(data["image"], width=600)

    with col2:
        st.success(f"Engine Active: {engine_key}")
        st.caption(data["name"])
        st.markdown("### Gear Table")
        for i, g in enumerate(CARS[engine_key], start=1):
            st.markdown(f"Gear {i}: `{g}`")

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
