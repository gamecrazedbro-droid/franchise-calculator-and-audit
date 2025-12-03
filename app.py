import streamlit as st
import google.generativeai as genai
import os

st.title("🔌 Connection Test")

# 1. SETUP API KEY (From Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key Found")
except Exception as e:
    st.error(f"❌ API Key Error: {e}")
    st.stop()

# 2. VERIFY MODELS (The Debugger)
# This will ask Google "What models are available to me?" and print them.
# If this list is empty, your API Key is the problem.
st.subheader("Available Models:")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
    st.write(available_models)
except Exception as e:
    st.error(f"❌ Connection Error: {e}")

# 3. RUN THE TEST (Official Quickstart Code)
st.subheader("Test Generation")
if st.button("Run Test"):
    try:
        # Using the model exactly as listed in the docs
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content("Explain how AI works in one sentence.")
        st.info(response.text)
    except Exception as e:
        st.error(f"❌ Model Error: {e}")
