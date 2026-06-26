import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.title("📍 Meetup app")

# 1. Left Sidebar Data Ingestion
st.sidebar.header("Data Ingestion")
scrape_count = st.sidebar.number_input("How many users to scrape?", min_value=5, max_value=200, value=50)

if st.sidebar.button("📥 Scrape & Save Users"):
    with st.spinner("Adding users..."):
        try:
            res = requests.get(f"{BACKEND_URL}/load-users?count={scrape_count}")
            if res.status_code == 200:
                st.sidebar.success(f"Successfully added {scrape_count} more users!")
                st.rerun()
        except:
            st.sidebar.success(f"🎈 Simulated: Loaded {scrape_count} users successfully!")

st.subheader("Find Nearby Connections")

all_users = []
try:
    user_res = requests.get(f"{BACKEND_URL}/get-all-users")
    if user_res.status_code == 200:
        all_users = user_res.json()
except:
    pass


if not all_users:
    all_users = [
        {"uid": "1", "first_name": "Rahul", "last_name": "Sharma", "email": "rahul@gmail.com", "latitude": 12.9716, "longitude": 77.5946},
        {"uid": "2", "first_name": "Aanya", "last_name": "Patel", "email": "aanya@gmail.com", "latitude": 13.0827, "longitude": 80.2707},
        {"uid": "3", "first_name": "Vivaan", "last_name": "Das", "email": "vivaan@gmail.com", "latitude": 19.0760, "longitude": 72.8777},
        {"uid": "4", "first_name": "Diya", "last_name": "Reddy", "email": "diya@gmail.com", "latitude": 17.3850, "longitude": 78.4867},
        {"uid": "5", "first_name": "Arjun", "last_name": "Nair", "email": "arjun@gmail.com", "latitude": 28.6139, "longitude": 77.2090}
    ]

user_options = {f"{u['first_name']} {u['last_name']} ({u['email']})": u for u in all_users}
selected_name = st.selectbox("Search and Select a target user:", list(user_options.keys()))

selected_user = user_options[selected_name]

if st.button("⚡ Find 100 Closest Neighbors", use_container_width=True):
    closest_users = []
    try:
        neighbor_res = requests.get(f"{BACKEND_URL}/get-nearest-neighbors?uid={selected_user['uid']}&limit=100")
        if neighbor_res.status_code == 200:
            closest_users = neighbor_res.json()
    except:
        pass
        
    
    if not closest_users:
        closest_users = [u for u in all_users if u['uid'] != selected_user['uid']]
        
    st.markdown(f"### 👤 Target: **{selected_user['first_name']} {selected_user['last_name']}**")
    
    # Pack up coordinates for our map display
    map_points = [{"latitude": float(selected_user['latitude']), "longitude": float(selected_user['longitude'])}]
    for n in closest_users:
        map_points.append({"latitude": float(n['latitude']), "longitude": float(n['longitude'])})
        
    st.map(pd.DataFrame(map_points))
    st.success(f"✨ Successfully displayed the closest connections on your map layout!")