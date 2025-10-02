from fastapi import APIRouter, Request, HTTPException
from typing import Optional, List
from datetime import datetime
from models import ParkingSubmissionRequest, ParkingSubmissionResponse

router = APIRouter(tags=["Parking"])

@router.post(
    "/v1/parking",
    response_model=ParkingSubmissionResponse,
    summary="Submit parking location",
    description="Submit a community contributed safe parking location. Address must be valid Victorian address.",
    response_description="Confirmation of parking submission with unique ID"
)
def submit_parking(
    request: Request,
    submission: ParkingSubmissionRequest
) -> ParkingSubmissionResponse:
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

        result = db.upsert_parking_contribution({
            "address": verified_address["address"],
            "suburb": verified_address["suburb"],
            "postcode": verified_address["postcode"],
            "type": submission.type,
            "lighting": submission.lighting,
            "cctv": submission.cctv
        }, facilities=submission.facilities or [])

        messages = {
            "inserted": "Parking suggestion submitted successfully",
            "updated": "Parking suggestion updated successfully",
            "no_change": "Parking suggestion submitted successfully" # I don't think it make sense to tell them it's a dupe?
        }

        return ParkingSubmissionResponse(
            parking_id=result["parking_id"],
            message=messages[result["action"]],
            action=result["action"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit parking suggestion: {str(e)}")
