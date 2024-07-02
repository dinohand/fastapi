from pydantic import BaseModel
from typing import Optional

class MEMB_M(BaseModel):
    USER : str
    USER_PW : Optional[str] | None = None
    
class DICT_M(BaseModel):
    KEY: Optional[str] | None= None
    VALUE: Optional[str] | None= None
    
    