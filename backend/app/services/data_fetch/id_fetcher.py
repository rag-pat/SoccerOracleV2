import requests
from app.core.settings import api_key
from fuzzywuzzy import process
from datetime import datetime

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

def get_season_year():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    if month >= 7:
        return year

    return year - 1

def get_league_id(league_name):
    """Fetch league ID for a specific league."""
    url = f"{BASE_URL}/leagues"
    params = {"search": league_name}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        leagues = data.get("response", [])
        
        if leagues:
            # Get all league names and find best match
            choices = [l["league"]["name"] for l in leagues]
            best_match, _ = process.extractOne(league_name, choices)
            return next(l["league"]["id"] for l in leagues if l["league"]["name"] == best_match)
        else:
            return {"error_code": 404, "message": "No leagues found"}
    else:
        return {"error_code": response.status_code, "message": response.json().get("message")}