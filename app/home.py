import streamlit as st
import json
import random

# ---- Title & Welcome ----
st.markdown("""
<h2 style='color: orange;'>🎉 Having Fun Learning with Lam! 🧡</h2>

Welcome to our playful corner of learning!  
Here, math becomes an adventure full of puzzles, smiles, and brainy fun. 🧠✨  

Let's count, add, subtract — and most of all, enjoy every step of the journey.  
Perfect for curious little minds in **K–2**! 📚👧🧒
""", unsafe_allow_html=True)

# ---------- Load Brain Teasers ----------
@st.cache_data
def load_brain_questions():
    with open("app/data/brain_questions.json", "r") as f:
        return json.load(f)

brain_questions = load_brain_questions()

def get_new_brain_question():
    q = random.choice(brain_questions)
    return q["question"], q["answer"]

# ---------- Math Problem of the Day ----------
def init_math():
    if "math_question" not in st.session_state:
        op = random.choice(['+', '-', '×'])
        if op == '+':
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            answer = a + b
            question = f"{a} + {b} = ?"
        elif op == '-':
            a = random.randint(10, 50)
            b = random.randint(1, a)
            answer = a - b
            question = f"{a} - {b} = ?"
        else:  # ×
            a = random.randint(1, 10)
            b = random.randint(1, 5)
            answer = a * b
            question = f"{a} × {b} = ?"

        choices = [answer]
        while len(choices) < 4:
            wrong = answer + random.choice([-3, -2, -1, 1, 2, 3])
            if wrong not in choices and wrong >= 0:
                choices.append(wrong)
        random.shuffle(choices)

        st.session_state.math_question = question
        st.session_state.math_answer = answer
        st.session_state.math_choices = choices
        st.session_state.math_answered = False
        st.session_state.math_user_choice = None

def reset_math():
    keys = ["math_question", "math_answer", "math_choices", "math_answered", "math_user_choice"]
    for k in keys:
        st.session_state.pop(k, None)

# ---------- Brain Teaser ----------
def init_brain():
    if "brain_question" not in st.session_state:
        q, ans = get_new_brain_question()
        st.session_state.brain_question = q
        st.session_state.brain_answer = ans
        st.session_state.brain_answered = False

def reset_brain():
    for key in ["brain_question", "brain_answer", "brain_answered"]:
        st.session_state.pop(key, None)

# ---------- Main UI ----------
st.markdown("## 🧮 Math Problem of the Day")
init_math()
st.write(f"**{st.session_state.math_question}**")

math_answer = st.radio("Choose your answer:", st.session_state.math_choices, key="math_radio")

if st.button("Check Math Answer", key="check_math") and not st.session_state.math_answered:
    st.session_state.math_user_choice = math_answer
    st.session_state.math_answered = True
    if math_answer == st.session_state.math_answer:
        st.success("🎉 Yay! That's correct!")
    else:
        st.error(f"Oops! The correct answer is {st.session_state.math_answer}.")

if st.session_state.math_answered:
    if st.button("Try Another Math Problem", key="try_another_math"):
        reset_math()

st.markdown("---")

st.markdown("## 🧠 Brain Teaser of the Day")
init_brain()
st.write(f"**{st.session_state.brain_question}**")

if not st.session_state.brain_answered:
    if st.button("Show Answer", key="show_answer_brain"):
        st.session_state.brain_answered = True

if st.session_state.brain_answered:
    st.success(f"Answer: {st.session_state.brain_answer}")
    if st.button("Next Brain Teaser", key="next_brain_teaser"):
        reset_brain()
st.markdown("---")       
st.markdown("© 2025 Dinolala. All rights reserved.")
st.markdown("**Disclaimer:** Please use this app at your own risk.")