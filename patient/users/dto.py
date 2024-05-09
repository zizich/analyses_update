from pydantic import BaseModel, Field


class UserData(BaseModel):
    full_name: str
    phone: int
    address: str
