from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, Field, validator, model_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @model_validator(mode="before")
    def validate_fields(cls, values):
        # ✅ Check if username contains spaces
        if " " in values.get("username", ""):
            raise ValueError("Username cannot contain spaces")
        return values
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    user_id: int
    message_text: str

class MessageResponse(BaseModel):
    id: int
    user_id: int
    message_text: str

    class Config:
        orm_mode = True