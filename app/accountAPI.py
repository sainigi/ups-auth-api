from datetime import datetime, timedelta, timezone
import logging
import pyodbc
from typing import Dict
from fastapi import status,  Depends,APIRouter
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from app.commons import auth
from app.models.common import Status
from app.models.user import UserCred,userClaims
from app.services.accountService import verify_password,GetUserInfo,UpdateLoginStatusHelper,\
    GetUserAccessHelper,GetUserDetails,GetDashboardCardsHelper
from app.commons.error_helper import responses, GetJSONResponse,  db_unauthorized
from app.commons.jwt_auth import generate_Token,validate_token,validate_corp_token
import os

logger = logging.getLogger()
allowedDomainName = os.environ["Entra_Id_Domain_Name"]
tenant_id = os.environ["tenant_id"]

router = APIRouter(
    prefix="/account",
    tags=["Account"],
    responses={404: {"description": "Not found"}},
)

@router.post('/login', responses=responses("422", "500"))
async def Login(credentials: UserCred, Authorization: APIKey = Depends(auth.get_api_key)):
    try:
        logger.debug(f'Get-User Request : {credentials}...')
        userInfo = await GetUserInfo(user_Name=credentials.userName)
        
        if(userInfo == None):
            response = False
        else:
            response = True
            isValidCredentials = await verify_password(credentials.Password,userInfo.password_hash)
        
        if(response == True and isValidCredentials == True and userInfo.IsActive == True and userInfo.IsLocked == False):
            await UpdateLoginStatusHelper(credentials.userName,isValidCredentials)
            claims = userClaims(firstName=userInfo.firstName,
                       lastName=userInfo.lastName,
                       userName=credentials.userName,
                       userRole=userInfo.userRole,
                       user_id=userInfo.user_id,
                       businessUnit=userInfo.businessUnit,
                       PhoneNumber=userInfo.PhoneNumber,
                       AlternateEmail=userInfo.AlternateEmail,
                       exp= datetime.now(timezone.utc) + timedelta(minutes=30)).dict()
            logger.debug(f'Get-Userinfo Response : {claims}...')
            token = await generate_Token(claims)
        elif(response == True and isValidCredentials == False):
            await UpdateLoginStatusHelper(credentials.userName,isValidCredentials)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "Invalid user credentials.").dict())
        elif(response == True and userInfo.IsActive == False):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "User is Inactive.").dict())
        elif(response == True and userInfo.IsLocked == True):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "User is Locked.").dict())
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "Invalid user credentials.").dict())

        logger.debug(f'Get-User Response : {token}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/corplogin', responses=responses("422", "500"))
async def CorpLogin(token: Dict = Depends(validate_corp_token)):
    try:
        domain_name = str(token['unique_name']).split('@')[1]
        logger.debug(f'Corp-Login Request : PayLoad {token}')
        userInfo = await GetUserInfo(user_Name=token['unique_name'])        
        if(userInfo == None):
            response = False
        else:
            response = True
            if domain_name == allowedDomainName and tenant_id == token['tid']:
                isValidCredentials = True
        
        if(response == True and isValidCredentials == True and userInfo.IsActive == True and userInfo.IsLocked == False):
            await UpdateLoginStatusHelper(token['unique_name'],isValidCredentials)
            claims = userClaims(firstName=userInfo.firstName,
                       lastName=userInfo.lastName,
                       userName=token['unique_name'],
                       userRole=userInfo.userRole,
                       user_id=userInfo.user_id,
                       businessUnit=userInfo.businessUnit,
                       PhoneNumber=userInfo.PhoneNumber,
                       AlternateEmail=userInfo.AlternateEmail,
                       exp= datetime.now(timezone.utc) + timedelta(minutes=30)).dict()
            logger.debug(f'Get-Userinfo Response : {claims}...')
            newToken = await generate_Token(claims)
        elif(response == True and isValidCredentials == False):
            await UpdateLoginStatusHelper(token['unique_name'],isValidCredentials)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "Invalid user credentials.").dict())
        elif(response == True and userInfo.IsActive == False):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "User is Inactive.").dict())
        elif(response == True and userInfo.IsLocked == True):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "User is Locked.").dict())
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=Status(Status= "Invalid user credentials.").dict())

        logger.debug(f'Get-User Response : {token}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=newToken)

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/refreshtoken', responses=responses("422", "500"))
async def refreshToken(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Create-User Request : PayLoad {token}')
        claims = userClaims(firstName=token['firstName'],
                    lastName=token['lastName'],
                    userName=token['userName'],
                    userRole=token['userRole'],
                    businessUnit=token['businessUnit'],
                    PhoneNumber=token['PhoneNumber'],
                    AlternateEmail=token['AlternateEmail'],
                    user_id=token['user_id'],
                    exp= datetime.now(timezone.utc) + timedelta(minutes=30)).dict()
        logger.debug(f'Get-Userinfo Response : {claims}...')
        token = await generate_Token(claims)
            
        logger.debug(f'Get-User Response : {token}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user information : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetUserAccess', responses=responses("422", "500"))
async def GetUserAccess(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetUserAccess Request : PayLoad {token}')
        roleInfo = await GetUserAccessHelper(userId=token['user_id'])        
        logger.debug(f'GetUserAccess Response : {roleInfo}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=roleInfo)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while GetUserAccess : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while GetUserAccess : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetUserDetails', responses=responses("422", "500"))
async def GetUserDetail(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-User-Details Request : PayLoad {token}')
        userInfo = await GetUserDetails(user_Name=token['userName'])        
        logger.debug(f'Get-User-Details Response : {userInfo.dict()}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=userInfo.dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user information : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user information : {ex!r}')
        return GetJSONResponse(500, ex)


@router.get('/GetUserDashboardCards', responses=responses("422", "500"))
async def GetUserDashboardCards(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Dashboard-Cards Request : PayLoad {token}')
        cards = await GetDashboardCardsHelper(user_Name=token['userName'])        
        logger.debug(f'Get-Dashboard-Cards Response : {cards}...')
        return JSONResponse(status_code=status.HTTP_200_OK, content=cards)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while Get user access Dashboard Card : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while Get user access Dashboard Card : {ex!r}')
        return GetJSONResponse(500, ex)