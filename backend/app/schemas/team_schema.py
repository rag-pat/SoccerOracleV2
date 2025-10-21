from pydantic import BaseModel

class TeamSchema(BaseModel):
    team_name: str
    league_name: str
    season: int | None = None