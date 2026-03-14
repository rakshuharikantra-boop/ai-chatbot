import streamlit as st
import requests
import json

st.title("AI Chatbot 🤖")

webhook_url = "PASTE_YOUR_N8N_WEBHOOK_URL_HERE"

# --- Store chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: New Chat button ---
st.sidebar.title("Chat Controls")
if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []

# --- File/photo upload ---
uploaded_file = st.file_uploader(
    "Upload image or file (optional)", 
    type=["png", "jpg", "jpeg", "pdf", "txt"]
)
if uploaded_file:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# --- Show previous chat ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Ask something")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send input to n8n webhook
    response = requests.post(
        webhook_url,
        json={"chatInput": user_input}
    )

    text = response.text
    reply = ""

    # Extract words from n8n stream response
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

    # Show AI message
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
