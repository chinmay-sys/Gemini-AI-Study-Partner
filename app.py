# Gemini AI Study Partner
import streamlit as st
from google import genai
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# GEMINI CLIENT
client = genai.Client(api_key="AIzaSyCS_PEp3N3RiqHtxUp8iplW-kbo7Qn3_o4")

def chatbot(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=user_input
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# SIDEBAR – USER PROFILE
with st.sidebar:
    st.markdown("## 👤 User Profile")
    st.markdown("---")

    username = st.text_input("Name", value="Guest User")
    role = st.selectbox("Role", ["Student", "Developer", "Researcher", "Other"])

    theme = st.radio("Theme", ["Dark", "Darker"], index=0)

    st.markdown("---")
    st.markdown("## 🤖 Bot Info")
    st.markdown("- **Name:** Gemini AI")
    st.markdown("- **Model:** Gemini Flash")
    st.markdown("- **Status:** 🟢 Online")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.welcomed = False
        st.rerun()

# THEME STYLES
if theme == "Dark":
    bg_color = "#0e1117"
    user_bg = "#1f2937"
    bot_bg = "#111827"
else:
    bg_color = "#07090f"
    user_bg = "#111827"
    bot_bg = "#030712"

st.markdown(f"""
<style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        font-family: 'Segoe UI', sans-serif;
    }}

    .main {{
        max-width: 900px;
        margin: auto;
    }}

    .header {{
        text-align: center;
        padding: 10px 0 10px 0;
    }}

    .header h1 {{
        margin-bottom: 4px;
        font-size: 34px;
    }}

    .header p {{
        margin-top: 0;
        font-size: 15px;
        color: #9ca3af;
    }}

    .user-msg {{
        background-color: {user_bg};
        padding: 12px 16px;
        border-radius: 12px;
    }}

    .bot-msg {{
        background-color: {bot_bg};
        padding: 12px 16px;
        border-radius: 12px;
    }}

    footer {{
        visibility: hidden;
    }}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main">
    <div class="header">
        <h1>🤖 Gemini AI Assistant</h1>
        <p>Your calm, reliable AI companion for questions and ideas</p>
    </div>
</div>
""", unsafe_allow_html=True)

# CHAT STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "welcomed" not in st.session_state:
    st.session_state.welcomed = False

# BOT WELCOME MESSAGE
if not st.session_state.welcomed:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello 👋 I’m Gemini AI. Ask me anything — I’m here to help.",
        "time": "Gemini • online"
    })
    st.session_state.welcomed = True

# CHAT DISPLAY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f"<div class='{css_class}'>{msg['content']}</div>", unsafe_allow_html=True)
        st.caption(msg["time"])

# INPUT
user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": f"{username} • {timestamp}"
    })

    with st.spinner("Gemini is thinking..."):
        reply = chatbot(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "time": f"Gemini • {timestamp}"
    })

    st.rerun()

# FOOTER
st.markdown("---")
st.markdown(
    "<center style='color:#9ca3af; font-size:14px;'>"
    "🚀 Built using Streamlit & Gemini API • Academic Demo Project"
    "</center>",
    unsafe_allow_html=True
)
