from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Float,
    ARRAY,
    func,
)
from sqlalchemy.ext.declarative import declarative_base

from app.models.common import DateTimeModelMixin
from app.models.rwmodel import RWModel
from pydantic import BaseModel, ConfigDict
from typing import List
from app.schemas.calendar import CalendarEventBase  # <-- this should be a Pydantic model


Base = declarative_base()

class CalendarEvent(RWModel, DateTimeModelMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_uid = Column(Text, nullable=False, unique=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    status = Column(Text, nullable=False, index=True)
    summary = Column(Text, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    rrule = Column(Text, nullable=True)
    exdates = Column(ARRAY(DateTime(timezone=True)), nullable=True)
    dtstamp = Column(DateTime(timezone=True), nullable=True)
    event_created = Column(DateTime(timezone=True), nullable=True)
    last_modified = Column(DateTime(timezone=True), nullable=True)
    sequence = Column(Integer, nullable=True)
    transp = Column(Text, nullable=True)
    embedding = Column(ARRAY(Float), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.current_timestamp()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class CalendarEventsResponse(BaseModel):
    events: List[CalendarEventBase]
    total: int

    model_config = ConfigDict(from_attributes=True)
