import requests
from app.core.settings import api_key
from fuzzywuzzy import process
from datetime import datetime
from app.models.db.league_model import get_league_by_name, insert_league

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
    existing_league = get_league_by_name(league_name)
    if existing_league:
        return existing_league[0]

    url = f"{BASE_URL}/leagues"
    params = {"search": league_name}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return {"error_code": response.status_code, "message": response.json().get("message", "API error")}

    data = response.json().get("response", [])
    if not data:
        return {"errorCode": 404, "message": "No leagues found"}
    
    choices = [l["league"]["name"] for l in data]
    best_match, _ = process.extractOne(league_name, choices)
    league_info = next(l for l in data if l["league"]["name"] == best_match)

    league_id = league_info["league"]["id"]
    league_name_api = league_info["league"]["name"]

    insert_league(league_id, league_name_api)

    return league_id