from uuid import UUID
import bcrypt
from app.models.user import UserInfo,User,UserAccess,UserDetail,DashboardCards
from app.commons.sp_helper import exec_stored_procedure
import logging

logger = logging.getLogger()

# Check if the provided password matches the stored password (hashed)
async def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password.encode('utf-8'))

async def GetUserInfo(user_Name:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetUserDetails",
                                           param_names=["UserName"],
                                     param_values=[user_Name],
                                     fetch_data=True)
        
        logger.debug(f'{resp}')
        data = None
        if len(resp) > 0:
            data = UserInfo(user_id = resp[0][0],
                            firstName=resp[0][1],
                            lastName=resp[0][2],
                            businessUnit=resp[0][3],
                            PhoneNumber=resp[0][4],
                            AlternateEmail=resp[0][5],
                            userRole=resp[0][6],
                            password_hash=resp[0][7],                        
                            password_salt=resp[0][8],
                            IsActive=resp[0][9],
                            IsLocked=resp[0][10])
        return data

    except Exception as ex:
        raise

async def UpdateLoginStatusHelper(UserName:str,IsValidCredentials:bool):
    try:       
        await exec_stored_procedure(sp_name= "UpdateLoginStatus",
                                           param_names=["UserName","IsValidCredentials"],
                                            param_values=[UserName,
                                                   IsValidCredentials
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetUserAccessHelper(userId:UUID):
    try:
        permissions = await exec_stored_procedure(sp_name= "GetRAPUserAccess",
                                           param_names=["UserID"],
                                     param_values=[userId],
                                     fetch_data=True)
        perData = []
        logger.debug(f'{permissions}')        
        for perm in permissions:
            perData.append(UserAccess(AppName=perm[0],
                                                   EntityName=perm[1],
                                                   CanRead=perm[2],
                                                   CanCreate=perm[3],
                                                   CanUpdate=perm[4],
                                                   CanDelete=perm[5],
                                                   NumberOfDays=perm[6],
                                                   ModuleName=perm[7],
                                                   ModuleDescription=perm[8],
                                                   EntityDescription=perm[9],
                                                   DisplayOrder=perm[10]
                                                   ).dict())
        return perData

    except Exception as ex:
        raise
    
async def GetUserDetails(user_Name:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetUserDetails",
                                           param_names=["UserName"],
                                     param_values=[user_Name],
                                     fetch_data=True)
        
        logger.debug(f'{resp}')
        data = None
        if len(resp) > 0:
            data = UserDetail(user_id = resp[0][0],
                                firstName=resp[0][1],
                                lastName=resp[0][2],
                                businessUnit=resp[0][3],
                                PhoneNumber=resp[0][4],
                                AlternateEmail=resp[0][5],
                                userRole=resp[0][6],
                                isActive=resp[0][9],
                                IsLocked=resp[0][10],
                                userName=user_Name)
        return data

    except Exception as ex:
        raise

async def GetDashboardCardsHelper(user_Name:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetDashboardCardByUser",
                                           param_names=["UserName"],
                                     param_values=[user_Name],
                                     fetch_data=True)
        data = []
        for cards in resp:
            data.append(DashboardCards(Id=cards[0],
                                   redirectionLink=cards[1],
                                   imgWidth=cards[2],
                                   CardImage=str(cards[3]),
                                   ImageName=cards[4],
                                   ImageExt=cards[5],
                                   Heading=cards[6],
                                   SubHeading=cards[7],
                                   Order=cards[8],
                                   LoginType=cards[9],
                                   AppCategory=cards[10],
                                   MimeType=cards[11],
                                   IsNewTab=cards[12]
                            ).dict())
        return data

    except Exception as ex:
        raise