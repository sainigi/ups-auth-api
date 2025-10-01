import logging
from uuid import UUID
import pyodbc
from typing import Dict, List
from fastapi import status, Depends,APIRouter
from fastapi.responses import JSONResponse
from app.models.common import Status
from app.models.securityGroup import SecurityGroup,UpdateSecurityGroup,DeleteSecurityGroups
from app.services.roleManagementService import AddSecurityGroupHelper,GetRoleListHelper,\
    GetAssignablePermissionsHelper,DeleteSecurityGroupHelper,UpdateSecurityGroupHelper,\
        GetCorporateRoleDetailsHelper,ActivateDeactivateRolesHelper
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/rolemanagement",
    tags=["RoleManagement"],
    responses={404: {"description": "Not found"}},
)

@router.post('/AddSecurityGroup', responses=responses("422", "500"))
async def AddSecurityGroup(body: SecurityGroup, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Create-Role Request : {body.dict()}..., PayLoad {token}')
        
        await AddSecurityGroupHelper(securityGroup=body,CreatedBy=token["user_id"])
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=Status(Status= "Security Group created Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while saving role information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while saving role information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetRoleList', responses=responses("422", "500"))
async def GetRoleList(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Role-List Request : PayLoad {token}')
        roleInfo = await GetRoleListHelper()        
        logger.debug(f'Get-Role-List Response : {roleInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=roleInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get Role List : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get Role List : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetAssignablePermissions', responses=responses("422", "500"))
async def GetAssignablePermissions(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'AssignablePermissions Request : PayLoad {token}')
        userInfo = await GetAssignablePermissionsHelper()        
        logger.debug(f'AssignablePermissions Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get AssignablePermissions List : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get AssignablePermissions List : {ex!r}')
        return GetJSONResponse(500, ex)

@router.delete('/DeleteSecurityGroup', responses=responses("422", "500"))
async def DeleteSecurityGroup(SecurityGroupId: UUID, token: Dict = Depends(validate_token)):
    try:
        await DeleteSecurityGroupHelper(securityGroupID=SecurityGroupId,CreatedBy=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Security Group Deleted Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Delete role information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Delete role information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateSecurityGroup', responses=responses("422", "500"))
async def UpdateSecurityGroupData(SecurityGroup: UpdateSecurityGroup, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Update-Role Request : {SecurityGroup.dict()}..., PayLoad {token}')
        
        await UpdateSecurityGroupHelper(securityGroup=SecurityGroup,CreatedBy=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Security Group Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Update role information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Update role information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/getSecurityGroupDetails', responses=responses("422", "500"))
async def GetSecurityGroupDetails(SecurityGroupId:UUID,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Security-Group-Details Request : PayLoad {token}')
        roleInfo = await GetCorporateRoleDetailsHelper(securityGroupId=SecurityGroupId)        
        logger.debug(f'Get-Security-Group-Details Response : {roleInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=roleInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get-Security-Group-Details : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get-Security-Group-Details : {ex!r}')
        return GetJSONResponse(500, ex)

@router.patch('/activatedeactivateroles', responses=responses("422", "500"))
async def ActivateDeactivateRoles(isActive:bool,body: List[DeleteSecurityGroups], token: Dict = Depends(validate_token)):
    try:
        await ActivateDeactivateRolesHelper(roles= body,
                                   isActive=isActive,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Role Activate / Deactivate Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Activate / Deactivate role : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Activate / Deactivate role information : {ex!r}')
        return GetJSONResponse(500, ex)