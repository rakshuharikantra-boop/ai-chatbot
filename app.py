import streamlit as st
import requests
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("AI Chatbot 🤖")

# --- n8n webhook URL (replace with your actual URL) ---
webhook_url = "PASTE_YOUR_N8N_WEBHOOK_URL_HERE"

# --- Lock 1: Check webhook is configured ---
if webhook_url == "PASTE_YOUR_N8N_WEBHOOK_URL_HERE":
    st.error("❌ Webhook URL is not configured. Please add your n8n webhook URL.")
    st.stop()

# --- User login ---
if "username" not in st.session_state:
    st.session_state.username = ""
if st.session_state.username == "":
    st.session_state.username = st.text_input("Enter your name to login")
    if st.session_state.username == "":
        st.stop()  # wait for user to login

# --- Chat session state per user ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
if st.session_state.username not in st.session_state.chats:
    st.session_state.chats[st.session_state.username] = []

# --- Sidebar: New Chat button ---
st.sidebar.title("Chat Controls")
new_chat_clicked = st.sidebar.button("➕ New Chat")
if new_chat_clicked:
    st.session_state.chats[st.session_state.username] = []

# --- File upload ---
uploaded_file = st.file_uploader(
    "Upload image or file",
    type=["png", "jpg", "jpeg", "pdf", "txt"]
)
if uploaded_file:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# --- Display chat history ---
for msg in st.session_state.chats[st.session_state.username]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Ask something")
if user_input:

    # --- Lock 2: Check for empty input ---
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a valid message.")
        st.stop()

    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.chats[st.session_state.username].append(
        {"role": "user", "content": user_input, "time": str(datetime.now())}
    )

    # --- Lock 3: Send to n8n and handle errors ---
    try:
        with st.spinner("AI is thinking..."):
            response = requests.post(
                webhook_url,
                json={"chatInput": user_input},
                timeout=30
            )
            response.raise_for_status()  # Raises HTTPError for bad status codes

        # Parse AI response from n8n
        text = response.text
        reply = ""
        parts = text.split("}")
        for p in parts:
            if '"content":"' in p:
                try:
                    content = p.split('"content":"')[1].split('"')[0]
                    reply += content
                except:
                    pass

        if reply == "":
            reply = "⚠️ Sorry, the AI workflow returned an empty response."

    except requests.exceptions.Timeout:
        reply = "❌ Error: Request timed out. Check your n8n workflow."
    except requests.exceptions.ConnectionError:
        reply = "❌ Error: Could not connect to n8n. Check your webhook URL and internet."
    except requests.exceptions.HTTPError as e:
        reply = f"❌ Error: HTTP error {e.response.status_code}."
    except Exception as e:
        reply = f"❌ Unexpected error: {e}"

    # Show AI message
    st.chat_message("assistant").write(reply)
    st.session_state.chats[st.session_state.username].append(
        {"role": "assistant", "content": reply, "time": str(datetime.now())}
    )
