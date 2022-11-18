"""
Pydantic types used in isaric/schemas
"""

from pydantic import BaseModel, validator, NonNegativeInt, PastDate


class IntegerRange(BaseModel):
    "Range of non-negative integers"
    start: NonNegativeInt
    end: NonNegativeInt

    @validator("end")
    def end_greater_than_start(cls, v, values):
        if values.get("start") and v < values.get("start"):
            raise ValueError("IntegerRange: start should be lower than end")
        return v


class DateRange(BaseModel):
    "Range of dates in the past"
    start: PastDate
    end: PastDate

    @validator("end")
    def end_after_start(cls, v, values):
        if v < values["start"]:
            raise ValueError("DateRange: end date has to be after start date")
        return v
