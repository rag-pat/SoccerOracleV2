from fastapi import APIRouter
from app.schemas.player_schema import PlayerSchema
from app.services.data_fetch.id_fetcher import get_player_id

players_router = APIRouter()

@players_router.post("/player_id")
def get_player(request: PlayerSchema):
    result = get_player_id(request.player_name, request.team_name, request.league_name, request.season)

    if not result:
        return {"error": "Player not found."}

    player_id, player_name = result
    return {
        "player_id": player_id,
        "player_name": player_name,
    }
