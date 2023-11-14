from fastapi import APIRouter

from src.utils import model
from src.utils.socket import socket_connection
from src.services.event_service import write_log

router = APIRouter(prefix="/event")

@router.post("")
async def post_event(event: model.Event):
    await socket_connection.send_data(
        channel="alert",
        data=event.dict()
    )
    write_log(event)
    return "success"
