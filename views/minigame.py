import streamlit as st
import random

from cipher.config import CARS, CHARSET, MODULO

# ======================================================
# INIT SESSION STATE
# ======================================================
def init_state():
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "round" not in st.session_state:
        st.session_state.round = 0
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

    if "engine" not in st.session_state:
        new_round()

# ======================================================
# GAME ROUND
# ======================================================
def new_round():
    engine = random.choice(list(CARS.keys()))
    speeds = CARS[engine]

    plaintext = random.choice(CHARSET)

    gear_index = st.session_state.round % len(speeds)
    speed = speeds[gear_index]

    p_index = CHARSET.index(plaintext)
    cipher_index = (p_index + speed) % MODULO
    cipher_char = CHARSET[cipher_index]

    st.session_state.engine = engine
    st.session_state.plaintext = plaintext
    st.session_state._answer = cipher_char

# ======================================================
# MULTIPLIER
# ======================================================
def get_multiplier():
    s = st.session_state.streak
    if s >= 5:
        return 3
    if s >= 3:
        return 2
    return 1

# ======================================================
# VALIDATION
# ======================================================
def check_answer(user_input):
    if not user_input:
        return

    user_input = user_input.upper()
    correct = st.session_state._answer

    if user_input == correct:
        st.session_state.streak += 1
        mult = get_multiplier()
        st.session_state.score += 10 * mult
        st.session_state.feedback = f"Correct ×{mult}"
    else:
        st.session_state.streak = 0
        st.session_state.score = max(0, st.session_state.score - 5)
        st.session_state.feedback = f"Wrong (answer: {correct})"

    st.session_state.round += 1
    new_round()

# ======================================================
# PAGE
# ======================================================
def game_page():
    st.title("Mini Game — DCT-36 Cipher Challenge (Level 1)")

    # --------------------------------------------------
    # ANNOUNCEMENT
    # --------------------------------------------------
    st.info(
        "This mini game is currently under active development. "
        "Core mechanics are playable, but balance, difficulty, "
        "and additional modes will be refined in future updates."
    )

    init_state()

    # --------------------------------------------------
    # SCOREBOARD
    # --------------------------------------------------
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", st.session_state.score)
    c2.metric("Streak", st.session_state.streak)
    c3.metric("Multiplier", f"×{get_multiplier()}")

    st.markdown("---")

    # --------------------------------------------------
    # CHALLENGE INFO
    # --------------------------------------------------
    st.subheader("Current Challenge")

    st.markdown(f"""
    **Engine Code** : `{st.session_state.engine}`  
    **Plaintext**  : `{st.session_state.plaintext}`  
    """)

    st.caption(
        "Gear and speed are hidden. Gear shifts automatically each round."
    )

    st.markdown("---")

    # --------------------------------------------------
    # INPUT
    # --------------------------------------------------
    with st.form("minigame_form"):
        user_input = st.text_input(
            "Enter ciphertext character",
            max_chars=1
        )
        submit = st.form_submit_button("Submit")

    if submit:
        check_answer(user_input)

    # --------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------
    if st.session_state.feedback:
        if "Correct" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

    st.markdown("---")

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------
    if st.button("Reset Game"):
        st.session_state.clear()
