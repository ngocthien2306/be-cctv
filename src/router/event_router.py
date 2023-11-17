from fastapi import APIRouter

from utils import model
from utils.socket import socket_connection
from services.event_service import write_log, write_video_log

router = APIRouter(prefix="/event")

@router.post("")
async def post_event(event: model.Event):
    await socket_connection.send_data(
        channel="alert",
        data=event.dict()
    )
    # write_log(event)
    return "success"

@router.post('/video')
async def save_log(event: model.EventVideo):
    event = write_video_log(event)
    return event


