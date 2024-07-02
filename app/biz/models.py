from pydantic import BaseModel

class MEMB_M(BaseModel):
    USER : str
    USER_PW : Optional[str] | None = None
    