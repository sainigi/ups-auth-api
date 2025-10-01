from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional, List, Any

from app.commons.utils import isValidUUID

class errorMsg(BaseModel):
    Error: str
    Message: str
    Detail: str

class Action(str, Enum):
    Create = "C"
    Read = "R"
    Update = "U"
    Delete = "D"

class Status(BaseModel):
    Status: Any
