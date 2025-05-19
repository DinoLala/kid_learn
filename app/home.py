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

# -------------------- MATH QUESTION --------------------
st.markdown("<h2 style='color: orange;'>🧮 Daily Math Challenge</h2>", unsafe_allow_html=True)

# Session state for math
if "math_question" not in st.session_state:
    
    op = random.choice(['+', '-', '×'])

    if op == '+':
        a, b = random.randint(1, 50), random.randint(1, 50)
        answer = a + b
        question = f"{a} + {b} = ?"
    elif op == '-':
        a = random.randint(10, 50)
        b = random.randint(1, a)
        answer = a - b
        question = f"{a} - {b} = ?"
    else:
        a, b = random.randint(1, 10), random.randint(1, 5)
        answer = a * b
        question = f"{a} × {b} = ?"

    # Generate answer choices
    choices = [answer]
    while len(choices) < 4:
        wrong = answer + random.choice([-3, -2, -1, 1, 2, 3])
        if wrong not in choices and wrong >= 0:
            choices.append(wrong)
    random.shuffle(choices)

    # Save to session
    st.session_state.math_question = question
    st.session_state.math_answer = answer
    st.session_state.math_choices = choices
    st.session_state.math_answered = False

# Show math question
st.markdown(f"<h3>{st.session_state.math_question}</h3>", unsafe_allow_html=True)
user_math_answer = st.radio("Choose your answer:", st.session_state.math_choices, key="math_radio")

if st.button("Check Math Answer") and not st.session_state.math_answered:
    st.session_state.math_answered = True
    if user_math_answer == st.session_state.math_answer:
        st.success("🎉 Yay! That's correct!")
    else:
        st.error(f"Oops! The correct answer is {st.session_state.math_answer}.")

if st.session_state.math_answered:
    if st.button("Try Another Math"):
        for key in ["math_question", "math_answer", "math_choices", "math_answered"]:
            st.session_state.pop(key, None)
        st.stop()



# -------------------- BRAIN TEASER --------------------
st.markdown("<h2 style='color: orange;'>🧠 Problem of the Day - Brain Teaser</h2>", unsafe_allow_html=True)

# Load questions
@st.cache_data
def load_brain_questions():
    with open("app/data/brain_questions.json", "r") as f:
        return json.load(f)

@st.cache_data
def load_dummy_wrong_answers():
    with open("app/data/dummy_wrong_answers.json", "r") as f:
        return json.load(f)

def generate_wrong_answers(correct, count=3):
    wrongs = [ans for ans in dummy_wrong_answers if ans != correct]
    return random.sample(wrongs, count)

def get_new_brain_question():
    q = random.choice(brain_questions)
    correct = q["answer"]
    wrongs = generate_wrong_answers(correct)
    options = wrongs + [correct]
    random.shuffle(options)
    return q["question"], correct, options

# Load data
brain_questions = load_brain_questions()
dummy_wrong_answers = load_dummy_wrong_answers()

# Brain teaser session state
if "brain_question" not in st.session_state:
    q, a, opts = get_new_brain_question()
    st.session_state.brain_question = q
    st.session_state.brain_answer = a
    st.session_state.brain_options = opts
    st.session_state.brain_answered = False
    st.session_state.brain_user_answer = None

# Show question
st.write(f"**{st.session_state.brain_question}**")
user_brain_answer = st.radio("Choose your answer:", st.session_state.brain_options, key="brain_radio")

if st.button("Check Brain Answer") and not st.session_state.brain_answered:
    st.session_state.brain_user_answer = user_brain_answer
    st.session_state.brain_answered = True
    if user_brain_answer == st.session_state.brain_answer:
        st.success("🎉 Correct! You're a thinker!")
    else:
        st.error(f"Oops! The correct answer is: {st.session_state.brain_answer}")

if st.session_state.brain_answered:
    if st.button("Next Brain Teaser"):
        q, a, opts = get_new_brain_question()
        st.session_state.brain_question = q
        st.session_state.brain_answer = a
        st.session_state.brain_options = opts
        st.session_state.brain_answered = False
        st.session_state.brain_user_answer = None
        st.stop()

st.image("app/data/happy-dance-excited.gif", width=200)