from typing import List
from uuid import UUID
from app.models.user import EncryptPassword,User,UserList,AssignableRole,\
    UpdateUser,DeleteUsers,AssignableRestaurant,UserInormation,DashboardCardOrder,UserHeirarchy
from app.commons.sp_helper import exec_stored_procedure,exec_stored_procedure_multiple_sets
from app.commons.utils import stringify_dt
import logging
import bcrypt

logger = logging.getLogger()

# Hash a password using bcrypt
async def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    data = EncryptPassword(salt=salt,hash=hashed_password)
    return data

async def CreateUserHelper(user:User,password_salt:str,password_hash:str,CreatedBy:UUID):
    try:
        TabVar = []
        for rest in user.locations:
            TabVar.append((rest.Unit,))
            
        await exec_stored_procedure(sp_name= "CreateFranchiseeUser",
                                           param_names=["UserId","FirstName","LastName","Email",
                                                        "AlternateEmail","PasswordHash","SecurityStamp",
                                                        "PhoneNumber","PrimaryRole","Locations"],
                                            param_values=[CreatedBy,
                                                   user.firstName,
                                                   user.lastName,
                                                   user.Email,
                                                   user.AlternateEmail,
                                                   password_hash,
                                                   password_salt,
                                                   user.PhoneNumber,
                                                   user.PrimaryRole,
                                                   TabVar
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetUserListHelper():
    try:
        resp = await exec_stored_procedure(sp_name= "GetFranchiseeUsers",
                                           param_names=[],
                                     param_values=[],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for usr in resp:
            data.append(UserList(id=usr[0],
                                 createdOn=stringify_dt(usr[1]),
                                 userName=usr[2],
                                 firstName=usr[3],
                                 lastName=usr[4],
                                 franchiseeId=usr[5],
                                 franchiseeName=usr[6],
                                 isActive=usr[7],
                                 isLocked=usr[8],
                                 lastLoginDate=stringify_dt(usr[9]) if usr[9] else usr[9],
                                 securityGroupName=usr[10],
                                 isDeleted=usr[11]).dict())
        return data

    except Exception as ex:
        raise

async def GetUserHeirarchyHelper(userName:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetUserHeirarchy",
                                           param_names=["UserName"],
                                     param_values=[userName],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for usr in resp:
            data.append(UserHeirarchy(id=usr[0],
                                 userName=usr[3],
                                 firstName=usr[1],
                                 lastName=usr[2]).dict())
        return data

    except Exception as ex:
        raise

async def GetAssignableRoleHelper(userId:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetAssignableRolesForUser",
                                           param_names=["FranchiseeID","UserId"],
                                     param_values=[None,userId],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for rl in resp:
            data.append(AssignableRole(ID=rl[0],
                                 Name=rl[1]).dict())
        return data

    except Exception as ex:
        raise

async def UpdateUserHelper(user:UpdateUser,CreatedBy:UUID):
    try:
        TabVar = []
        for rest in user.locations:
            TabVar.append((rest.Unit,))
            
        await exec_stored_procedure(sp_name= "UpdateFranchiseeUser",
                                           param_names=["CallerUserId","UserId","FirstName","LastName",
                                                        "AlternateEmail","IsActive",
                                                        "PhoneNumber","PrimaryRole","Locations"],
                                            param_values=[CreatedBy,
                                                          user.UserId,
                                                        user.firstName,
                                                        user.lastName,
                                                        user.AlternateEmail,
                                                        user.IsActive,
                                                        user.PhoneNumber,
                                                        user.PrimaryRole,
                                                        TabVar
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def DeleteUserHelper(user:List[DeleteUsers],CreatedBy:UUID):
    try:
        TabVar = []
        for rest in user:
            TabVar.append((rest.UserId,))
            
        await exec_stored_procedure(sp_name= "DeleteUsers",
                                           param_names=["UserId","UsersTable"],
                                            param_values=[CreatedBy,TabVar],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def LockUnlockUserHelper(isLocked:bool, user:List[DeleteUsers],CreatedBy:UUID):
    try:
        TabVar = []
        for rest in user:
            TabVar.append((rest.UserId,))
            
        await exec_stored_procedure(sp_name= "LockUnlockUsers",
                                           param_names=["UserId","IsLocked","UsersTable"],
                                            param_values=[CreatedBy,isLocked,TabVar],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def ActivateDeactivateUserHelper(isActive:bool, user:List[DeleteUsers],CreatedBy:UUID):
    try:
        TabVar = []
        for rest in user:
            TabVar.append((rest.UserId,))
            
        await exec_stored_procedure(sp_name= "ActivateInactivateUsers",
                                           param_names=["UserId","IsActive","UsersTable"],
                                            param_values=[CreatedBy,isActive,TabVar],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetAssignableLocationsHelper(userId:str):
    try:
        resp = await exec_stored_procedure(sp_name= "GetAssignableLocationsForUser",
                                           param_names=["UserId"],
                                     param_values=[userId],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for rl in resp:
            data.append(AssignableRestaurant(unit=rl[0],
                                             street=rl[1]).dict())
        return data

    except Exception as ex:
        raise

async def GetUserInformationHelper(userId:str):
    try:
        userInfo,stores = await exec_stored_procedure_multiple_sets(sp_name= "GetUserInformation",
                                           param_names=["UserID"],
                                     param_values=[userId],
                                     fetch_data=True)
        
        logger.debug(f'{userInfo}')
        logger.debug(f'{stores}')
        storesdata = []
        data = None
        for store in stores:
            storesdata.append(AssignableRestaurant(unit=store[0],
                                                   street=store[1],
                                                   brand=store[2]).dict())
        if len(userInfo) > 0:
            data = UserInormation(user_id = userInfo[0][0],
                                firstName=userInfo[0][1],
                                lastName=userInfo[0][2],
                                businessUnit=userInfo[0][3],
                                PhoneNumber=userInfo[0][4],
                                AlternateEmail=userInfo[0][5],
                                isActive=userInfo[0][6],
                                userName=userInfo[0][7],
                                IsLocked=userInfo[0][8],
                                PrimaryRoleId=userInfo[0][9],
                                restaurants=storesdata
                                ).dict()
        return data

    except Exception as ex:
        raise

async def ChangeBulkRoleHelper(user:List[DeleteUsers],CreatedBy:UUID,SecurityGroupId:UUID):
    try:
        TabVar = []
        for rest in user:
            TabVar.append((rest.UserId,))
            
        await exec_stored_procedure(sp_name= "ChangeUsersRole",
                                           param_names=["UserId","UserIds","SecurityGroupID"],
                                            param_values=[CreatedBy,TabVar,SecurityGroupId],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def UpdateUserDashboardCardOrderHelper(dashboardCards:List[DashboardCardOrder],CreatedBy:UUID):
    try:
        TabVar = []
        for card in dashboardCards:
            TabVar.append((card.DashboardCardId,card.Ordinal))
            
        await exec_stored_procedure(sp_name= "InsertUpdateDashboardCardOrderByUser",
                                           param_names=["UserId","TabVar"],
                                            param_values=[CreatedBy,TabVar],
                                            fetch_data=False)
    except Exception as ex:
        raise