from pydantic import BaseModel

class LeagueSchema(BaseModel):
    league_name: str