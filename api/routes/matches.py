from fastapi import APIRouter

matches_router = APIRouter()


@matches_router.get("/", tags=["matches"])
async def read_matches():
    return [{"username": "Rick"}, {"username": "Morty"}]


@matches_router.get("/{match_id}", tags=["matches"])
async def read_match(match_id: str):
    return {"match_id": match_id}


@matches_router.delete("/{match_id}", tags=["matches"])
async def delete_match(match_id: str):
    return {"match_id": match_id}
