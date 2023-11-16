from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

M = TypeVar("M", bound=BaseModel)


class Server(BaseModel):
    ip: str = ''
    server_id: str = ''
    server_name: str = ''
    
class Reponse(GenericModel, Generic[M]):
    data: M
    status: str = "success"

class ListReponse(GenericModel, Generic[M]):
    data: List[M]
    status: str = "success"