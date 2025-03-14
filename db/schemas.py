from pydantic import BaseModel

class CreateTable(BaseModel):
    name: str
    email: str

class Table(CreateTable):
    id: int

    class Config:
        from_attributes = True