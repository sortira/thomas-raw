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
    input_variables=["destination", "days", "min_budget", "max_budget", "currency", "activities"],
    template="""
You are a travel budgeting assistant. DO NOT USE LATEX ANYWHERE JUST USE MARKDOWN.

Plan a travel budget for a trip to {destination} for {days} days.
The user has a budget between {min_budget} and {max_budget} {currency}.
Activities planned: {activities}.

Keep the response brief apart from the table, there should not be more than 150 words.

Output a table with the following format:

| Category   | Estimated Cost ({currency}) |
|------------|-----------------------------|
| Flights    | ...                         |
| Accommodation | ...                      |
| Food       | ...                         |
| Activities | ...                         |
| Transport  | ...                         |
| Misc       | ...                         |
| **Total**  | **...**                     |
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

# --- Currency Dropdown Options ---
CURRENCY_OPTIONS = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "INR": "Indian Rupee",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "CNY": "Chinese Yuan",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "SGD": "Singapore Dollar",
    "ZAR": "South African Rand",
    "BRL": "Brazilian Real",
    "KRW": "South Korean Won",
    "CHF": "Swiss Franc",
    "AED": "UAE Dirham",
    "MXN": "Mexican Peso",
    "THB": "Thai Baht",
    "MYR": "Malaysian Ringgit",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar"
}

# --- UI ---
st.title("💰 Budget Builder")
st.markdown("Cash tight? Just let us know your destination, intentions, and duration of stay, and we will let you know what options are available within your limits!")

destination = st.text_input("Destination (if multiple, separate them by commas)", "Bali")
days = st.slider("Trip Duration (days)", 1, 30, 7)

col1, col2 = st.columns(2)
with col1:
    min_budget = st.number_input("Minimum Budget", min_value=0, value=500)
with col2:
    max_budget = st.number_input("Maximum Budget", min_value=0, value=1500)

currency_code = st.selectbox(
    "Select Your Currency",
    options=list(CURRENCY_OPTIONS.keys()),
    format_func=lambda code: f"{code} - {CURRENCY_OPTIONS[code]}"
)

activities = st.multiselect(
    "Planned Activities",
    ["Sightseeing", "Adventure Sports", "Food Tours", "Shopping", "Cultural Tours", "Relaxation"],
    default=["Sightseeing"]
)

if st.button("Generate Budget"):
    if min_budget > max_budget:
        st.error("Minimum budget cannot be greater than maximum budget.")
    else:
        with st.spinner("Crunching numbers..."):
            response = chain.run({
                "destination": destination,
                "days": days,
                "min_budget": min_budget,
                "max_budget": max_budget,
                "currency": currency_code,
                "activities": ", ".join(activities)
            })
            st.session_state["budget_response"] = response

        st.markdown("### 🧾 Estimated Budget")
        st.markdown(response, unsafe_allow_html=True)
