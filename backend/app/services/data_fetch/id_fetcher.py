import requests
from app.core.settings import api_key
from fuzzywuzzy import process
from datetime import datetime
from app.models.db.league_model import get_league_by_name, insert_league
from app.models.db.team_model import get_team_by_name, insert_team

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

def get_season_year():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    if month >= 8:
        return year
    else:
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

    league_id = get_league_id(league_name)

    if not league_id:
        return None

    # Check database cache first
    existing_team = get_team_by_name(team_name, league_id)
    if existing_team:
        return existing_team[0]

    working_season = 2023
    url = f"{BASE_URL}/teams"

    params = {"league": league_id, "season": working_season}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    all_teams = data.get("response", [])

    if not all_teams:
        return None

    team_names = [t["team"]["name"] for t in all_teams]
    
    # Use fuzzy matching to find the best match
    best_match, confidence = process.extractOne(team_name, team_names)
    
    if confidence < 60:
        return None
    
    # Find the matched team
    matched_team = next(t for t in all_teams if t["team"]["name"] == best_match)
    team_id = matched_team["team"]["id"]
    team_name_api = matched_team["team"]["name"]
    
    # Cache the team in database
    insert_team(team_id, team_name_api, league_id, league_name)
    
    print(f"[SUCCESS] Found team '{best_match}' → ID: {team_id}")
    return team_id