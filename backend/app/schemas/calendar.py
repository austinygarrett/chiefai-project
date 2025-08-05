from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.message import ApiResponse


class CalendarEventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    event_uid: str
    user_id: int
    status: str
    summary: str
    start_time: datetime
    end_time: datetime
    rrule: str | None = None
    exdates: list[datetime] | None = None
    dtstamp: datetime | None = None
    event_created: datetime | None= None
    last_modified: datetime | None = None
    sequence: int | None = None
    transp: str | None = None
    embedding: list[float] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class CalendarEventInCreate(BaseModel):
    event_uid: str
    user_id: int
    status: str
    summary: str
    start_time: datetime
    end_time: datetime
    rrule: str | None = None
    exdates: list[datetime] | None = None
    dtstamp:  datetime | None = None
    event_created: datetime | None = None
    last_modified: datetime | None = None
    sequence: int | None = None
    transp: str | None = None
    embedding:list[float] | None = None
    
class CalendarEventOutData(CalendarEventBase):
    pass
    
class CalendarEventResponse(ApiResponse):
    message: str = "Calendar Event API Response"
    data: CalendarEventOutData | list[CalendarEventOutData]
    detail: dict[str, Any] | None = {"key": "val"}
    

class Message(BaseModel):
    role: str
    text: str

class DeepChatRequest(BaseModel):
    messages: List[Message]
