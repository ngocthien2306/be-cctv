from fastapi import APIRouter

from utils import model
from utils.socket import socket_connection
from services.event_service import write_log

router = APIRouter(prefix="/event")

@router.post("")
async def post_event(event: model.Event):
    await socket_connection.send_data(
        channel="alert",
        data=event.dict()
    )
    write_log(event)
    return "success"
