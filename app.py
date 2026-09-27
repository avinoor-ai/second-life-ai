import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import re

st.set_page_config(page_title="Second Life AI", page_icon="♻️", layout="wide")

# ---------------- Data ----------------
PROJECTS = [
    {
        "name": "Cardboard Phone Stand",
        "description": "phone stand mobile holder cardboard useful desk study video watching",
        "keywords": ["cardboard", "box", "paper", "phone", "mobile"],
        "materials": ["cardboard", "scissors", "glue"],
        "alternatives": {"glue": ["paper tape", "strong tape"]},
        "difficulty": "Easy",
        "time": "15–20 min",
        "advantages": [
            "Keeps a phone upright for hands-free viewing.",
            "Reuses cardboard instead of throwing it away.",
            "Can be made without buying a new phone stand."
        ],
        "steps": [
            "Draw and cut two cardboard pieces for the base and back support.",
            "Make a small front lip so the phone cannot slide forward.",
            "Join the pieces with glue. If glue is unavailable, use paper tape or strong tape.",
            "Test the stand on a flat surface and adjust the angle if needed."
        ],
        "image": "phone_stand.png"
    },
    {
        "name": "Cardboard Desk Organizer",
        "description": "desk organizer stationery pen pencil storage cardboard box useful table",
        "keywords": ["cardboard", "box", "paper", "desk", "pens", "pencils"],
        "materials": ["cardboard", "scissors", "glue", "colored paper"],
        "alternatives": {"glue": ["paper tape", "strong tape"], "colored paper": ["old newspaper", "magazine paper"]},
        "difficulty": "Easy",
        "time": "20–30 min",
        "advantages": [
            "Keeps small stationery items together.",
            "Uses an old box instead of sending it to waste.",
            "Can be customized with old paper or newspaper."
        ],
        "steps": [
            "Cut the box into sections of suitable height.",
            "Create 2–3 compartments using spare cardboard.",
            "Join the compartments with glue or paper tape.",
            "Decorate with old newspaper or magazine paper if desired."
        ],
        "image":  "desk_organizer.png"
    },
    {
        "name": "Small Cardboard Plant Holder",
        "description": "plant holder pot decoration cardboard bottle container garden reuse",
        "keywords": ["cardboard", "box", "bottle", "paper", "plant", "garden"],
        "materials": ["cardboard", "scissors", "glue", "small container"],
        "alternatives": {"glue": ["paper tape", "strong tape"]},
        "difficulty": "Medium",
        "time": "25–35 min",
        "advantages": [
            "Turns packaging into a decorative holder.",
            "Encourages reuse and creative thinking.",
            "Can be used as an outer decorative sleeve around a small container."
        ],
        "steps": [
            "Measure a cardboard sleeve slightly larger than the container.",
            "Cut and fold the cardboard to form the sleeve.",
            "Secure the edges with glue or strong tape.",
            "Place a leak-proof container inside before adding a plant."
        ],
        "image": "plant_holder.png"
    }
]

# ---------------- Simple AI recommendation engine ----------------
@st.cache_resource
def build_model():
    corpus = [p["description"] for p in PROJECTS]
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(corpus)
    return vec, matrix

vectorizer, matrix = build_model()

def normalize(text):
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())

def recommend(user_text, wanted=""):
    query = normalize(user_text + " " + wanted)
    q = vectorizer.transform([query])
    scores = cosine_similarity(q, matrix)[0]
    ranked = sorted(zip(PROJECTS, scores), key=lambda x: x[1], reverse=True)
    # Always return useful suggestions, even when the input is short.
    return [p for p, score in ranked[:3]]

def material_state(project, available_text):
    available = set(normalize(available_text).split())
    states = []
    for m in project["materials"]:
        key = m.lower().split()[0]
        present = key in available or m.lower() in normalize(available_text)
        states.append((m, present))
    return states

def chatbot_reply(message, project, available):
    msg = normalize(message)
    if any(x in msg for x in ["glue", "adhesive"]):
        if "glue" in [m.lower() for m in project["materials"]]:
            alts = project["alternatives"].get("glue", [])
            return f"No problem! For this project, you can try {', '.join(alts)} instead of glue, if you have them. I can also update the steps for you."
    if "don't have" in msg or "dont have" in msg or "not have" in msg or "missing" in msg:
        found = [m for m in project["materials"] if m.lower().split()[0] not in normalize(available).split()]
        if found:
            suggestions = []
            for m in found:
                if m in project["alternatives"]:
                    suggestions.append(f"{m}: {', '.join(project['alternatives'][m])}")
            if suggestions:
                return "Let's adapt the project. Possible alternatives — " + "; ".join(suggestions) + "."
            return "Tell me which missing material you want to replace, and I will suggest an alternative."
    if "advantage" in msg or "benefit" in msg:
        return "Main advantages: " + " ".join(project["advantages"])
    if "steps" in msg or "how" in msg or "make" in msg:
        return "Here are the steps: " + " ".join(f"{i+1}. {s}" for i, s in enumerate(project["steps"]))
    return "I can help you change materials, explain the steps, or tell you the advantages. For example: “I don't have glue” or “Why is this useful?”"

# ---------------- Styling ----------------
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 22px 26px; border: 2px solid #222; border-radius: 22px; background: #f7f7f7;}
.card {padding: 18px; border: 1px solid #bbb; border-radius: 18px; background: white;}
.small {color:#555; font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>♻️ SECOND LIFE AI</h1><p><b>Don’t throw it. Transform it.</b><br>Tell the AI what you have, what you want, and what you are missing.</p></div>', unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns(2)
with col1:
    items = st.text_area("📦 What do you have?", placeholder="Example: cardboard box, plastic bottle, newspaper", height=110)
with col2:
    wanted = st.text_input("🎯 What do you want to make?", placeholder="Example: something useful for my desk")

if st.button("✨ ASK AI", type="primary", use_container_width=True):
    if not items.strip():
        st.warning("Please enter at least one item you have.")
    else:
        st.session_state["suggestions"] = recommend(items, wanted)
        st.session_state["selected"] = None
        st.session_state["available"] = items

suggestions = st.session_state.get("suggestions", [])
if suggestions:
    st.subheader("🤖 AI Suggestions")
    cols = st.columns(3)
    for i, p in enumerate(suggestions):
        with cols[i]:
            st.image(p["image"], use_container_width=True)
            st.markdown(f"### {p['name']}")
            st.write(f"**Difficulty:** {p['difficulty']}  \n**Time:** {p['time']}")
            st.write(p["advantages"][0])
            if st.button("MAKE THIS", key=f"choose_{i}", use_container_width=True):
                st.session_state["selected"] = p
                st.rerun()

project = st.session_state.get("selected")
if project:
    st.divider()
    st.header(f"🛠️ {project['name']}")
    left, right = st.columns([1, 1.25])
    with left:
        st.image(project["image"], caption="Reference picture", use_container_width=True)
        st.markdown("### ⭐ Advantages")
        for a in project["advantages"]:
            st.write("• " + a)
    with right:
        st.markdown("### 🧰 Materials")
        states = material_state(project, st.session_state.get("available", ""))
        for m, present in states:
            st.write(("✅ " if present else "❌ ") + m)
        st.markdown("### 📋 Steps")
        for i, step in enumerate(project["steps"], 1):
            st.write(f"**{i}.** {step}")

    st.markdown("### 💬 Second Life AI Chatbot")
    st.caption("Ask me to adapt the project. Example: “I don't have glue” or “Tell me the advantages.”")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.write(msg)
    user_msg = st.chat_input("Type your question...")
    if user_msg:
        st.session_state.chat.append(("user", user_msg))
        reply = chatbot_reply(user_msg, project, st.session_state.get("available", ""))
        st.session_state.chat.append(("assistant", reply))
        st.rerun()

st.divider()
with st.expander("🧠 How the AI works"):
    st.write("This prototype uses TF-IDF text features and cosine similarity to match the user's materials and goal with reuse-project descriptions. The chatbot then adapts instructions using the project's material alternatives.")
with st.expander("🔐 AI Ethics"):
    st.write("The prototype does not ask for names, phone numbers, addresses, or private documents. AI suggestions are recommendations, not guarantees. Users should check that materials and tools are safe and suitable before making a project.")
with st.expander("📊 Project idea for Excel"):
    st.write("You can record the number of times each item is entered and make charts such as “Most reused items” and “Most selected projects.”")
