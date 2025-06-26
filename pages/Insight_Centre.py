import streamlit as st

st.set_page_config(page_title="Trip Exporter", page_icon="📦")
st.title("📦 Insight Centre - Thomas Raw")
st.markdown("Once you're done with planning, Insight Centre is where you export it for future reference!")

# --- Gather data ---
chat = st.session_state.get("chat_history", [])
budget = st.session_state.get("budget_response", "")
itinerary = st.session_state.get("itinerary_response", "")

st.markdown("Select what you want to export:")

include_chat = st.checkbox("Include Chat Conversation", True)
include_budget = st.checkbox("Include Budget", True)
filename = st.text_input("Filename", value="my_trip_plan")

# --- Build content ---
content = "# Travel Summary\n\n"

if include_chat and chat:
    content += "## Chat Conversation\n"
    for role, msg in chat:
        content += f"**{role.title()}**: {msg}\n\n"

if include_budget and budget:
    content += "## Budget Estimate\n" + budget + "\n\n"

st.download_button("⬇️ Download Insights", content, file_name=f"{filename}.txt", mime="text/plain")


