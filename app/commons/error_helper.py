from fastapi import status
from fastapi.responses import JSONResponse
import http

from app.models.common import errorMsg

status_codes = {
    "401": {
        "description": "Unauthorized Error",
        "model": errorMsg
    },
    "422": {
        "description": "Validation Error",
        "model": errorMsg
    },
    "500": {
        "description": "Internal Server Error",
        "model": errorMsg
    },
    "503": {
        "description": "Service Unavailable",
        "model": errorMsg
    },
    "409": {
        "description": "Conflict",
        "model": errorMsg
    },
    "400": {
        "description": "Bad Request",
        "model": errorMsg
    },
    "404": {
        "description": "Not Found",
        "model": errorMsg
    },
    "202": {
        "description": "Accepted",
        "model": errorMsg
    },

}

db_errors = [ "No Access on Entity", "No Access on to RestId / GroupId" ]
db_unauthorized = "No Access on Entity"

def responses(*response_status_codes):
    global status_codes
    return {codes: status_codes[codes] for codes in response_status_codes}

def GetJSONResponse(status_code, ex):
    try:
        status_code = int(status_code)
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            ex = http.client.responses[status_code]
        error_msg = errorMsg(Error=str(status_code), Message=http.client.responses[status_code], Detail=str(ex))
        return JSONResponse(status_code=status_code, content=error_msg.dict())
    except:
        raise
