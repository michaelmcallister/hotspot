from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class ParkingSubmission(BaseModel):
    address: str = Field(..., description="Street address")
    suburb: str = Field(..., description="Suburb name")
    postcode: str = Field(..., description="Postcode")
    type: str = Field(..., description="Parking type", pattern="^(on-street|off-street|secure)$")
    lighting: Optional[int] = Field(None, ge=1, le=4, description="Lighting quality: 1=poor, 2=fair, 3=good, 4=excellent")
    cctv: Optional[bool] = Field(None, description="CCTV availability: true, false, or null for unknown")
    facilities: Optional[List[int]] = Field(default=[], description="List of facility IDs")

class ParkingResponse(BaseModel):
    parking_id: int
    message: str

@router.post("/v1/parking", response_model=ParkingResponse)
def submit_parking(
    request: Request,
    submission: ParkingSubmission
):
    db = request.app.state.db

    try:
        # To prevent abuse we only allow addresses that we know about (no custom ones)
        verified_address = db.verify_address(
            submission.address,
            submission.suburb,
            submission.postcode
        )

        if not verified_address:
            raise HTTPException(
                status_code=400,
                detail="Invalid address"
            )

        parking_id = db.insert_parking_contribution({
            "address": verified_address["address"],
            "suburb": verified_address["suburb"],
            "postcode": verified_address["postcode"],
            "type": submission.type,
            "lighting": submission.lighting,
            "cctv": submission.cctv
        })

        if submission.facilities:
            for facility_id in submission.facilities:
                db.insert_parking_facility(parking_id, facility_id)

        return ParkingResponse(
            parking_id=parking_id,
            message="Parking suggestion submitted successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit parking suggestion: {str(e)}")

@router.get("/v1/parking/{postcode}")
def get_parking_by_postcode(
    request: Request,
    postcode: str
):
    db = request.app.state.db

    parking_list = db.get_parking_by_postcode(postcode)

    for parking in parking_list:
        facilities = db.get_facilities_for_parking(parking["parking_id"])
        parking["facilities"] = facilities

    return parking_list
