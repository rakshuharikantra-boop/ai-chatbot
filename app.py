import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Chatbot", layout="wide")

st.title("🤖 AI Chatbot")

# ---------- Sidebar ----------
st.sidebar.title("Chats")

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "current_chat" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat = new_id
    st.session_state.chat_sessions[new_id] = []

# New chat button
if st.sidebar.button("➕ New Chat"):
    new_id = str(uuid.uuid4())
    st.session_state.current_chat = new_id
    st.session_state.chat_sessions[new_id] = []

# Show previous chats
for chat_id in st.session_state.chat_sessions:
    if st.sidebar.button(f"Chat {chat_id[:6]}"):
        st.session_state.current_chat = chat_id

messages = st.session_state.chat_sessions[st.session_state.current_chat]

# ---------- Chat display ----------
for role, msg in messages:
    with st.chat_message(role):
        st.write(msg)

# ---------- File Upload ----------
uploaded_file = st.file_uploader("Upload file or image")

# ---------- Chat input ----------
prompt = st.chat_input("Ask something...")

if prompt:

    messages.append(("user", prompt))

    with st.chat_message("user"):
        st.write(prompt)

    # 🔗 PASTE YOUR N8N WEBHOOK HERE
    webhook_url = "https://rakshitaharikantra.app.n8n.cloud/webhook/7917e788-e022-44bc-8628-ba73e4212949/chat"

    try:
        response = requests.post(
            webhook_url,
            json={"chatInput": prompt}
        )

        data = response.json()

        if "output" in data:
            bot_reply = data["output"]
        else:
            bot_reply = str(data)

    except:
        bot_reply = "Error connecting to AI workflow"

    messages.append(("assistant", bot_reply))

    with st.chat_message("assistant"):
        st.write(bot_reply)
