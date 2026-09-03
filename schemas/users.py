from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
