from fastapi import APIRouter, HTTPException, Request
from utils.models.server_model import *
from services.server_service import server_service
from services.camera_service import camera_service
from utils.socket import SocketIOClient

router = APIRouter(prefix="/server")

@router.get("/")
async def get_server():
    records = server_service.get_all()
    return {
        "data": list(records),
        "msg": "success"
    } 
    
@router.post("", response_model=Reponse[Server])
async def add_server(server: Server): 
    try:
        result = server_service.add_server(server)
        
        return {"data": result}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
        
@router.put("", response_model=Reponse[Server])
async def update_server(server: Server): 
    try:
        result = server_service.update_server(server)
        return {"data": result}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/update-ip", response_model=Reponse[Server])
async def update_ip(model: Server):
    try:
        server = server_service.get_by_server_name(model.server_name)
        if server is not None:
            server['ip'] = model.ip
            del server['_id']
            
            server = server_service.update_server(Server(**server))
            return {"data": server}
        else:
            raise HTTPException(
                status_code=400,
                detail='Server ID not exist'
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
       
@router.delete("/{server_id}", response_model=Reponse[object])
async def delete_server(server_id: str):
    try:
        result = server_service.delete_server(server_id)
        return {"data": result}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )      

@router.post('/report')
async def report_camera(model: RequestReport):
    try:
        server = None
        camera = camera_service.get_by_id(model.camera_id)
        if camera is not None:
            server = server_service.get_by_id(camera['server_id'])
        else:
            raise HTTPException(
            status_code=400,
            detail='Camera ID is not existed'
        )  
        
        if server is not None:
            client_socket = SocketIOClient(f"http://{server['ip']}:5000")
            client_socket.send_alarm(model.dict())

        else:
            raise HTTPException(
            status_code=400,
            detail='Server is not existed'
        )  
        
        return {"detail": 'Send alarm successfull', 'status_code': 200}
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )  
