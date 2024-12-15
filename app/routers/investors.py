from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Investor, Commitment
from app.schemas import Investor as InvestorSchema
from app.database import get_db

router = APIRouter()

# If more APIs are added, would make a services folder and separate APIs into their own files

# Serialize an Investor object to a dictionary suitable for API response.
def serialize_investor(investor: Investor) -> dict:
    return {
        "id": investor.id,
        "name": investor.name,
        "type": investor.type,
        "country": investor.country,
        "date_added": investor.date_added.isoformat() if investor.date_added else None,
        "last_updated": investor.last_updated.isoformat() if investor.last_updated else None,
        "commitments": [
            {"asset_class": c.asset_class, "amount": c.amount, "currency": c.currency}
            for c in investor.commitments
        ],
    }

# Retrieve all investors with their details and commitments.
@router.get("/investors", response_model=list[InvestorSchema])
def get_investors(db: Session = Depends(get_db)):
    investors = db.query(Investor).all()
    return [
        {
            "id": investor.id,
            "name": investor.name,
            "type": investor.type,
            "country": investor.country,
            "total_commitments": sum(c.amount for c in investor.commitments),  # Calculates total commitments per investor
            "date_added": investor.date_added.isoformat() if investor.date_added else None,
            "last_updated": investor.last_updated.isoformat() if investor.last_updated else None,
            "commitments": [
                {"asset_class": c.asset_class, "amount": c.amount, "currency": c.currency}
                for c in investor.commitments
            ],
        }
        for investor in investors
    ]

# Need to add total commitment here for consistency
# Retrieve a specific investor's details and optionally filter commitments by asset class.
@router.get("/investors/{investor_id}", response_model=InvestorSchema)
def get_investor_details(investor_id: int, asset_class: str = None, db: Session = Depends(get_db)):
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    # Query commitments and apply filtering
    commitments_query = db.query(Commitment).filter(Commitment.investor_id == investor_id)
    if asset_class:
        commitments_query = commitments_query.filter(Commitment.asset_class == asset_class)
    commitments = commitments_query.all()

    # Calculate total commitments (sum of amounts)
    total_commitments = sum(c.amount for c in commitments)

    # Prepare the response
    investorData = {
        "id": investor.id,
        "name": investor.name,
        "type": investor.type,
        "country": investor.country,
        "date_added": investor.date_added.isoformat() if investor.date_added else None,
        "last_updated": investor.last_updated.isoformat() if investor.last_updated else None,
        "total_commitments": total_commitments,  # Add total commitments here
        "commitments": [
            {"asset_class": c.asset_class, "amount": c.amount, "currency": c.currency}
            for c in commitments
        ],
    }
    return investorData

