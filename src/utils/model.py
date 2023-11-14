from pydantic import BaseModel

class Event(BaseModel):
    camera_id: str
    module_id: str
    timestamp: int
    image_uri: str
    msgType: int

class EventLog(Event):
    set_false: bool = False
    line: int = 2
    shift: int = 1

class History(EventLog):
    id: str

class Filter(BaseModel):
    page: int = 0
    size: int = 10
    module_id: str = None
    camera_id: str = None
    shift: int = None
    line: int = None 
    start_timestamp: int = 0
    end_timestamp: int = 0

class ReportEvent(BaseModel):
    id: str