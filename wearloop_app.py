import streamlit as st
import pandas as pd
import random
import time

# --- App Configuration ---
st.set_page_config(page_title="WearLoop AI", page_icon="♻️", layout="centered")

# --- State Initialization ---
if 'wardrobe' not in st.session_state: st.session_state.wardrobe = []
if 'credits' not in st.session_state: st.session_state.credits = 0
if 'total_water_saved' not in st.session_state: st.session_state.total_water_saved = 0
if 'scanned_items' not in st.session_state: st.session_state.scanned_items = []

# --- AI Classification Engine ---
def analyze_garment(image):
    genders = ["Mens", "Womens", "Unisex"]
    types = ["T-Shirt", "Jeans", "Hoodie", "Dress", "Blouse", "Jacket"]
    fits = ["Slim Fit", "Oversized", "Regular Fit"]
    time.sleep(2)  # Simulate AI analysis
    return {
        "gender": random.choice(genders),
        "type": random.choice(types),
        "fit": random.choice(fits),
        "confidence": random.randint(92, 99)
    }

# --- Navigation ---
page = st.sidebar.radio("Navigate", ["Home", "Smart Add 📸", "Your Wardrobe 👕", "Concierge Swap 🚚", "Rewards Center 🎁"])

# --- HOME ---
if page == "Home":
    st.title("WearLoop Concierge 🌿")
    c1, c2 = st.columns(2)
    c1.metric("Water Saved", f"{st.session_state.total_water_saved} L")
    c2.metric("Wear Credits", f"{st.session_state.credits} 🪙")
    st.info("Scan items to earn credits and join the circular fashion movement.")

# --- SMART ADD ---
elif page == "Smart Add 📸":
    st.title("AI Wardrobe Scanner")
    img_file = st.camera_input("Scan Garment")

    if img_file:
        with st.status("Analyzing garment silhouette...", expanded=True) as status:
            prediction = analyze_garment(img_file)
            proposed_name = f"{prediction['gender']} {prediction['fit']} {prediction['type']}"
            st.write(f"📊 Confidence: **{prediction['confidence']}%**")
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        if proposed_name in st.session_state.scanned_items:
            st.warning(f"⚠️ '{proposed_name}' is already in your wardrobe!")
        else:
            with st.form("add_form"):
                st.subheader("Edit Details (Correct if AI was wrong)")
                name = st.text_input("Item Name:", value=proposed_name)
                cat = st.selectbox("Category:", ["Top", "Bottom", "Outerwear", "Shoes", "Accessory"])
                
                if st.form_submit_button("Add to Wardrobe"):
                    st.session_state.wardrobe.append({"name": name, "category": cat})
                    st.session_state.scanned_items.append(name)
                    st.session_state.credits += 50
                    st.balloons()
                    st.success(f"{name} added! +50 Credits.")
                    st.rerun()

# --- WARDROBE ---
elif page == "Your Wardrobe 👕":
    st.title("Your Wardrobe")
    if not st.session_state.wardrobe:
        st.warning("Your wardrobe is empty. Use **Smart Add** to digitize!")
    else:
        st.dataframe(pd.DataFrame(st.session_state.wardrobe), use_container_width=True)

# --- CONCIERGE SWAP ---
elif page == "Concierge Swap 🚚":
    st.title("Concierge Swap")
    if not st.session_state.wardrobe:
        st.error("Add items to your wardrobe first!")
    else:
        my_item = st.selectbox("Select item to swap:", [i['name'] for i in st.session_state.wardrobe])
        if st.button("Request Pickup", type="primary"):
            st.session_state.wardrobe = [i for i in st.session_state.wardrobe if i['name'] != my_item]
            st.session_state.credits += 50
            st.success("Pickup scheduled! Team arriving in 2-hour window.")
            st.map(pd.DataFrame({'lat': [25.1972], 'lon': [55.2744]}))

# --- REWARDS ---
elif page == "Rewards Center 🎁":
    st.title("Rewards Center")
    st.write(f"Balance: {st.session_state.credits} Credits")
    rewards = {"Ghaf Tree Planting": 250, "Eco-Tote Bag": 100}
    for item, cost in rewards.items():
        if st.button(f"Redeem {item} ({cost} 🪙)"):
            if st.session_state.credits >= cost:
                st.session_state.credits -= cost
                st.success(f"Claimed {item}!")
                st.rerun()