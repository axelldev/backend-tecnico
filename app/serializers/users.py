from app.models.users import User


def userEntity(user) -> User:
    """Parse an user bson entity to a User Instance.
    @return: A User model instance.
    """
    return User(
        id=str(user["_id"]),
        email=user["email"],
        phone=user["phone"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        password=user["password"],
    )


def userEntities(users) -> list[User]:
    """Parse a list of user entities to a list of Users.
    @return: list of User model.
    """
    return [userEntity(user) for user in users]
