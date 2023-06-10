"""
This module contains the user actions, list, detail, create.
"""
from fastapi import status, HTTPException, Path
from fastapi.routing import APIRouter
from pydantic import EmailStr
from pymongo.errors import DuplicateKeyError
from app.models.users import UserSchema
from app.config.database import users_collection
from app.serializers.users import userEntity, userEntities
from app.utils.password import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users():
    """Retrieves all the users."""
    return userEntities(users_collection.find())


@router.get("/{email}")
def detail_user(
    email: EmailStr = Path(
        ..., description="A valid email address", example="someuser@example.com"
    )
):
    """Retrieves the detail of a user by his email."""
    user = users_collection.find_one({"email": email})
    if user:
        return userEntity(user)
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Not found user with email {email}")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    """Creates a new user."""
    user.password = hash_password(user.password)
    try:
        id = users_collection.insert_one(user.dict()).inserted_id
        user = users_collection.find_one({"_id": id})
    except DuplicateKeyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "This email address is already in use!"
        )
    return userEntity(user)
