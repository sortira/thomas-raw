import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import argparse 
import sys

st.set_page_config(page_title="Budget Buddy - Thomas Raw", page_icon="💰")

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

# --- Gemini LLM Setup ---
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.5
)

# --- Prompt Template ---
prompt = PromptTemplate(
    input_variables=["destination", "days", "style", "activities"],
    template="""
You are a travel budgeting assistant. DO NOT USE LATEX ANYWHERE JUST USE MARKDOWN.

Plan a travel budget for a trip to {destination} for {days} days.
The user prefers a {style} travel experience.
Activities planned: {activities}.

Keep the response brief apart from the table, there should not be more than 150 words.

Output a table with the following format:

| Category   | Estimated Cost (USD) |
|------------|----------------------|
| Flights    | $...                 |
| Accommodation | $...              |
| Food       | $...                 |
| Activities | $...                 |
| Transport  | $...                 |
| Misc       | $...                 |
| **Total**  | **$...**             |
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

# --- UI ---
st.title("💰 Budget Builder")
st.markdown("Cash tight? Just let us know your destination, intentions, and duration of stay, and we will let you know what options are available within your limits!")

destination = st.text_input("Destination (if multiple, separate them by commas)", "Bali")
days = st.slider("Trip Duration (days)", 1, 30, 7)
style = st.selectbox("Travel Style", ["Budget", "Mid-range", "Luxury"])
activities = st.multiselect(
    "Planned Activities",
    ["Sightseeing", "Adventure Sports", "Food Tours", "Shopping", "Cultural Tours", "Relaxation"],
    default=["Sightseeing"]
)

if st.button("Generate Budget"):
    with st.spinner("Crunching numbers..."):
        response = chain.run({
            "destination": destination,
            "days": days,
            "style": style,
            "activities": ", ".join(activities)
        })
        st.session_state["budget_response"] = response
    st.markdown("### 🧾 Estimated Budget")
    st.markdown(response, unsafe_allow_html=True)
