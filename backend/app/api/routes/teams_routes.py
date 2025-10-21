from fastapi import APIRouter
from app.schemas.team_schema import TeamSchema
from app.services.data_fetch.id_fetcher import get_team_id

teams_router = APIRouter()

@teams_router.post("/team_id")
def get_team(request: TeamSchema):
    result = get_team_id(request.team_name, request.league_name, request.season)

    if not result:
        return {"error": "Team not found."}

    return result