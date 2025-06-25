import streamlit as st
import argparse
import sys
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


st.set_page_config(page_title="Travel Planner with Gemini")

# --- Handle CLI args ---
@st.cache_resource
def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="dev", choices=["dev", "prod"], help="Run mode")
    
    # NOTE: Streamlit runs as `streamlit run script.py [args]`
    # So manually parse from sys.argv beyond Streamlit's args
    args, _ = parser.parse_known_args(sys.argv[1:])
    return args.mode

# --- Load API Key based on mode ---
def get_api_key(mode):
    if mode == "prod":
        if hasattr(st.secrets, "_file_path") and os.path.exists(st.secrets._file_path or ""):
            return st.secrets["API_KEY"]
        else:
            st.error("❌ Missing `.streamlit/secrets.toml` file in production mode!")
            st.stop()
    else:
        with open("secret", "r") as f:
            return f.read().strip()

# Get mode and key
mode = get_mode()
api_key = get_api_key(mode)

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash", 
    google_api_key=api_key,
    temperature=0.7
)

# --- Structured Prompt ---
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
"""
)

# Memory & Chain
memory = ConversationBufferMemory()
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# --- Streamlit UI ---
st.title("AI Travel Planner")
st.markdown("Plan your next vacation using Google Gemini and LangChain!")

user_input = st.text_input("Where do you want to go or what do you want help with?", "")

if user_input:
    with st.spinner("Planning your trip..."):
        response = chain.run(user_input=user_input)
    st.markdown("### ✈️ Suggested Plan")
    st.markdown(response, unsafe_allow_html=True)

with st.expander("🧠 Chat History"):
    st.write(memory.buffer)
