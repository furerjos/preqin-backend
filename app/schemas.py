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
    type: Optional[str]  # Allow None
    country: Optional[str]  # Allow None
    date_added: Optional[str]  # Allow None
    last_updated: Optional[str]  # Allow None
    commitments: List[Commitment]

    class Config:
        orm_mode = True
