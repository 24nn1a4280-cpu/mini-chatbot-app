import streamlit as st
from openai import OpenAI

# =====================================
# Page Configuration
st.set_page_config(
    page_title="Mini ChatGPT - Mistral",
    page_icon="🦚",
    layout="centered"
)

st.title("🦚 Mini ChatGPT (Mistral AI)")

# =====================================
# API Key Input
api_key = st.text_input(
    "Enter your Mistral API Key",
    type="password"
)

# =====================================
# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# =====================================
# Display Previous Messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# =====================================
# Chat Input
prompt = st.chat_input("Type your message...")

if prompt:
    if not api_key:
        st.error("Please enter your Mistral API Key.")
        st.stop()

    # Create Mistral Client
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.mistral.ai/v1"
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="mistral-small-latest",
                messages=st.session_state.messages
            )

            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

    # Save AI Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

# =====================================
# Sidebar
with st.sidebar:
    st.header("Options")

    if st.button(" Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]
        st.rerun()

    st.markdown("---")
    st.write("**Model:** mistral-small-latest")
    st.write("**Framework:** Streamlit")
    st.write("**API:** Mistral AI")