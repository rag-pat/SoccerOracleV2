from fastapi import FastAPI
from app.api.routes.standings_route import standings_router

app = FastAPI(
    title="Football Stats API",
    description="API for football statistics including standings, team comparisons, and player stats",
    version="1.0.0"
)

app.include_router(standings_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Football Stats API"}