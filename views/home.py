import os
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BANNER_PATH = os.path.join(PROJECT_ROOT, "assets", "banner.png")

def home_page():
    st.title("Drag Cipher Transmission (DCT-36)")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    banner_path = os.path.join(project_root, "assets", "banner.png")


    if not os.path.isfile(banner_path):
        st.error("File banner.png tidak ditemukan di folder assets!")
    else:
        st.image(banner_path, width=1000)

    st.markdown("""
    **Drag Cipher Transmission (DCT-36)** adalah sistem kriptografi orisinal
    yang menggabungkan prinsip *Substitution Shift Cipher* dengan data teknis
    performa kendaraan dari simulator **Car Driving Indonesia (CDID)**.

    Algoritma ini memanfaatkan *DNA transmisi kendaraan* sebagai sumber
    kunci dinamis untuk mengamankan pesan teks.
    """)

    st.markdown("---")

    st.subheader("1. Filosofi Kunci (Dual-Key System)")
    st.markdown("""
    **Key 1 — Engine Code**  
    Menentukan basis data transmisi kendaraan yang digunakan.

    **Key 2 — Gear Shifting**  
    Nilai pergeseran diambil dari batas kecepatan setiap gear,
    membentuk sistem polialfabetik.
    """)

    st.subheader("2. Standar Karakter & Modulo 36")
    st.markdown("""
    - A–Z → indeks 0–25  
    - 0–9 → indeks 26–35
    """)

    st.subheader("3. Model Matematis")
    st.markdown("""
    Enkripsi  : `C = (P + S) mod 36`  
    Dekripsi  : `P = (C − S) mod 36`
    """)

    st.subheader("4. Aturan Sistem")
    st.markdown("""
    - Spasi diabaikan  
    - Spesifikasi kendaraan harus standar  
    - Gear berotasi secara looping
    """)

    st.subheader("Keunikan DCT-36")
    st.markdown("""
    Perubahan performa kendaraan (buff/nerf) secara otomatis
    mengubah kunci kriptografi, menciptakan sistem keamanan
    dinamis berbasis komunitas otomotif.
    """)
