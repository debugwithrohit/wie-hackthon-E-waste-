import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page Configuration
st.set_page_config(
    page_title="SheCycle: E-Waste & Women SHG Hub",
    page_icon="♻️",
    layout="wide"
)

# Initialize Session State
if 'requests' not in st.session_state:
    st.session_state.requests = [
        {
            "id": "EW-1001",
            "citizen_name": "Rahul Sharma",
            "phone": "9876543210",
            "address": "Kankar Kheda, Meerut",
            "item_type": "Old Smartphone & Charger",
            "weight": "0.5 kg",
            "status": "Pending",
            "assigned_shg": "Unassigned",
            "date": "2026-11-06"
        },
        {
            "id": "EW-1002",
            "citizen_name": "Amit Kumar",
            "phone": "9123456789",
            "address": "Rohta Road, Meerut",
            "item_type": "Dead Laptop Motherboard",
            "weight": "2.0 kg",
            "status": "Collected",
            "assigned_shg": "Maa Durga Mahila SHG (DAY-NULM)",
            "date": "2026-11-05"
        }
    ]

if 'shg_partners' not in st.session_state:
    st.session_state.shg_partners = [
        {
            "shg_name": "Maa Durga Mahila SHG",
            "portal_type": "DAY-NULM (Urban)",
            "registration_id": "NULM-2024-88",
            "leader_name": "Sunita Devi",
            "phone": "9837000000",
            "area": "Kankar Kheda",
            "bank_ac": "********1234",
            "status": "Verified",
            "total_collected": 15,
            "earnings": "₹3,400"
        }
    ]

# --- MAIN APP TITLE ---
st.title("♻️ SheCycle: Women-Led Smart E-Waste Management & Recycling System")
st.caption("Connecting Citizens with Govt. Registered (DAY-NRLM / NULM) Women Self-Help Groups for Sustainable E-Waste Recycling")
st.markdown("---")

# Sidebar Navigation
role = st.sidebar.selectbox(
    "Select Your Portal / Role:",
    ["👤 Citizen Portal (E-Waste User)", "👩‍🦰 Women SHG Partner Portal", "🏛️ Admin / Municipal Dashboard"]
)

# Sidebar Info for Govt Portals
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Official Govt. Portals")
st.sidebar.markdown("- 🌾 [DAY-NRLM Portal (Rural)](https://aajeevika.gov.in/)")
st.sidebar.markdown("- 🏙️ [DAY-NULM Portal (Urban)](https://nulm.gov.in/)")

# ==========================================
# 1. CITIZEN PORTAL (E-Waste User)
# ==========================================
if role == "👤 Citizen Portal (E-Waste User)":
    st.header("Drop Your E-Waste Safely & Support Women Micro-Entrepreneurs")
    
    with st.form("ewaste_form"):
        col1, col2 = st.columns(2)
        with col1:
            c_name = st.text_input("Your Full Name")
            c_phone = st.text_input("Mobile Number")
        with col2:
            c_address = st.text_area("Complete Address (with Locality)")
            item_desc = st.selectbox("E-Waste Item Type", ["Old Smartphone / Mobile", "Laptop / Computer Parts", "Lithium-ion Batteries / Chargers", "Home Appliances (Iron, Toaster)", "Mixed E-Scrap"])
            estimated_weight = st.selectbox("Estimated Weight", ["Under 1 kg", "1 kg - 3 kg", "3 kg - 5 kg", "Above 5 kg"])
            
        submitted = st.form_submit_button("Submit Pickup Request")
        
        if submitted:
            if c_name and c_phone and c_address:
                new_id = f"EW-{random.randint(1003, 9999)}"
                new_req = {
                    "id": new_id,
                    "citizen_name": c_name,
                    "phone": c_phone,
                    "address": c_address,
                    "item_type": item_desc,
                    "weight": estimated_weight,
                    "status": "Pending",
                    "assigned_shg": "Unassigned",
                    "date": str(datetime.now().date())
                }
                st.session_state.requests.append(new_req)
                st.success(f"Success! Request ID **{new_id}** generated. Nearby verified Women SHG will pick it up soon.")
            else:
                st.error("Please fill in all required contact details.")

    st.markdown("### 📋 Track Your Request")
    check_phone = st.text_input("Enter your mobile number to view status:")
    if check_phone:
        filtered_reqs = [r for r in st.session_state.requests if r['phone'] == check_phone]
        if filtered_reqs:
            st.table(pd.DataFrame(filtered_reqs))
        else:
            st.info("No active requests found for this number.")

# ==========================================
# 2. WOMEN SHG PARTNER PORTAL
# ==========================================
elif role == "👩‍🦰 Women SHG Partner Portal":
    st.header("👩‍🦰 Women Self-Help Group (SHG) Micro-Entrepreneur Portal")
    
    tab1, tab2, tab3 = st.tabs(["📲 Live Pickup Requests", "📝 SHG Govt. Portal Onboarding", "💰 Earnings & Collection History"])
    
    with tab1:
        st.subheader("Available E-Waste Pickups")
        pending_reqs = [r for r in st.session_state.requests if r['status'] == 'Pending']
        
        if not pending_reqs:
            st.info("No pending requests currently.")
        else:
            for req in pending_reqs:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.write(f"**ID:** {req['id']}")
                        st.write(f"**Citizen:** {req['citizen_name']} ({req['phone']})")
                        st.write(f"**Address:** {req['address']}")
                    with c2:
                        st.write(f"**Item:** {req['item_type']}")
                        st.write(f"**Weight:** {req['weight']}")
                    with c3:
                        selected_shg = st.selectbox("Select Registered SHG", [s['shg_name'] for s in st.session_state.shg_partners], key=f"sel_{req['id']}")
                        if st.button("Accept & Pickup", key=f"btn_{req['id']}"):
                            req['status'] = "Collected"
                            req['assigned_shg'] = selected_shg
                            st.success(f"Request {req['id']} assigned to {selected_shg}!")
                            st.rerun()

    with tab2:
        st.subheader("Register SHG using Govt NRLM / NULM Credentials")
        st.info("Verify your group using official National Rural Livelihoods Mission (NRLM) or Urban Livelihoods Mission (NULM) IDs.")
        
        with st.form("shg_reg_form"):
            s_name = st.text_input("SHG Group Name")
            portal_choice = st.selectbox("Select Government Portal Registry", ["DAY-NULM (Urban / Shahari)", "DAY-NRLM (Rural / Dehati)"])
            s_reg = st.text_input("Enter Govt Registration ID (e.g., NULM-2024-99 or NRLM-8823)")
            s_leader = st.text_input("Group Leader Name")
            s_phone = st.text_input("Mobile Number (Aadhaar Linked)")
            s_area = st.text_input("Operating Locality / Ward Name")
            s_bank = st.text_input("SHG Bank Account Number")
            
            reg_submit = st.form_submit_button("Verify & Onboard SHG")
            if reg_submit:
                if s_name and s_reg and s_phone:
                    st.session_state.shg_partners.append({
                        "shg_name": s_name,
                        "portal_type": portal_choice,
                        "registration_id": s_reg,
                        "leader_name": s_leader,
                        "phone": s_phone,
                        "area": s_area,
                        "bank_ac": s_bank,
                        "status": "Verified Partner",
                        "total_collected": 0,
                        "earnings": "₹0"
                    })
                    st.success(f"🎉 Success! {s_name} registered under {portal_choice} as a Verified E-Waste Recycling Partner.")
                else:
                    st.error("Please fill in mandatory fields.")

    with tab3:
        st.subheader("Group Earnings & Account Summary")
        st.table(pd.DataFrame(st.session_state.shg_partners))

# ==========================================
# 3. ADMIN / MUNICIPAL DASHBOARD
# ==========================================
else:
    st.header("🏛️ Admin / Municipal Authority Oversight")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total E-Waste Requests", len(st.session_state.requests))
    col2.metric("Registered SHGs (NRLM/NULM)", len(st.session_state.shg_partners))
    col3.metric("Total Recycled Items", len([r for r in st.session_state.requests if r['status'] != 'Pending']))
    
    st.markdown("---")
    st.subheader("📊 Master Requests Log")
    st.dataframe(pd.DataFrame(st.session_state.requests), use_container_width=True)
    
    st.subheader("👩‍🦰 Onboarded SHGs & Verification Portal Directory")
    st.dataframe(pd.DataFrame(st.session_state.shg_partners), use_container_width=True)