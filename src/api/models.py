from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Dict, Any


class SuburbSearchResult(BaseModel):
    """Search result for suburb lookup"""
    label: str = Field(..., description="Display label combining suburb and postcode")
    suburb: str = Field(..., description="Suburb name")
    postcode: str = Field(..., description="4-digit postcode")
    lga: str = Field(..., description="Local government area")
    risk_score: float = Field(..., description="Risk score from 0 (safe) to 1 (high risk)")


class Address(BaseModel):
    """Victorian address"""
    address: str = Field(..., description="Full street address")
    suburb: str = Field(..., description="Suburb name")
    postcode: str = Field(..., description="4-digit postcode")


class ParkingFacility(BaseModel):
    """Parking facility details"""
    facility_id: int = Field(..., description="Unique facility identifier")
    facility_name: str = Field(..., description="Facility name")


class ParkingSubmission(BaseModel):
    """Community submitted parking location"""
    parking_id: int = Field(..., description="Unique parking submission ID")
    address: str = Field(..., description="Street address")
    suburb: str = Field(..., description="Suburb name")
    postcode: str = Field(..., description="4-digit postcode")
    type: str = Field(..., description="Parking type: on-street, off-street, or secure")
    lighting: Optional[int] = Field(None, description="Lighting quality: 1=poor to 4=excellent")
    cctv: Optional[bool] = Field(None, description="CCTV availability")
    facilities: List[ParkingFacility] = Field(default=[], description="Available facilities at location")
    created_at: Optional[str] = Field(None, description="Submission timestamp")


class ParkingSubmissionRequest(BaseModel):
    """Request model for submitting parking location"""
    address: str = Field(..., description="Street address")
    suburb: str = Field(..., description="Suburb name")
    postcode: str = Field(..., description="Postcode")
    type: str = Field(..., description="Parking type", pattern="^(on-street|off-street|secure)$")
    lighting: Optional[int] = Field(None, ge=1, le=4, description="Lighting quality: 1=poor, 2=fair, 3=good, 4=excellent")
    cctv: Optional[bool] = Field(None, description="CCTV availability: true, false, or null for unknown")
    facilities: Optional[List[int]] = Field(default=[], description="List of facility IDs")


class ParkingSubmissionResponse(BaseModel):
    """Response model for parking submission"""
    parking_id: int = Field(..., description="Unique parking submission ID")
    message: str = Field(..., description="Success message")
    action: str = Field(..., description="Action performed: inserted, updated, or no_change")


class SaferSuburb(BaseModel):
    """Nearby suburb with lower risk score"""
    postcode: str = Field(..., description="4-digit postcode")
    suburb: str = Field(..., description="Suburb name")
    lga: str = Field(..., description="Local government area")
    distance_in_meters: int = Field(..., description="Distance from target postcode in meters")
    risk_score: float = Field(..., description="Risk score from 0 (safe) to 1 (high risk)")
    parking_count: int = Field(0, description="Number of community parking submissions")

    @field_validator('distance_in_meters', mode='before')
    @classmethod
    def round_distance(cls, v):
        """Convert float distance to int by rounding"""
        if isinstance(v, float):
            return round(v)
        return v


class CurrentLocation(BaseModel):
    """Current postcode information"""
    postcode: str = Field(..., description="4-digit postcode")
    suburb: str = Field(..., description="Suburb name")
    risk_score: float = Field(..., description="Risk score from 0 (safe) to 1 (high risk)")


class PostcodeFeedResponse(BaseModel):
    """Feed data for a specific postcode"""
    current: CurrentLocation = Field(..., description="Current location details")
    parking_submissions: List[ParkingSubmission] = Field(..., description="Community parking submissions")
    nearest_safer_suburbs: List[SaferSuburb] = Field(..., description="Nearby suburbs with lower risk")


class YearlyTheft(BaseModel):
    """Yearly theft statistics"""
    year: int = Field(..., description="Calendar year")
    thefts: int = Field(..., description="Number of reported thefts")


class StatisticsSummary(BaseModel):
    """Platform-wide statistics"""
    total_postcodes: int = Field(..., description="Number of postcodes covered")
    total_addresses: int = Field(..., description="Number of validated addresses")
    total_lgas: int = Field(..., description="Number of local government areas")
    total_submissions: int = Field(..., description="Number of community submissions")


class MotorcycleModel(BaseModel):
    """Motorcycle model with theft statistics"""
    brand: str = Field(..., description="Motorcycle brand")
    model: str = Field(..., description="Model name")
    total: int = Field(..., description="Total number of thefts")
    percentage: float = Field(..., description="Percentage of total thefts")
    model_risk: float = Field(..., description="Risk score from 0 (safe) to 1 (high risk)")


class RiskRankingItem(BaseModel):
    """Risk ranking entry for postcode or LGA"""
    # Postcode fields
    postcode: Optional[str] = Field(None, description="4-digit postcode")
    suburb: Optional[str] = Field(None, description="Suburb name")

    # LGA fields
    lga: Optional[str] = Field(None, description="Local government area")
    avg_risk: Optional[float] = Field(None, description="Average risk score for LGA")
    postcode_count: Optional[int] = Field(None, description="Number of postcodes in LGA")

    # Common field
    risk_score: Optional[float] = Field(None, description="Risk score from 0 (safe) to 1 (high risk)")


class PaginatedRiskResponse(BaseModel):
    """Paginated risk ranking response"""
    items: List[Dict[str, Any]] = Field(..., description="Risk ranking items")
    total: int = Field(..., description="Total number of items")


class ContactFormSubmission(BaseModel):
    """Contact form submission request"""
    email: EmailStr = Field(..., description="Contact email address")
    category: str = Field(..., description="Issue category")
    subject: str = Field(..., description="Issue subject")
    postcode: Optional[str] = Field(None, description="Related postcode")
    details: str = Field(..., description="Issue details")
    recaptchaToken: str = Field(..., description="reCAPTCHA verification token")


class ContactFormResponse(BaseModel):
    """Contact form submission response"""
    success: bool = Field(..., description="Whether submission was successful")
