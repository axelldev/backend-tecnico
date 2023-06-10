from pydantic import BaseModel, EmailStr, Field, constr


class User(BaseModel):
    """
    Users model.

    Attributes:
    - id (int): User ID.
    - first_name (str): first name of the user.
    - last_name (str): last name of the user.
    - phone (int): User phone number.
    - email (EmailStr): User email address.
    """

    id: str
    email: EmailStr
    phone: int
    first_name: str
    last_name: str
    password: str


class UserSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    phone: int = Field(
        ..., ge=1000000000, le=9999999999, description="User phone number"
    )
    first_name: constr(min_length=4, max_length=15) = Field(
        ..., description="First name of the user"
    )
    last_name: constr(min_length=4, max_length=15) = Field(
        ..., description="Last name of the user"
    )
    password: constr(min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Axell",
                "last_name": "Solis",
                "email": "axell@example.com",
                "phone": 5542771463,
                "password": "test1234"
            }
        }

