import pandas as pd
from serpapi import GoogleSearch
import os
import time

def find_global_dental_leads():
    api_key = os.getenv("SERP_API_KEY")
    
    # Top Global English-Speaking Markets for Dental AI
    cities = [
        "New York, NY", "Los Angeles, CA", "London, UK", 
        "Sydney, Australia", "Toronto, Canada", "Dubai, UAE",
        "Singapore", "Dublin, Ireland", "Auckland, New Zealand",
        "Manchester, UK"
    ]
    
    all_results = []

    for city in cities:
        print(f"Scouting for leads in: {city}...")
        params = {
            "engine": "google_maps",
            "q": "dentist",
            "location": city,
            "type": "search",
            "api_key": api_key
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            local_results = results.get("local_results", [])
            
            for entry in local_results:
                entry['found_in_city'] = city  # Tag the city so you know who to call
                all_results.append(entry)
            
            # Small pause to be polite to the API
            time.sleep(1) 
        except Exception as e:
            print(f"Error searching {city}: {e}")

    # Process with Pandas
    df = pd.DataFrame(all_results)

    # 1. Selection: Only keep what helps you sell
    cols = ['title', 'address', 'phone', 'website', 'rating', 'reviews', 'found_in_city']
    df = df[df.columns.intersection(cols)]

    # 2. The "Leaky Bucket" Filter: 
    # Sort by lowest rating (needs reputation AI) 
    # then highest reviews (has the budget/volume to pay you)
    df = df.sort_values(by=['rating', 'reviews'], ascending=[True, False])

    # 3. Final Polish
    df = df.dropna(subset=['phone', 'website']) # Only leads you can actually contact
    
    df.to_csv("monday_leads.csv", index=False)
    print(f"\nSuccess! Found {len(df)} global leads. File 'monday_leads.csv' is ready.")

if __name__ == "__main__":
    find_global_dental_leads()
