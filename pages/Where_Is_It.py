import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import argparse
import sys

st.set_page_config(page_title="Where Is It? - Thomas Raw", page_icon="🗺️")
st.title("🗺️ Where Is It?")
st.markdown("See a lovely pic but can't ask where the place is? Fear not, just upload the photo, we'll ID it and give you a sample itinerary for the same")


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

genai.configure(api_key=api_key)

# Use Gemini model with vision
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Image Upload ---
uploaded_file = st.file_uploader("Upload a travel photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Photo", use_column_width=True)
    st.info("This may take a few seconds...")

    with st.spinner("Analyzing your photo..."):
        # Convert to byte data for API
        byte_data = io.BytesIO()
        image.save(byte_data, format="PNG")
        byte_data = byte_data.getvalue()

        # Run Gemini Vision
        response = model.generate_content([
            "What famous landmark or tourist spot is shown in this image? Also suggest nearby attractions.",
            {
                "mime_type": "image/png",
                "data": byte_data
            }
        ])

        st.markdown("### 📍 Detected Spot & Suggestions")
        st.markdown(response.text)
