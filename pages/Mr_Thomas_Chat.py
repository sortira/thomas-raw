import streamlit as st
import argparse
import sys
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Mr. Thomas - Thomas Raw", page_icon="💬")

# --- CLI Mode Toggle ---
@st.cache_resource
def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["dev"], help="Run mode: 'dev' or leave empty for 'prod'")
    args, _ = parser.parse_known_args(sys.argv[1:])
    return "dev" if args.mode == "dev" else "prod"

# --- Load Key ---
def get_api_key(mode):
    if mode == "dev":
        with open("secret", "r") as f:
            return f.read().strip()
    else:
        return st.secrets["API_KEY"]

mode = get_mode()
api_key = get_api_key(mode)

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.7
)

# --- Prompt Template ---
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a professional travel planner AI. Based on the user's request, respond with a detailed itinerary, travel tips, and estimated cost. Always be friendly and informative.

User request: {user_input}

Structure your response like this:
- **Destination Overview**
- **Best Time to Visit**
- **Day-by-Day Itinerary**
- **Budget Estimate**
- **Travel Tips**

Make sure it's clear, practical, within 250 words and sounds like a helpful travel agent.

DO NOT USE LATEX IN YOUR RESPONSE. ONLY USE MARKDOWN.
"""
)

# --- Chain with Memory ---
memory = ConversationBufferMemory(return_messages=True)
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# --- Chat Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- UI ---
st.title("Thomas Raw: Your Agentic AI Travel Planner")
st.markdown("Your personal assistant, talk all about travel plans and he has you covered for everything. Get all your doubts clarified here!")

# Display full chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat input (bottom box)
user_input = st.chat_input("Ask me about your next trip...")

if user_input:
    # Append user message to chat
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Planning your trip..."):
        response = chain.run(user_input=user_input)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))

    # Append bot response
    st.session_state.chat_history.append(("assistant", response))
    with st.chat_message("assistant"):
        st.markdown(response)
