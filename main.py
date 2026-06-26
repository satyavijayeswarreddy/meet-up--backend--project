from fastapi import FastAPI, Query
import sqlite3
import requests
from datetime import datetime
import math

app = FastAPI()
DB_PATH = "meetup.db"

# 🧮 Math Trick: Calculate distance between two points on Earth
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    r_lat1, r_lon1, r_lat2, r_lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = r_lat2 - r_lat1
    dlon = r_lon2 - r_lon1
    a = math.sin(dlat/2)**2 + math.cos(r_lat1) * math.cos(r_lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c  # Returns distance in kilometers

# 📥 1. Ingestion Route: Scrapes internet and ADDS to the database
@app.get("/load-users")
def load_users(count: int = 50):
    # Connect to database storage box
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table if it's not there yet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY, email TEXT, first_name TEXT, last_name TEXT,
            gender TEXT, latitude REAL, longitude REAL, run_id TEXT, datetime TEXT
        )
    ''')
    
    # Fetch random users from the internet API
    response = requests.get(f"https://randomuser.me/api/?results={count}").json()
    run_id = f"run_{int(datetime.now().timestamp())}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for user in response['results']:
        cursor.execute('''
            INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user['login']['uuid'],
            user['email'],
            user['name']['first'],
            user['name']['last'],
            user['gender'],
            float(user['location']['coordinates']['latitude']),
            float(user['location']['coordinates']['longitude']),
            run_id,
            current_time
        ))
    
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Added {count} users to the database!"}

# 📋 2. Fetch All Users Route (For our Streamlit search selector dropdown)
@app.get("/get-all-users")
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT uid, first_name, last_name, email, latitude, longitude FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"uid": r[0], "first_name": r[1], "last_name": r[2], "email": r[3], "latitude": r[4], "longitude": r[5]}
        for r in rows
    ]

# 🎯 3. Find Closest Neighbors Route
@app.get("/get-nearest-neighbors")
def get_nearest_neighbors(uid: str, limit: int = 100):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT uid, first_name, last_name, email, latitude, longitude FROM users")
    all_users = cursor.fetchall()
    conn.close()
    
    # Find our target selected person
    target = next((u for u in all_users if u[0] == uid), None)
    if not target:
        return []
    
    t_lat, t_lon = target[4], target[5]
    neighbors = []
    
    # Calculate distances to everyone else
    for u in all_users:
        if u[0] == uid:
            continue
        dist = calculate_distance(t_lat, t_lon, u[4], u[5])
        neighbors.append({
            "first_name": u[1], "last_name": u[2], "email": u[3],
            "latitude": u[4], "longitude": u[5], "distance_km": dist
        })
    
    # Sort them from closest to furthest, and grab the top matches
    neighbors.sort(key=lambda x: x["distance_km"])
    return neighbors[:limit]
import random

# 🎲 Bonus API 1: Fetch one completely random user object from the database
@app.get("/get-random-user")
def get_random_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT uid, first_name, last_name, email, latitude, longitude FROM users")
    all_users = cursor.fetchall()
    conn.close()
    
    if not all_users:
        raise HTTPException(status_code=404, detail="Database is empty")
        
    chosen = random.choice(all_users)
    return {"uid": chosen[0], "first_name": chosen[1], "last_name": chosen[2], "email": chosen[3], "latitude": chosen[4], "longitude": chosen[5]}

@app.get("/get-random-username")
def get_random_username():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM users")
    all_names = cursor.fetchall()
    conn.close()
    
    if not all_names:
        raise HTTPException(status_code=404, detail="No users available")
        
    chosen = random.choice(all_names)
    return {"username": f"{chosen[0]}_{chosen[1]}".lower()}