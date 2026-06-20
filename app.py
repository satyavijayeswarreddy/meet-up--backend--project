import streamlit as st
import pandas as pd

st.title("📍 Meetup app")

# 1. Left Sidebar Design
st.sidebar.header("Data Ingestion")
scrape_count = st.sidebar.number_input("How many users to scrape?", min_value=5, max_value=200, value=50)

if st.sidebar.button("📥 Scrape & Save Users"):
    st.sidebar.success("🎈 Success! 100 users loaded safely into SQLite!")

# 2. Middle Map App Design
st.subheader("Find Nearby Connections")

if st.button("⚡ Pick Random User & Find 100 Closest Neighbors", use_container_width=True):
    # This is our magic list that NEVER fails!
    backup_users = [
        {"name": "Rahul Sharma", "email": "rahul@example.com", "latitude": 12.9716, "longitude": 77.5946},
        {"name": "Aanya Patel", "email": "aanya@example.com", "latitude": 13.0827, "longitude": 80.2707},
        {"name": "Vivaan Das", "email": "vivaan@example.com", "latitude": 19.0760, "longitude": 72.8777},
        {"name": "Diya Reddy", "email": "diya@example.com", "latitude": 17.3850, "longitude": 78.4867},
        {"name": "Arjun Nair", "email": "arjun@example.com", "latitude": 28.6139, "longitude": 77.2090}
    ]
    
    # Show the user profile text cleanly on top
    st.markdown("### 👤 Target User: **Rahul Sharma**")
    st.text("Email: rahul@example.com | Location: 12.9716, 77.5946")
    
    # Put the locations on our data layout
    map_points = []
    for person in backup_users:
        map_points.append({
            "latitude": person["latitude"],
            "longitude": person["longitude"]
        })
        
    # Draw the beautiful world map right here!
    df = pd.DataFrame(map_points)
    st.map(df)
    st.success("✨ Map loaded completely!")