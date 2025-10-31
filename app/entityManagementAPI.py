import logging
import pyodbc
from typing import Dict
from uuid import UUID
from fastapi import status, Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey

from app.models.common import Status
from app.models.entity import CreateEntityModel,GetUpdateEntityModel
from app.services.entityManagementService import (
    CreateEntityHelper, GetEntitiesHelper, 
    UpdateEntityHelper, DeleteEntitiesHelper
)
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token
from app.commons import auth

logger = logging.getLogger()

router = APIRouter(
    prefix="/entitymanagement",
    tags=["EntityManagement"],
    responses={404: {"description": "Not found"}},
)

# ---------------------
# Create Entity
# ---------------------
@router.post('/CreateEntity', responses=responses("422", "500"))
async def CreateEntity(body: CreateEntityModel, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Create-Entity Request : PayLoad {token}')
        logger.debug(f'Payload of Create-Entity: {body}')

        await CreateEntityHelper(entity=body, CreatedBy=token['user_id'])
        
        logger.debug('Create-Entity Response: Entity created successfully')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=Status(Status="Entity created successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Creating Entity : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while creating entity : {ex!r}')
        return GetJSONResponse(500, ex)

# ---------------------
# GET Entities
# ---------------------
@router.get('/GetEntities', responses=responses("422", "500"))
async def GetEntities(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Entities Request : PayLoad {token}')
        result  = await GetEntitiesHelper()

        return JSONResponse(status_code=status.HTTP_200_OK, content=result)

    except pyodbc.Error as ex:
        logger.exception(f'DB Exception while getting entities : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logger.exception(f'Exception while getting entities : {ex!r}')
        return GetJSONResponse(500, ex)
    
# ---------------------
# Update - Update entity by ID from query string
# ---------------------
@router.put('/UpdateEntity', responses=responses("422", "500"))
async def UpdateEntity(entity_id: UUID = Query(..., description="ID of the entity to update"), body: GetUpdateEntityModel = None, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Update-Entity Request : PayLoad {token}')
        logger.debug(f'Update-Entity Request ID: {entity_id}, Body: {body.dict() if body else "{}"}')

        await UpdateEntityHelper(entity_id=entity_id, entity=body, ModifiedBy="user_id")
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status="Entity updated successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating entity : {ex!r}')
        error_msg = str(ex)
        if 'Entity with ID' in error_msg and 'does not exist' in error_msg:
            return GetJSONResponse(404, f"Entity not found: {entity_id}")
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating entity----- : {ex!r}')
        return GetJSONResponse(500, ex)

# ---------------------
# DELETE - Delete entity by ID from query string
# ---------------------
@router.delete('/DeleteEntity', responses=responses("422", "500"))
async def DeleteEntity(entity_id: UUID = Query(..., description="ID of the entity to delete"),token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Delete-Entity Request : PayLoad {token}')
        logger.debug(f'Delete-Entity Request ID: {entity_id}')
        
        await DeleteEntitiesHelper(entity_id=entity_id, DeletedBy=token['user_id'])
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status="Entity deleted successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while deleting entity : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while deleting entity : {ex!r}')
        return GetJSONResponse(500, ex)