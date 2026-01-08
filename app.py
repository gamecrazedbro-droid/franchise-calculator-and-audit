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
industry = st.sidebar.selectbox("Industry Type", ["Cafe / QSR", "Retail Store", "Salon / Spa"])
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
# --- MOBILE GUIDE (The Fix) ---
with st.expander("📱 ON MOBILE? CLICK HERE FIRST", expanded=True):
    st.info("👈 **Tap the '>' Arrow** in the top-left corner to enter your Rent & Business Details.")
    st.write("*(On Desktop, the menu is already open on the left)*")

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

# --- 1. HARDCODED MARKET INTELLIGENCE (The "Brain") ---
                market_data = """
                HYDERABAD MARKET BENCHMARKS (2025):
                [Zone A: Jubilee Hills, Banjara Hills, Hitech City]
                - Danger Rent: > ₹120/sqft
                - Survival Daily Orders: Must exceed 100/day
                - Safe Rent-to-Revenue Ratio: Max 18%

                [Zone B: Gachibowli, Madhapur, Kondapur]
                - Danger Rent: > ₹90/sqft
                - Survival Daily Orders: Must exceed 120/day (Volume Game)
                - Safe Rent-to-Revenue Ratio: Max 20%

                [Zone C: Kompally, AS Rao Nagar, Dilsukhnagar, Secunderabad]
                - Danger Rent: > ₹60/sqft
                - Safe Rent-to-Revenue Ratio: Max 15% (Lower spending power)

                CRITICAL FINANCIAL RULES:
                1. RENT TRAP: If Rent > 20% of Revenue -> IMMEDIATE RED LIGHT.
                2. SALARY BLEED: Staff costs > 25% of Revenue -> HIGH RISK.
                3. MARKETING VOID: If Marketing Budget < 3% of Revenue -> INVISIBLE BUSINESS.
                """

                # --- 2. THE FORENSIC PROMPT ---
                prompt = f"""
                You are a ruthless Investment Banker & Forensic Auditor for the Hyderabad market.
                Your job is NOT to be nice. Your job is to prevent bankruptcy.
                
                CONTEXT DATA:
                {market_data}

                USER'S P&L DATA:
                - Business: {industry} in {location_name}
                - Revenue: ₹{projected_revenue} (Driven by {daily_orders} daily orders at ₹{ticket_size} ATS)
                - Rent: ₹{rent} ({round((rent/projected_revenue)*100, 1)}% of Revenue)
                - Staff: ₹{salaries} ({round((salaries/projected_revenue)*100, 1)}% of Revenue)
                - Marketing: ₹{marketing}
                - Net Profit: ₹{net_profit} ({margin_pct}%)

                INSTRUCTIONS:
                1. **THE AUDIT:** Compare their Rent% and Staff% against the "HYDERABAD MARKET BENCHMARKS". 
                   - If Rent > 20% of Revenue, declare it a "RENT TRAP".
                   - If Net Profit is < 15%, declare it "UNINVESTABLE".
                
                2. **THE REALITY CHECK (The "Killer" Insight):**
                   - Calculate specific numbers. E.g., "You are paying Jubilee Hills rent but charging Kompally prices." 
                   - "To afford this rent, you don't need {daily_orders} orders. You need [Calculate: Total Expenses / (Ticket Size * 0.7)] orders/day."

                3. **THE STRESS TEST:** - "If Swiggy/Zomato take their 24% commission on half your orders, your profit drops to ₹[Estimate]." 
                
                4. **THE VERDICT:** - Start with: **🚦 VERDICT: [RED / YELLOW / GREEN] LIGHT**
                   - Follow with a 3-bullet summary of *exactly* why.

                5. **THE CLOSING HOOK (Crucial):**
                   - If RED/YELLOW: "You cannot open this. The math is broken. You need to restructure your Unit Economics using the Scenario Builder in the Asset Kit."
                   - If GREEN: "The numbers look good, but a text summary won't get you funding. Investors need the 18-Month Financial Model and Pitch Deck to sign the check."
                   - **Boldly state:** "Download the **Franchise Asset Kit** below to professionalize this plan."
                
                TONE: Short, punchy, numerical, and authoritative. Use formatting (Bold/Tables) to make it readable.
                
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
                    link = 'https://superprofile.bio/vp/the-franchise-asset-kit' 
                    st.markdown(f"""
                    <a href="{link}" target="_blank">
                        <button>📥 DOWNLOAD ASSET KIT</button>
                    </a>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"AI Error: {e}. Check your API Key in Secrets.")
