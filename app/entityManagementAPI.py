import logging
import pyodbc
from typing import Dict, List
from uuid import UUID
from fastapi import status, Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from app.models.common import Status
from app.models.entity import Entity,UpdateEntityModel
from app.services.entityManagementService import (
    CreateEntityHelper, GetEntitiesHelper, 
    UpdateEntityHelper, DeleteEntitiesHelper
)
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/entitymanagement",
    tags=["EntityManagement"],
    responses={404: {"description": "Not found"}},
)

# CREATE - Create new entity
@router.post('/createentity', responses=responses("422", "500"))
async def CreateEntity(body: Entity):
    try:
        logger.debug(f'Create-Entity')

        await CreateEntityHelper(
            entity=body,
            CreatedBy="user_id"
        )
        
        logger.debug('Create-Entity Response: Entity created successfully')
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content=Status(Status="Entity created successfully.").dict()
        )

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while creating entity : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while creating entity : {ex!r}')
        return GetJSONResponse(500, ex)

# READ - Get all entities
# @router.get('/getentities', responses=responses("422", "500"))
# async def GetEntities():
#     try:
#         entities = await GetEntitiesHelper()  # list of pyodbc.Row

#         if not entities:
#             return JSONResponse(status_code=status.HTTP_200_OK,content=None)
#         columns = [column[0] for column in entities[0].cursor_description]
#         entities_list = [
#             {
#                 column:(val.isoformat() if isinstance(val,datetime) else val)
#                 for column, val in zip(columns,row)
#             }
#             for row in entities
#         ]
#         logger.debug(f'Get-Entities Response : {entities_list}...')
#         return JSONResponse(status_code=status.HTTP_200_OK, content=entities_list)

#     except pyodbc.Error as ex:
#         logging.exception(f'DB Exception while getting entities : {ex!r}')
#         if db_unauthorized in ex.args[1]:
#             return GetJSONResponse(401, db_unauthorized)
#         return GetJSONResponse(500, ex)

#     except Exception as ex:
#         logging.exception(f'Exception while getting entities : {ex!r}')
#         return GetJSONResponse(500, ex)


@router.get('/getentities', responses=responses("422", "500"))
async def GetEntities():
    try:
        result = await GetEntitiesHelper()

        if not result or not result["entities"]:
            return JSONResponse(status_code=status.HTTP_200_OK, content=None)

        entities_list = result["entities"]
        cards = result["cards"]
        images = result["images"]

        # Merge cards and images into entities
        for entity in entities_list:
            entity_cards = [c for c in cards if c["EntityId"] == entity["EntityId"]]
            for card in entity_cards:
                card_images = [i for i in images if i["CardId"] == card["CardId"]]
                card["images"] = card_images
            entity["dashboard_cards"] = entity_cards

        logger.debug(f'Get-Entities Response : {entities_list}...')

        # Encode datetimes and other non-serializable objects
        entities_json = jsonable_encoder(entities_list)

        return JSONResponse(status_code=status.HTTP_200_OK, content=entities_json)

    except pyodbc.Error as ex:
        logger.exception(f'DB Exception while getting entities : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logger.exception(f'Exception while getting entities : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/updateentity', responses=responses("422", "500"))
async def UpdateEntity(
    entity_id: UUID = Query(..., description="ID of the entity to update"),
    body: UpdateEntityModel = None
):
    try:
        logger.debug(f'Update-Entity Request ID: {entity_id}, Body: {body.dict() if body else "{}"}')

        await UpdateEntityHelper(entity_id=entity_id, entity=body, ModifiedBy="user_id")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=Status(Status="Entity updated successfully.").dict()
        )

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating entity : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating entity : {ex!r}')
        return GetJSONResponse(500, ex)

# ---------------------
# DELETE - Delete entity by ID from query string
# ---------------------
@router.delete('/deleteentities', responses=responses("422", "500"))
async def DeleteEntities(
    entity_id: UUID = Query(..., description="ID of the entity to delete")
):
    try:
        logger.debug(f'Delete-Entity Request ID: {entity_id}')
        
        await DeleteEntitiesHelper(entity_id=entity_id, DeletedBy="user_id")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=Status(Status="Entity deleted successfully.").dict()
        )

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while deleting entity : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while deleting entity : {ex!r}')
        return GetJSONResponse(500, ex)