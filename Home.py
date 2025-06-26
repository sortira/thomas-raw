import streamlit as st

st.set_page_config(page_title="Thomas Raw - AI Travel Planner", page_icon="🌍")

st.title("🌍 Thomas Raw: Your AI Travel Planner")
st.markdown("""
Welcome to **Thomas Raw**, your smart travel assistant built with Google Gemini and Langchain.
The inspiration behind the name is after the world-famous travel agency Thomas Cook. 

Use the sidebar to access different tools:
- 💬 Mr. Thomas Chats : Your personal assistant, talk all about travel plans and he has you covered for everything. Get all your doubts clarified here!
- 💰 Budget Buddy : Cash tight? Just let us know your destination, intentions, and duration of stay, and we will let you know what options are available within your limits! 
- 🗺️ Where Is It? (Photo Spot Detector) : See a lovely pic but can't ask where the place is? Fear not, just upload the photo, we'll ID it and give you a sample itinerary for the same!
- 📦 Insight Centre (Export your trip plan) : Once you're done with planning, come to Insight Centre and export it for future reference!

Everything you generate — budget, chats, photos — will be saved while you're using the app.
            
More features to be added soon, stay tuned!
""")

st.info("To begin, choose a tool from the sidebar.")
