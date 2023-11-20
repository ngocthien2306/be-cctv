from fastapi import APIRouter, HTTPException, Request
from utils.models.server_model import *
from services.server_service import server_service
from services.camera_service import camera_service
from utils.socket import SocketIOClient
import threading
from utils.plc_controller import *
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
        print(camera)
        if camera is not None:
            server = server_service.get_by_id(camera['server_id'])
        else:
            raise HTTPException(
            status_code=400,
            detail='Camera ID is not existed'
        )  
        
        print(server)
        if server is not None:
            client_socket = SocketIOClient(f"http://{server['ip']}:5000")
            print('socket')
            client_socket.send_alarm(model.dict())
            
            def call_client_by_ip():
                print('Starting connect Socket')
                
                client_socket = SocketIOClient(f"http://{server['ip']}:5000")
                client_socket.send_alarm(model.dict())
                
                
            def connect_plc():
                print('Starting connect PLC')
                
                variables = [8212] # 8222, 8192, 8193, 8194, 8195, 8196, 8197] #, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209]
                
                list_config = {}
                for var in variables: 
                    plc_controller_config = PLCControllerConfig(
                        plc_ip_address="192.168.1.250",
                        plc_port=502,
                        plc_address=1,
                        modbus_address=var
                    )
                    _plc_controller = PLCController(plc_controller_config)
                    list_config[var] = _plc_controller
                    

                # res1 = list_config[8212].turn_on()
                
                # res2 = list_config[8212].turn_off()
            
            
            background_thread = threading.Thread(target=connect_plc)
            background_thread.start()
            background_thread = threading.Thread(target=call_client_by_ip)
            background_thread.start()

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
