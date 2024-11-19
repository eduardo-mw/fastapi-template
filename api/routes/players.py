"""Players routes"""

from typing import Annotated

from bson import ObjectId
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Body
from models.Players import PlayerCollection, PlayerModel, UpdatePlayerModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument


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
    """List all players

    Parameters
    ----------
    db : DbDep
        database

    Returns
    -------
    PlayerCollection
        A list of all players
    """
    player_collection = db.get_collection("players")
    response = PlayerCollection(players=await player_collection.find().to_list(1000))
    return response


@players_router.get(
    "/{player_id}",
    tags=["players"],
    response_description="Get a single player",
    response_model=PlayerModel,
    response_model_by_alias=False,
)
async def read_player(player_id: str, db: DbDep) -> PlayerModel:
    """Get a single player

    Parameters
    ----------
    player_id : str
        Player id
    db : DbDep
        database

    Returns
    -------
    PlayerModel
        Single player

    Raises
    ------
    HTTPException
    """
    player_collection = db.get_collection("players")
    if (
        player := await player_collection.find_one({"_id": ObjectId(player_id)})
    ) is not None:
        return player

    raise HTTPException(status_code=404, detail=f"Player {player_id} not found")


@players_router.delete(
    "/{player_id}",
    tags=["players"],
    response_description="Delete a single player",
    response_model=PlayerModel,
    response_model_by_alias=False,
)
async def delete_player(player_id: str, db: DbDep) -> PlayerModel:
    """Delete a single player

    Parameters
    ----------
    player_id : str
        Player ID
    db : DbDep
        database

    Returns
    -------
    PlayerModel
        The player that was deleted

    Raises
    ------
    HTTPException
    """
    player_collection = db.get_collection("players")
    if (
        player := await player_collection.find_one_and_delete(
            {"_id": ObjectId(player_id)}
        )
    ) is not None:
        return player
    raise HTTPException(status_code=404, detail=f"Player {player_id} not found")


@players_router.post(
    "/",
    response_description="Add a new player",
    response_model=PlayerModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_player(db: DbDep, player: PlayerModel = Body(...)) -> PlayerModel:
    """Create a new player

    Parameters
    ----------
    db : DbDep
        database
    player : PlayerModel, optional
        JSON request for new player, by default Body(...)

    Returns
    -------
    PlayerModel
        Newly created player
    """
    player_collection = db.get_collection("players")
    new_player = await player_collection.insert_one(
        player.model_dump(by_alias=True, exclude=["id"])
    )
    created_player = await player_collection.find_one({"_id": new_player.inserted_id})
    return created_player


@players_router.put(
    "/{player_id}",
    response_description="Update a player",
    response_model=PlayerModel,
    response_model_by_alias=False,
)
async def update_player(
    player_id: str, db: DbDep, player: UpdatePlayerModel = Body(...)
):
    """
    Update individual fields of an existing player record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    player_collection = db.get_collection("players")

    player = {
        k: v for k, v in player.model_dump(by_alias=True).items() if v is not None
    }
    if len(player) >= 1:
        update_result = await player_collection.find_one_and_update(
            {"_id": ObjectId(player_id)},
            {"$set": player},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
    # The update is empty, but we should still return the matching document:
    if (
        existing_player := await player_collection.find_one({"_id": player_id})
    ) is not None:
        return existing_player
    raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
