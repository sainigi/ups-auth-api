import logging
from uuid import UUID
import pyodbc
from typing import Dict,List
from fastapi import status, Depends,APIRouter
from fastapi.responses import JSONResponse
from app.models.common import Status
from app.models.user import User,DeleteUsers,UpdateUser,DashboardCardOrder
from app.services.userManagementService import hash_password,CreateUserHelper,\
    GetUserListHelper,GetAssignableRoleHelper,DeleteUserHelper,UpdateUserHelper,\
        GetAssignableLocationsHelper,GetUserInformationHelper,ChangeBulkRoleHelper,\
            UpdateUserDashboardCardOrderHelper,LockUnlockUserHelper,ActivateDeactivateUserHelper,\
                GetUserHeirarchyHelper
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/usermanagement",
    tags=["UserManagement"],
    responses={404: {"description": "Not found"}},
)

@router.post('/createuser', responses=responses("422", "500"))
async def CreateUser(body: User, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Create-User Request : {body.dict()}..., PayLoad {token}')

        response = await hash_password(body.password)
        await CreateUserHelper(user= body,
                               password_salt=response.salt,
                               password_hash=response.hash,
                               CreatedBy=token["user_id"]
                               )
        logger.debug(f'Create-User Response : {response}...')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=Status(Status= "User created Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while saving user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while saving user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetUserList', responses=responses("422", "500"))
async def GetUserList(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-User-List Request : PayLoad {token}')
        userInfo = await GetUserListHelper()        
        logger.debug(f'Get-User-List Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user List : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user List : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetUserHeirarchy', responses=responses("422", "500"))
async def GetUserHeirarchy(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetUserHeirarchy Request : PayLoad {token}')
        userInfo = await GetUserHeirarchyHelper(token["userName"])        
        logger.debug(f'GetUserHeirarchy Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user Heirarchy : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user Heirarchy : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetAssignableRole', responses=responses("422", "500"))
async def GetAssignableRole(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetAssignableRole Request : PayLoad {token}')
        userInfo = await GetAssignableRoleHelper(userId=token['user_id'])        
        logger.debug(f'GetAssignableRole Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get AssignableRole List : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get AssignableRole List : {ex!r}')
        return GetJSONResponse(500, ex)

@router.delete('/deleteusers', responses=responses("422", "500"))
async def DeleteUser(body: List[DeleteUsers], token: Dict = Depends(validate_token)):
    try:
        await DeleteUserHelper(user= body,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "User Deleted Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Delete user : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Delete user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/updateuser', responses=responses("422", "500"))
async def UpdateUserData(body: UpdateUser, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Update-User Request : {body.dict()}..., PayLoad {token}')

        await UpdateUserHelper(user= body,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "User Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Update user : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Update user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetAssignableLocations', responses=responses("422", "500"))
async def GetAssignableLocations(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetAssignableLocations Request : PayLoad {token}')
        userInfo = await GetAssignableLocationsHelper(userId=token['user_id'])        
        logger.debug(f'GetAssignableLocations Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get AssignableLocations List : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get AssignableLocations List : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetUserDetails', responses=responses("422", "500"))
async def GetUserDetail(userId:UUID,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-User-Details Request : PayLoad {token}')
        userInfo = await GetUserInformationHelper(userId=userId)        
        logger.debug(f'Get-User-Details Response : {userInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.patch('/changebulkrole', responses=responses("422", "500"))
async def ChangeBulkRole(SecurityGroupId:UUID,body: List[DeleteUsers], token: Dict = Depends(validate_token)):
    try:
        await ChangeBulkRoleHelper(user= body,
                               CreatedBy=token["user_id"],SecurityGroupId=SecurityGroupId
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Role Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating role : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating role : {ex!r}')
        return GetJSONResponse(500, ex)

@router.patch('/ChangeDashboardCardOrder', responses=responses("422", "500"))
async def ChangeDashboardCardOrder(body: List[DashboardCardOrder], token: Dict = Depends(validate_token)):
    try:
        await UpdateUserDashboardCardOrderHelper(dashboardCards=body,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Dashboard Card order Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating Dashboard Card order : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating Dashboard Card order : {ex!r}')
        return GetJSONResponse(500, ex)

@router.patch('/lockunlockusers', responses=responses("422", "500"))
async def LockUnlockUser(isLocked:bool,body: List[DeleteUsers], token: Dict = Depends(validate_token)):
    try:
        await LockUnlockUserHelper(user= body,
                                   isLocked=isLocked,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "User Locked / Unlocked Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Locked / Unlocked user : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Locked / Unlocked user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.patch('/activatedeactivateusers', responses=responses("422", "500"))
async def ActivateDeactivateUser(isActive:bool,body: List[DeleteUsers], token: Dict = Depends(validate_token)):
    try:
        await ActivateDeactivateUserHelper(user= body,
                                   isActive=isActive,
                               CreatedBy=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "User Activate / Deactivate Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Activate / Deactivate user : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Activate / Deactivate user information : {ex!r}')
        return GetJSONResponse(500, ex)