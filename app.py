import streamlit as st
import requests
from datetime import datetime

# --- Page config ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("AI Chatbot 🤖")

# --- n8n webhook ---
webhook_url = "PASTE_YOUR_N8N_WEBHOOK_URL_HERE"

# --- Lock: Check webhook ---
if webhook_url == "https://rakshitaharikantra.app.n8n.cloud/webhook/7917e788-e022-44bc-8628-ba73e4212949/chat":
    st.error("Webhook URL is not configured.")
    st.stop()

# --- User login ---
if "username" not in st.session_state:
    st.session_state.username = ""
if st.session_state.username == "":
    st.session_state.username = st.text_input("Enter your name to login")
    if st.session_state.username == "":
        st.stop()

# --- Chat session state ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
if st.session_state.username not in st.session_state.chats:
    st.session_state.chats[st.session_state.username] = []

# --- Sidebar: New Chat button ---
st.sidebar.title("Chat Controls")
new_chat_clicked = st.sidebar.button("➕ New Chat")
if new_chat_clicked:
    st.session_state.chats[st.session_state.username] = []
    # We do NOT rerun immediately; Streamlit will automatically refresh the UI

# --- File upload ---
uploaded_file = st.file_uploader(
    "Upload image or file",
    type=["png","jpg","jpeg","pdf","txt"]
)
if uploaded_file:
    st.success("File uploaded successfully!")

# --- Display chat history ---
for msg in st.session_state.chats[st.session_state.username]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Ask something")
if user_input:
    if user_input.strip() == "":
        st.warning("Please enter a valid message.")
        st.stop()

    # Add user message
    st.chat_message("user").write(user_input)
    st.session_state.chats[st.session_state.username].append(
        {"role": "user", "content": user_input, "time": str(datetime.now())}
    )

    # Send to n8n
    try:
        with st.spinner("AI is thinking..."):
            response = requests.post(
                webhook_url,
                json={"chatInput": user_input},
                timeout=30
            )
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
            reply = "Sorry, I couldn't understand the response."
    except:
        reply = "Error connecting to AI workflow."

    # Add AI response
    st.chat_message("assistant").write(reply)
    st.session_state.chats[st.session_state.username].append(
        {"role": "assistant", "content": reply, "time": str(datetime.now())}
    )
