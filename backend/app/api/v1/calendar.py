from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from icalendar import Calendar
from app.models.user import User
from app.api.dependencies.auth import get_current_user_auth
from app.api.dependencies.database import get_repository
from app.api.dependencies.service import get_service
from app.models.calendar import CalendarEventsResponse
from starlette.status import HTTP_200_OK
from app.utils import handle_result

from app.database.repositories.calendar import CalendarRepository
from app.services.calendar import CalendarService
from app.schemas.calendar import CalendarEventResponse, DeepChatRequest
from app.utils.openai_utils import ask_gpt_with_context, get_embedding

router = APIRouter()


@router.get(
    "",
    status_code=HTTP_200_OK,
    response_model=CalendarEventsResponse,
    name="calendar:get",
)
async def read_calendar(
    *,
    user: User = Depends(get_current_user_auth()),
    calendar_service: CalendarService = Depends(get_service(CalendarService)),
    calendar_repo: CalendarRepository = Depends(get_repository(CalendarRepository)),
) -> CalendarEventsResponse:
    result = await calendar_service.get_calendar_events(
        calendar_repo=calendar_repo,
        user=user,
    )

    return await handle_result(result)


@router.put(
    "/upload",
    status_code=HTTP_200_OK,
    response_model=CalendarEventResponse,
    name="calendar:upload",
)
async def upload_calendar(
    *,
    user: User = Depends(get_current_user_auth()),
    calendarFile: UploadFile = File(...),
    calendar_service: CalendarService = Depends(get_service(CalendarService)),
    calendar_repo: CalendarRepository = Depends(get_repository(CalendarRepository)),
) -> CalendarEventResponse:
    if not calendarFile.filename.endswith(".ics"):
        raise HTTPException(status_code=400, detail="Only .ics files are supported.")

    contents = await calendarFile.read()

    try:
        calendar = Calendar.from_ical(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ICS file: {str(e)}")

    result = await calendar_service.process_and_save_calendar(
        calendar_repo=calendar_repo,
        user=user,
        calendar=calendar,
    )

    return await handle_result(result)

@router.post(
    "/chat",
    status_code=HTTP_200_OK,
    name="calendar:chat",
)
async def deepchat_calendar_query(
    body: DeepChatRequest,
    user: User = Depends(get_current_user_auth()),
    calendar_repo: CalendarRepository = Depends(get_repository(CalendarRepository)),
) -> JSONResponse:
    # Get the last user message from the conversation
    user_messages = [msg.text for msg in body.messages if msg.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message provided.")

    question = user_messages[-1]

    query_embedding = get_embedding(question)
    context = await calendar_repo.get_relevant_context(query_embedding, user_id=user.id)
    try:
        answer = ask_gpt_with_context(question, context)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    # 4. Respond to DeepChat format
    return JSONResponse(
        content={
            "text": answer,
                "html": (
                    '<div class="deep-chat-temporary-message">'
                    '<button class="add-to-briefing-book-btn" '
                    'style="margin-top: 6px">Add to Briefing Book?</button>'
                    '</div>'
                )
        }
    )