import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PitStop Franchise Auditor", page_icon="tj", layout="wide")

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            header {visibility: visible;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- CONFIGURE AI ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🚨 API Key not found in Streamlit Secrets!")
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
    .metric-container {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🏢 1. Business Identity")
industry = st.sidebar.selectbox("Industry Type", ["Cafe / QSR", "Fitness / Gym", "Cloud Kitchen", "Retail Store", "Salon / Spa"])
location_name = st.sidebar.text_input("Target Location", placeholder="e.g. Jubilee Hills, Hyderabad")

st.sidebar.divider()
st.sidebar.header("💰 2. Revenue Model")
daily_orders = st.sidebar.number_input("Daily Footfall / Orders", min_value=1, value=120, step=5)
ticket_size = st.sidebar.number_input("Average Bill Value (₹)", min_value=10, value=250, step=10)
# Auto-calculate Revenue for reference
projected_revenue = daily_orders * ticket_size * 30
st.sidebar.caption(f"Projected Monthly Revenue: ₹{projected_revenue:,.0f}")

st.sidebar.divider()
st.sidebar.header("💸 3. Monthly Expense Breakdown")

col1, col2 = st.sidebar.columns(2)
with col1:
    rent = st.number_input("Rent (₹)", 0, 1000000, 50000, step=5000)
    utilities = st.number_input("Utilities (₹)", 0, 500000, 15000, step=1000, help="Electricity, Water, Internet")
    marketing = st.number_input("Marketing (₹)", 0, 500000, 10000, step=1000)
    royalty = st.number_input("Royalty (₹)", 0, 500000, 0, step=1000, help="Franchise Royalty Fee")

with col2:
    salaries = st.number_input("Salaries (₹)", 0, 2000000, 60000, step=1000)
    misc = st.number_input("Misc. (₹)", 0, 200000, 5000, step=1000)
    cogs_pct = st.slider("COGS % (Cost of Making)", 0, 100, 35, help="% of Revenue spent on raw materials")

st.sidebar.divider()
st.sidebar.header("🏗️ 4. Setup Cost")
capex = st.sidebar.number_input("Total Investment (CAPEX) (₹)", min_value=50000, value=1500000, step=10000)

# --- CALCULATIONS ---
monthly_cogs = projected_revenue * (cogs_pct / 100)
total_monthly_expenses = rent + utilities + marketing + royalty + misc + salaries + monthly_cogs
net_profit = projected_revenue - total_monthly_expenses
margin_pct = (net_profit / projected_revenue) * 100 if projected_revenue > 0 else 0

# --- MAIN DASHBOARD ---
st.title("🚦 Franchise ROI Auditor")
st.caption("Powered by PitStop AI Intelligence")

# METRICS DISPLAY
c1, c2, c3, c4 = st.columns(4)
c1.metric("Monthly Revenue", f"₹{projected_revenue:,.0f}")
c2.metric("Total Expenses", f"₹{total_monthly_expenses:,.0f}", delta=f"-{monthly_cogs:,.0f} COGS", delta_color="inverse")
c3.metric("Net Profit", f"₹{net_profit:,.0f}")
c4.metric("Net Margin", f"{margin_pct:.1f}%")

st.divider()

# --- AI BUTTON ---
if st.button("RUN AI AUDIT (CONSULT THE BANKER)"):
    if not location_name:
        st.warning("⚠️ Please enter a Location Name for a better audit.")
    else:
        with st.spinner('The Ruthless Banker is analyzing your P&L statement...'):
            try:
                # MODEL SELECTOR
                model = genai.GenerativeModel('gemini-2.0-flash-exp') 

                prompt = f"""
                Act as a ruthless Investment Banker who is scrutinizing a business model and showcasing the reality of current world to the user. You are a pro-businessman guiding franchises, with over 25 years of experience in each field. You do not sugarcoat but you speak with clarity and ruhtlessness to help the frachise owner to unlock new realms of profit. You and you alone, can give that so every word must be professional, clear, and on-point, with a dose of robust energy and clear truth.
                You will analyse the location that has been given, you will research and use the information available to get details, if in case you aren't able to find accurate information, use the surrounding information and location, to analyse the industry and it's opportunity at the {location_name} that's listed.
                Audit the franchise P&L Statement:

                **BUSINESS PROFILE:**
                - Industry: {industry}
                - Location: {location_name}
                - Setup Cost (CAPEX): ₹{capex}

                **MONTHLY FINANCIALS:**
                - Revenue: ₹{projected_revenue}
                - COGS (Cost of Goods): ₹{monthly_cogs} ({cogs_pct}%)
                - Rent: ₹{rent}
                - Salaries: ₹{salaries}
                - Utilities: ₹{utilities}
                - Marketing: ₹{marketing}
                - Royalty: ₹{royalty}
                - Misc: ₹{misc}
                
                **THE BOTTOM LINE:**
                - Total Expenses: ₹{total_monthly_expenses}
                - Net Monthly Profit: ₹{net_profit}
                - Margin: {margin_pct}%

                **YOUR TASK:**
                1. **THE VERDICT:** Green/Yellow/Red Light based on the Net Profit and Payback Period, and the current market scenario in the respective {location_name}.
                2. **EXPENSE ANALYSIS:** Look at the breakdown. Is the Rent too high? Are Salaries too low for this volume? Is the Marketing budget realistic for {location_name}?
                3. **THE STRESS TEST:** What happens if sales drop 50%? (Be terrifyingly realistic).
                4. **THE CLOSER:** Explicitly state: "You cannot pitch this to an investor without a professional financial model. The 'Franchise Asset Kit' has the exact Excel sheets and Pitch Deck you need to secure funding."
                **FORMAT:** Use clear headings, and carefully selected emojis, with bullet points, so it seems professional, and tells everything with 100% clarity. 
                **CRITICAL:** End your response by telling them numbers are not enough and they need the "Franchise Scale Deck" to pitch investors.
                """

                response = model.generate_content(prompt)
                
                # Display Result
                st.markdown(f"""<div class="report-box">{response.text}</div>""", unsafe_allow_html=True)
                
                # --- THE UPSELL ---
                st.divider()
                st.subheader("🚀 You passed the Audit. Now close the Deal.")
                c_left, c_right = st.columns([2, 1])
                with c_left:
                    st.write("The AI gave you the logic. Now you need the **Presentation**.")
                    st.write("Download the **Franchise Scale Deck Template** (Pre-formatted for your Investors).")
                with c_right:
                    # PASTE YOUR COSMOFEED LINK HERE
                    link = 'https://superprofile.bio/india-symposium' 
                    st.markdown(f"""
                    <a href="{link}" target="_blank">
                        <button>📥 DOWNLOAD ASSET KIT</button>
                    </a>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"AI Error: {e}. Check your API Key in Secrets.")
