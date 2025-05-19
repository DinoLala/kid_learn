import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import streamlit as st

import streamlit as st


# st.subheader('For more information, please visit US Chess official website')

# st.header(':orange[Having Fun learning with pricess LAM!!]')
st.markdown("""
<h2 style='color: orange;'>🎉 Having Fun Learning with Lam! 🧡</h2>

Welcome to our playful corner of learning!  
Here, math becomes an adventure full of puzzles, smiles, and brainy fun. 🧠✨  

Let's count, add, subtract — and most of all, enjoy every step of the journey.  
Perfect for curious little minds in **K–2**! 📚👧🧒
""", unsafe_allow_html=True)

#import streamlit as st
import random
import streamlit as st
import random

st.markdown("<h2 style='color: orange;'>🌟 Problem of the Day 🌟</h2>", unsafe_allow_html=True)

# Initialize the problem only once
if "question" not in st.session_state:
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

    # Generate multiple choices
    choices = [answer]
    while len(choices) < 4:
        wrong = answer + random.choice([-3, -2, -1, 1, 2, 3])
        if wrong not in choices and wrong >= 0:
            choices.append(wrong)
    random.shuffle(choices)

    # Store in session state
    st.session_state.question = question
    st.session_state.answer = answer
    st.session_state.choices = choices
    st.session_state.answered = False

# Show question and choices
st.markdown(f"<h3>{st.session_state.question}</h3>", unsafe_allow_html=True)
user_answer = st.radio("Choose your answer:", st.session_state.choices, key="user_choice")

# Check answer
if st.button("Check Answer") and not st.session_state.answered:
    if user_answer == st.session_state.answer:
        st.success("🎉 Yay! That's correct!")
    else:
        st.error(f"Oops! The correct answer is {st.session_state.answer}.")
    st.session_state.answered = True

# Allow new question only after answering
if st.session_state.answered and st.button("Try Another"):
    for key in ["question", "answer", "choices", "user_choice", "answered"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# Optional fun image
# st.image("data/happy-dance-excited.gif", width=200)
st.image("app/data/happy-dance-excited.gif")
