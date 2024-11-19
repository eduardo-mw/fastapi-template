from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model
# so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


# export interface IPlayer {
#   name: string;
#   displayName: string;
#   iconUrl?: string;
#   createdAt?: Date;
#   updatedAt?: Date;
# }


class PlayerModel(BaseModel):
    """
    Container for a single player record.
    """

    # The primary key for the PlayerModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB, due to pythons _id
    # but provided as `id` in the API requests and responses.
    # Defaults to none so id does not need to be provided upon creation
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    displayName: str = Field()
    iconUrl: str = Field(default="https://placehold.co/128x128.webp")
    # Get the current time in ISO 8601 format
    createdAt: datetime = Field(default=datetime.now().isoformat())
    updatedAt: datetime = Field(default=datetime.now().isoformat())
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "displayName": "jdoe111",
                "iconUrl": "https://placehold.co/128x128.webp",
                "createdAt": "2024-10-18 18:59:35.850711",
                "updatedAt": "2024-10-18 18:59:35.850711",
            }
        },
    )


class UpdatePlayerModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: str = Field(...)
    displayName: str = Field(...)
    iconUrl: str = Field(default="https://placehold.co/128x128.webp")
    createdAt: datetime = Field(default=datetime.now().isoformat())
    updatedAt: datetime = Field(default=datetime.now().isoformat())
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "displayName": "jdoe111",
                "iconUrl": "https://placehold.co/128x128.webp",
                "createdAt": "2024-10-18 18:59:35.850711",
                "updatedAt": "2024-10-18 18:59:35.850711",
            }
        },
    )


class PlayerCollection(BaseModel):
    """
    A container holding a list of `PlayerModel` instances.

    This exists because providing a top-level array
    in a JSON response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    players: List[PlayerModel]
