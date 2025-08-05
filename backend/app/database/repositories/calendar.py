from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database.repositories.base import BaseRepository, db_error_handler
from app.models.calendar import CalendarEvent
from app.schemas.calendar import CalendarEventInCreate
from app.services.vector_store import calendar_vector_store
from app.utils.openai_utils import get_embedding  # assumes you already have this

class CalendarRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection) -> None:
        super().__init__(conn)

    @db_error_handler
    async def get_calendar_events(self, *, user_id: int) -> list[CalendarEvent]:
        query = select(CalendarEvent).where(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.deleted_at.is_(None),
            )
        )

        raw_results = await self.connection.execute(query)
        results = raw_results.scalars().all()
        return results

    @db_error_handler
    async def get_event_by_uid(self, *, user_id: int, event_uid: str) -> CalendarEvent | None:
        query = select(CalendarEvent).where(
            and_(
                CalendarEvent.user_id == user_id,
                CalendarEvent.event_uid == event_uid,
                CalendarEvent.deleted_at.is_(None),
            )
        ).limit(1)

        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()
        return result.CalendarEvent if result else None

    @db_error_handler
    async def create_event(self, event_in: CalendarEventInCreate) -> CalendarEvent:
        new_event = CalendarEvent(**event_in.model_dump(exclude_none=True))
        embedding = get_embedding(new_event.summary or "")
        new_event.embedding = embedding 

        self.connection.add(new_event)
        await self.connection.commit()
        await self.connection.refresh(new_event)

        calendar_vector_store.add(
            embedding,
            (
                new_event.summary,
                new_event.status,
                new_event.rrule,
                new_event.start_time,
                new_event.end_time,
            )
        )

        return new_event
    
    @db_error_handler
    async def get_relevant_context(self, query_embedding: list[float], user_id: int, k: int = 15) -> str:
        chunks = calendar_vector_store.search(user_id, query_embedding, k)
        return "\n\n".join(chunks) if chunks else "No relevant events found."

    @db_error_handler
    async def get_all_with_embeddings_by_user(self) -> dict[int, list[tuple]]:
        sql = text("""
            SELECT user_id, embedding, summary, status, rrule, start_time, end_time
            FROM events
            WHERE deleted_at IS NULL AND embedding IS NOT NULL
        """)

        result = await self.connection.execute(sql)
        rows = result.fetchall()

        grouped: dict[int, list[tuple]] = {}
        for user_id, *rest in rows:
            if user_id not in grouped:
                grouped[user_id] = []
            grouped[user_id].append(tuple(rest))

        return grouped