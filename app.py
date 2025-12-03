import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PitStop Franchise Auditor", page_icon="🚦", layout="wide")

# --- CONFIGURE AI ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🚨 API Key not found in Secrets!")
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #C5A059;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    .report-box {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-top: 20px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🏢 Franchise Parameters")
industry = st.sidebar.selectbox("Industry Type", ["Cafe / QSR", "Fitness / Gym", "Cloud Kitchen", "Retail Store", "Salon / Spa"])
location = st.sidebar.text_input("City / Location", "Hyderabad")

st.sidebar.divider()
st.sidebar.subheader("💰 The Money")
capex = st.sidebar.number_input("Total Setup Cost (₹)", 100000, 5000000, 1500000, step=50000)
rent = st.sidebar.number_input("Monthly Rent (₹)", 0, 500000, 50000, step=5000)
revenue = st.sidebar.number_input("Est. Monthly Revenue (₹)", 0, 5000000, 300000, step=10000)

# --- MAIN DASHBOARD ---
st.title("🚦 Franchise ROI Auditor")
st.caption("Running on Gemini 2.0 Flash (Experimental)")

# --- AI BUTTON ---
if st.button("RUN AI AUDIT (CONSULT THE BANKER)"):
    with st.spinner('Gemini 2.0 is crunching the numbers...'):
        try:
            model = genai.GenerativeModel('gemini-3.0-pro') 
# ^ REPLACE 'gemini-3.0-pro' WITH THE EXACT ID FROM AI STUDIO
            prompt = f"""
            Act as a ruthless Investment Banker. Audit this franchise plan:
            - Business: {industry} in {location}
            - Setup Cost: ₹{capex}
            - Rent: ₹{rent}
            - Revenue: ₹{revenue}

            Task:
            1. Give a Red/Yellow/Green light verdict based on ROI.
            2. Roast the Rent-to-Revenue ratio if it's over 15%.
            3. Write a 2-sentence "Investment Thesis" for a corporate investor.
            
            Format nicely with emojis. End by suggesting they download the "Franchise Scale Deck" for the full financial model.
            """
            
            response = model.generate_content(prompt)
            st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
            
            # THE UPSELL
            st.divider()
            st.write("Need to pitch this? Get the Asset Kit:")
            # PASTE YOUR COSMOFEED LINK BELOW
            st.link_button("📥 DOWNLOAD ASSET KIT", "https://cosmofeed.com/vp/YOUR_LINK_HERE")

        except Exception as e:
            st.error(f"AI Connection Error: {e}")
            st.info("Tip: If 2.0 fails, your API Key might not have access yet. Check AI Studio.")
