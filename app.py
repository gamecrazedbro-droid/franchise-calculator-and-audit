import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PitStop Franchise Auditor", page_icon="🚦", layout="wide")

# --- CUSTOM CSS FOR BRANDING ---
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
    .verdict-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2666/2666505.png", width=50)
st.sidebar.header("🏢 Audit Parameters")

industry = st.sidebar.selectbox(
    "Select Industry Type",
    ("Cafe / QSR", "Fitness / Gym", "Cloud Kitchen", "Retail Store", "Salon / Spa")
)

st.sidebar.divider()
st.sidebar.subheader("💰 Financial Inputs")
capex = st.sidebar.number_input("Total Setup Cost (₹)", min_value=50000, value=1500000, step=50000)
rent = st.sidebar.number_input("Monthly Rent (₹)", min_value=0, value=50000, step=5000)
daily_orders = st.sidebar.number_input("Daily Footfall / Orders", min_value=1, value=80, step=5)
ticket_size = st.sidebar.number_input("Average Bill Value (₹)", min_value=10, value=200, step=10)

# --- LOGIC ENGINE ---
revenue = daily_orders * ticket_size * 30

# Industry Specific Logic
if industry == "Cafe / QSR":
    cogs_pct = 0.35
    commission_pct = 0.0
    staff_cost_base = 40000
    industry_risk = "High Food Waste & Location Dependency"
elif industry == "Cloud Kitchen":
    cogs_pct = 0.35
    commission_pct = 0.30 
    staff_cost_base = 30000
    industry_risk = "Aggregator Commissions (30%) Eating Margins"
elif industry == "Fitness / Gym":
    cogs_pct = 0.05 
    commission_pct = 0.0
    staff_cost_base = 25000
    industry_risk = "Member Retention & High Churn Rates"
elif industry == "Retail Store":
    cogs_pct = 0.65 
    commission_pct = 0.0
    staff_cost_base = 20000
    industry_risk = "Dead Stock Inventory"
else: # Salon
    cogs_pct = 0.15
    commission_pct = 0.0
    staff_cost_base = revenue * 0.40 
    industry_risk = "Staff Poaching Clients"

# Dynamic Staff Cost Scaling
staff_cost = staff_cost_base * 1.5 if revenue > 500000 else staff_cost_base

# Calculations
variable_costs = revenue * (cogs_pct + commission_pct)
gross_profit = revenue - variable_costs
utilities = 15000
marketing = revenue * 0.05 
fixed_costs = rent + staff_cost + utilities + marketing
net_profit = gross_profit - fixed_costs

# Payback Logic
payback_months = capex / net_profit if net_profit > 0 else 999

# --- MAIN DASHBOARD ---
st.title("🚦 Franchise ROI Auditor")
st.caption("Strategic Audit Tool by PitStop Studios")

st.info(f"**Auditing Sector:** {industry} | **Target Revenue:** ₹{revenue:,.0f} / month")

# METRICS GRID
c1, c2, c3 = st.columns(3)
c1.metric("Gross Profit", f"₹{gross_profit:,.0f}")
c2.metric("Net Monthly Profit", f"₹{net_profit:,.0f}")
profit_margin = (net_profit/revenue)*100 if revenue > 0 else 0
c3.metric("Net Margin", f"{profit_margin:.1f}%")

st.divider()

# VERDICT SECTION
if payback_months <= 18:
    verdict_color = "#d4edda"
    text_color = "#155724"
    verdict_text = f"🟢 GREEN LIGHT: {payback_months:.1f} Months Payback"
    advice = "This is an Investable Asset. The 'Jay' Investor would buy this."
elif payback_months <= 24:
    verdict_color = "#fff3cd"
    text_color = "#856404"
    verdict_text = f"🟡 YELLOW LIGHT: {payback_months:.1f} Months Payback"
    advice = "Operable, but risky. You need to lower Rent or increase Volume."
else:
    verdict_color = "#f8d7da"
    text_color = "#721c24"
    verdict_text = "🔴 RED LIGHT: Investment Risk High"
    advice = "Do not open this. You are buying a job, not a business."

st.markdown(f"""
    <div style="background-color: {verdict_color}; color: {text_color};" class="verdict-box">
        {verdict_text}
    </div>
    """, unsafe_allow_html=True)

st.write(f"**Consultant's Verdict:** {advice}")

# THE REALITY CHECK
with st.expander("🧐 See The Reality Check (Why this happens)", expanded=True):
    st.write(f"**Your Industry Trap:** {industry_risk}")
    
    if industry == "Cloud Kitchen":
        st.warning(f"⚠️ **Hidden Cost Alert:** We deducted 30% (₹{revenue*0.30:,.0f}) for Swiggy/Zomato commissions.")
    
    rent_ratio = rent/revenue if revenue > 0 else 0
    if rent_ratio > 0.20:
        st.error(f"⚠️ **Rent Trap:** Your rent is {rent_ratio:.0%} of sales. Safe limit is 15%.")

st.divider()

# THE UPSELL (MONETIZATION)
st.subheader("🚀 Make It Official")
c_left, c_right = st.columns([2, 1])

with c_left:
    st.write("Numbers are easy. Narratives sell. If you want to pitch this to investors, you need our **Corporate Franchise Deck**.")
    st.write("*Includes: Zero-Flame Safety Slides, Unit Economics Tables, and Investor Logic.*")

with c_right:
    # LINK TO YOUR COSMOFEED PRODUCT
    link = '[INSERT YOUR COSMOFEED LINK HERE]'
    st.markdown(f"""
    <a href="{link}" target="_blank">
        <button style="background-color:#C5A059; color:white; border:none; padding:15px 32px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin:4px 2px; cursor:pointer; width:100%; border-radius:10px;">
            📥 DOWNLOAD ASSET KIT
        </button>
    </a>
    """, unsafe_allow_html=True)
