from pydantic import BaseModel, ConfigDict









class BookBase(BaseModel):
    title: str
    author: str
    pages: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

model_config = ConfigDict(from_attributes=True)