from pydantic import BaseModel


class Animal(BaseModel):
    id: int
    name: str
    photo_url: str
    description: str

    class Config:
        orm_mode = True
