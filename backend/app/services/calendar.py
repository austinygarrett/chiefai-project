import logging
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from icalendar import Calendar as ICS_Calendar

from app.api.dependencies.database import get_repository
from app.core import constant
from app.models.user import User
from app.schemas.calendar import CalendarEventBase, CalendarEventInCreate
from app.services.base import BaseService
from app.utils import ServiceResult, return_service
from app.database.repositories.calendar import CalendarRepository
from app.utils.openai_utils import embed_texts_async

logger = logging.getLogger(__name__)


class CalendarService(BaseService):
    @return_service
    async def get_calendar_events(
        self,
        calendar_repo: CalendarRepository = Depends(get_repository(CalendarRepository)),
        user: User = None,
    ) -> ServiceResult:
        try:
            events = await calendar_repo.get_calendar_events(user_id=user.id)
        except Exception as e:
            logger.error(f"Error retrieving calendar events: {e}")
            return dict(
                status_code=HTTP_400_BAD_REQUEST,
                content={"message": "Error retrieving calendar events"}
            )

        return dict(
            status_code=HTTP_200_OK,
            content={
                "message": constant.SUCCESS_GET_USERS,
                "data": jsonable_encoder([
                    CalendarEventBase.model_validate(event) for event in events
                ]),
            },
        )

    @return_service
    async def process_and_save_calendar(
        self,
        calendar_repo: CalendarRepository = Depends(get_repository(CalendarRepository)),
        user: User = None,
        calendar: ICS_Calendar = None,
    ) -> ServiceResult:
        try:
            events = [c for c in calendar.walk() if c.name == "VEVENT"]
            saved = []
            event_texts = [
                f"{e.get('SUMMARY') or ''}\n{e.get('DESCRIPTION') or ''}\n{e.get('LOCATION') or ''}" for e in events
            ]            
            embeddings = await embed_texts_async(event_texts)
            for i, e in enumerate(events):
                try:
                    embedding = embeddings[i]

                    summary = str(e.get("SUMMARY", ""))
                    event_data = CalendarEventInCreate(
                        event_uid=str(e.get("UID")),
                        user_id=user.id,
                        status=str(e.get("STATUS", "CONFIRMED")),
                        summary=summary,
                        start_time=e.decoded("DTSTART"),
                        end_time=e.decoded("DTEND"),
                        rrule=str(e.get("RRULE")) if e.get("RRULE") else None,
                        exdates=[
                            exd.dt for exd in e.get("EXDATE").dts
                        ] if e.get("EXDATE") else None,
                        dtstamp=e.decoded("DTSTAMP") if e.get("DTSTAMP") else None,
                        event_created=e.decoded("CREATED") if e.get("CREATED") else None,
                        last_modified=e.decoded("LAST-MODIFIED") if e.get("LAST-MODIFIED") else None,
                        sequence=int(e.get("SEQUENCE")) if e.get("SEQUENCE") else None,
                        transp=str(e.get("TRANSP")) if e.get("TRANSP") else None,
                        embedding=embedding, 
                    )

                    result = await calendar_repo.create_event(event_data)
                    saved.append(result)

                except Exception as ie:
                    logger.warning(f"Skipping invalid event: {ie}")
                    continue

        except Exception as e:
            logger.error(f"Failed to parse and save calendar: {e}")
            return dict(
                status_code=HTTP_400_BAD_REQUEST,
                content={"message": f"Failed to parse calendar: {e}"}
            )

        return {
            "status_code": HTTP_201_CREATED,
            "content": {
                "message": "Calendar uploaded and events saved.",
                "data": jsonable_encoder([
                    CalendarEventBase.model_validate(evt) for evt in saved
                ]),
            }
        }
        