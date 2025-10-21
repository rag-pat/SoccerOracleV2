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
    
    # Premier League season typically runs from August to May
    # If we're in the first half of the year, we're still in the previous season
    if month >= 8:  # August onwards, we're in the new season
        return year
    else:  # Before August, we're still in the previous season
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

def get_team_id(team_name: str, league_name: str, season: int | None = None):
    """Fetch team ID for a given team name."""
    if not season:
        season = get_season_year()
    
    print(f"[DEBUG] Using season: {season}")

    league_id = get_league_id(league_name)
    print(f"[DEBUG] Resolved league_id for '{league_name}': {league_id}")

    if not league_id:
        print("[ERROR] No valid league_id found")
        return None

    # Use season 2023 as it has reliable data
    working_season = 2023
    url = f"{BASE_URL}/teams"
    
    # Get all teams first (search parameter seems to have issues)
    params = {"league": league_id, "season": working_season}
    print(f"[DEBUG] Calling API with params: {params}")
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[ERROR] Team fetch failed: {response.status_code} → {response.text[:200]}")
        return None

    data = response.json()
    all_teams = data.get("response", [])
    print(f"[DEBUG] Found {len(all_teams)} teams for league {league_id}, season {working_season}")

    if not all_teams:
        print(f"[ERROR] No teams found for league {league_id}, season {working_season}")
        return None

    # Filter teams by name using fuzzy matching
    team_names = [t["team"]["name"] for t in all_teams]
    print(f"[DEBUG] Available teams: {team_names[:5]}...")  # Show first 5 teams
    
    # Use fuzzy matching to find the best match
    best_match, confidence = process.extractOne(team_name, team_names)
    print(f"[DEBUG] Best match for '{team_name}': '{best_match}' (confidence: {confidence})")
    
    if confidence < 60:  # If confidence is too low, return None
        print(f"[ERROR] No good match found for '{team_name}' (confidence: {confidence})")
        return None
    
    # Find the matched team
    matched_team = next(t for t in all_teams if t["team"]["name"] == best_match)
    team_id = matched_team["team"]["id"]
    
    print(f"[SUCCESS] Found team '{best_match}' → ID: {team_id}")
    return team_id