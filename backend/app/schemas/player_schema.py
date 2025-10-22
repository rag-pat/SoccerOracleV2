from pydantic import BaseModel

class PlayerSchema(BaseModel):
    player_name: str
    team_name: str
    league_name: str
    season: int | None = None
