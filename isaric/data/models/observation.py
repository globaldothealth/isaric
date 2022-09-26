import datetime

from pydantic import BaseModel

from ...taxonomy import Observation


class Observation(BaseModel):

    id: int
    visit_id: int
    subject_id: int
    study_id: int

    date: datetime.datetime
    end_date: datetime.datetime = None
    value_num: float = None
    value_char: str = None
    is_present: bool = None
    name: Observation
