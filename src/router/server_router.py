from fastapi import APIRouter, HTTPException, Request
from utils.models.server_model import *
from services.server_service import server_service


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
        
