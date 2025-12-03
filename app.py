import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PitStop Franchise Auditor", page_icon="🚦", layout="wide")

# --- CONFIGURE GEMINI AI ---
# This grabs the key from the "Secrets" vault we set up in Step 2
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("⚠️ API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #C5A059;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .report-box {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2666/2666505.png", width=50)
st.sidebar.header("🏢 1. Business Profile")

industry = st.sidebar.selectbox(
    "Industry Type",
    ("Cafe / QSR", "Fitness / Gym", "Cloud Kitchen", "Retail Store", "Salon / Spa")
)
location_name = st.sidebar.text_input("Location / City Area", placeholder="e.g. Gachibowli, Hyderabad")

st.sidebar.divider()
st.sidebar.header("💰 2. The Numbers")

capex = st.sidebar.number_input("Total Setup Cost (₹)", min_value=50000, value=1500000, step=50000)
rent = st.sidebar.number_input("Monthly Rent (₹)", min_value=0, value=50000, step=5000)
marketing_budget = st.sidebar.number_input("Marketing Budget (₹/mo)", value=10000, step=1000)
daily_orders = st.sidebar.number_input("Daily Footfall / Orders", min_value=1, value=80, step=5)
ticket_size = st.sidebar.number_input("Average Bill Value (₹)", min_value=10, value=200, step=10)

st.sidebar.divider()
st.sidebar.header("⚔️ 3. Market Context")
competitors = st.sidebar.slider("Competitors nearby (1km radius)", 0, 20, 5)

# --- MAIN DASHBOARD ---
st.title("🚦 AI Franchise Consultant")
st.caption("Powered by PitStop Studios Intelligence & Google Gemini")

# Calculate basic numbers for display
revenue = daily_orders * ticket_size * 30
profit_est = revenue * 0.20 # Rough estimate just for visuals

# Show Live Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Projected Monthly Sales", f"₹{revenue:,.0f}")
c2.metric("Rent to Sales Ratio", f"{(rent/revenue)*100:.1f}%")
c3.metric("Competition Level", f"{competitors} Rivals")

st.divider()

# --- THE AI BUTTON ---
if st.button("RUN AI AUDIT (CONSULT THE BANKER)"):
    if not location_name:
        st.warning("⚠️ Please enter a Location Name for a better audit.")
    else:
        with st.spinner('The Ruthless Banker is auditing your numbers...'):
            
            # THE PROMPT (The Brain)
            prompt = f"""
            You are the 'Ruthless Investment Banker' for PitStop Studios. 
            Audit this franchise business plan. Be critical, specific, and direct.

            **BUSINESS DATA:**
            - Industry: {industry}
            - Location: {location_name}
            - Setup Cost (CAPEX): ₹{capex}
            - Monthly Rent: ₹{rent}
            - Marketing Budget: ₹{marketing_budget}
            - Projected Monthly Revenue: ₹{revenue}
            - Competitors Nearby: {competitors}

            **YOUR TASK:**
            1. **THE VERDICT:** Green/Yellow/Red Light based on payback period and rent ratio.
            2. **REALITY CHECK:** Criticize their Marketing Budget vs Competitor count. Is the Rent too high for this location?
            3. **THE STRESS TEST:** What happens if sales drop 30%?
            4. **THE 'JAY' PITCH:** Write a 2-sentence investment thesis for a Corporate VP investor.

            **FORMAT:** Use clear headings, emojis, and bullet points. 
            **CRITICAL:** End your response by telling them that numbers are not enough, and they need the "Franchise Scale Deck" to pitch investors.
            """

            try:
                # Call Gemini
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                # Display Result
                st.markdown(f"""<div class="report-box">{response.text}</div>""", unsafe_allow_html=True)
                
                # --- THE UPSELL (Only shows after AI runs) ---
                st.divider()
                st.subheader("🚀 You passed the Audit. Now close the Deal.")
                c_left, c_right = st.columns([2, 1])
                with c_left:
                    st.write("The AI gave you the logic. Now you need the **Presentation**.")
                    st.write("Download the **Franchise Scale Deck Template** (Pre-formatted for 'Jay' Investors).")
                with c_right:
                    # LINK TO YOUR COSMOFEED PRODUCT
                    link = 'YOUR_COSMOFEED_LINK_HERE' 
                    st.markdown(f"""
                    <a href="{link}" target="_blank">
                        <button>📥 DOWNLOAD ASSET KIT</button>
                    </a>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"AI Error: {e}. Check your API Key in Secrets.")
