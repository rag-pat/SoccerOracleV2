from fastapi import APIRouter
from app.schemas.league_schema import LeagueSchema
from app.services.data_fetch.id_fetcher import get_league_id

standings_router = APIRouter()

@standings_router.post("/league_name")
def get_standings(request: LeagueSchema):
    league_id = get_league_id(request.league_name)

    if not league_id:
        return {"error": "League not found."}

    return {"league_id": league_id}