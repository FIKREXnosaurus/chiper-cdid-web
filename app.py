import streamlit as st

from views.home import home_page
from views.cipher_ui import cipher_page
from views.minigame import game_page

# ======================================================
# APP CONFIG
# ======================================================
st.set_page_config(
    page_title="Drag Cipher Transmission (CTC-36)",
    layout="wide"
)

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Menu",
    ["Home", "Encrypt / Decrypt", "Mini Game"]
)

# ======================================================
# ROUTING
# ======================================================
if menu == "Home":
    home_page()

elif menu == "Encrypt / Decrypt":
    cipher_page()

elif menu == "Mini Game":
    game_page()

# ======================================================
# FOOTER
# ======================================================
def footer():
    st.markdown("---")

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px;">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                 width="20"/>
            <span style="font-size:14px;">
                Created by <strong>FIKREXnosaurus</strong> —
                <a href="https://github.com/FIKREXnosaurus" target="_blank">
                    github.com/FIKREXnosaurus
                </a>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

footer()
