from fastapi import APIRouter
from app.services.data_fetch.team_fetcher import get_league_id
from app.schemas.league_schema import LeagueSchema

standings_router = APIRouter()

@standings_router.post("/league_name")
def get_standings(request: LeagueSchema):
    return get_league_id(request.league_name)