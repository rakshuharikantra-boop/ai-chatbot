import streamlit as st
import requests

st.title("AI Chatbot 🤖")

webhook_url = "https://rakshitaharikantra.app.n8n.cloud/webhook/7917e788-e022-44bc-8628-ba73e4212949/chat"

# security check (lock)
if webhook_url == "PASTE_YOUR_N8N_WEBHOOK_URL_HERE":
    st.error("Webhook URL is not configured.")
    st.stop()

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask something")

if user_input:

    if user_input.strip() == "":
        st.warning("Please enter a valid message.")
        st.stop()

    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
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

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
