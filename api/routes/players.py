from fastapi import APIRouter, Depends
from models.Players import PlayerCollection
from dependencies import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated

players_router = APIRouter()
DbDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


@players_router.get(
    "/",
    response_description="List all players",
    response_model=PlayerCollection,
    response_model_by_alias=False,
    tags=["players"],
)
async def list_players(db: DbDep) -> PlayerCollection:
    player_collection = db.get_collection("players")
    return PlayerCollection(players=await player_collection.find().to_list(
        1000
        ))


# @players_router.get("/{player_id}", tags=["players"])
# async def read_player(player_id: str):
#     return {"player_id": player_id}


# @players_router.delete("/{player_id}", tags=["players"])
# async def delete_player(player_id: str):
#     return {"player_id": player_id}


# @players_router.post(
#     "/",
#     response_description="Add a new player",
#     response_model=PlayerModel,
#     status_code=status.HTTP_201_CREATED,
#     response_model_by_alias=False,
# )
# async def create_player(player: PlayerModel = Body(...)):
#     """Insert a new player record

#     Parameters
#     ----------
#     player : PlayerModel, optional
#         Player JSON request, by default Body(...)
#     """
#     # new_player = await player_collection.insert_one(
#     #     player.model_dump(by_alias=True, exclude=["id"])
#     # )
#     # created_player = await player_collection.find_one({"_id": new_player.inserted_id})
#     return {"hello": "world"}
