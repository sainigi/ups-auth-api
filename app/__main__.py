import os
from fastapi import FastAPI
import uvicorn
from app import accountAPI,userManagementAPI,roleManagementAPI,healthCheckAPI,entityManagementAPI
from fastapi.middleware.cors import CORSMiddleware

host = os.environ["host_name"]
port = os.environ["port_no"]
if __name__ == '__main__':
    description = """
    ## Auth API
    """
    tags_metadata = [
        {
            "name": "Auth API",
        },
    ]
    
    app = FastAPI(
    title="Auth API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    
    app.include_router(healthCheckAPI.router)
    app.include_router(accountAPI.router)
    app.include_router(userManagementAPI.router)
    app.include_router(roleManagementAPI.router)
    app.include_router(entityManagementAPI.router)
    
    uvicorn.run(app, host=host, port=int(port))
