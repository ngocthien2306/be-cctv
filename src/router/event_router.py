from fastapi import APIRouter

from utils import model
from utils.socket import socket_connection
from services.event_service import write_log, write_video_log
from utils.plc_controller import *
import threading

router = APIRouter(prefix="/event")

@router.post("")
async def post_event(event: model.Event):
    await socket_connection.send_data(
        channel="alert",
        data=event.dict()
    )
    
    def connect_plc():
        plc_controller_config = PLCControllerConfig(
                plc_ip_address="192.168.1.250",
                plc_port=502,
                plc_address=1,
                modbus_address=8212
        )
        
        _plc_controller = PLCController(plc_controller_config)
        
        _plc_controller.turn_on()
    
    background_thread = threading.Thread(target=connect_plc)
    background_thread.start()
    # write_log(event)
    return "success"

@router.post('/video')
async def save_log(event: model.EventVideo):
    print(event)
    event = write_video_log(event)
    return event


