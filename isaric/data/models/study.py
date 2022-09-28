import datetime

from pydantic import BaseModel


class Study(BaseModel):

    id: int
    name: str
    date: datetime.datetime
    end_date: datetime.datetime = None
    location: dict[str]  # GeoJSON
    country_iso3: str
    description: str
