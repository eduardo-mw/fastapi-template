"""Entrypoint"""

from fastapi import FastAPI
from routes import players, matches
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.include_router(players.players_router, prefix="/players", tags=["players"])
app.include_router(matches.matches_router, prefix="/matches", tags=["matches"])


@app.get("/health")
def get_health() -> dict:
    """Get health check status

    Returns
    -------
    dict
        Status of service
    """
    return {"status": "up"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
