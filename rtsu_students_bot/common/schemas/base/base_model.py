from pydantic import BaseModel as BModel


class BaseModel(BModel):
    class Config:
        orm_mode = True
