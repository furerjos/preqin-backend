from pydantic import BaseModel
from typing import List, Optional

class Commitment(BaseModel):
    asset_class: str
    amount: float
    currency: str

    class Config:
        orm_mode = True

class Investor(BaseModel):
    id: int
    name: str
    type: str
    country: str
    total_commitments: float
    date_added: str
    last_updated: str
    commitments: List[Commitment]

    class Config:
        orm_mode = True
