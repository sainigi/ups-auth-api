from typing import List
from uuid import UUID
from app.models.securityGroup import SecurityGroup,SecurityGroupList,AssignablePermission,\
    UpdateSecurityGroup,SecurityGroupDetail,SecurityGroupPermission,DeleteSecurityGroups
from app.commons.sp_helper import exec_stored_procedure,exec_stored_procedure_multiple_sets
from app.commons.utils import stringify_dt
import logging

logger = logging.getLogger()

async def AddSecurityGroupHelper(securityGroup:SecurityGroup,CreatedBy:UUID):
    try:
        logger.debug(f'data: {securityGroup}')
        TabVar = []
        for permi in securityGroup.Permissions:
            TabVar.append((permi.Entity_Id,permi.CanRead,permi.CanUpdate,permi.CanCreate,
                           permi.CanDelete,permi.NumberOfDays,permi.IsAutoAccept,
                           'CORP',permi.IsCorporateOnly))
            
        await exec_stored_procedure(sp_name= "CreateCorporateRole",
                                           param_names=["UserId","Name","Description","AllowFZUsage",
                                                        "IsActive","Hierarchy","AutoApplyToNewFranchisee",
                                                        "Permissions","ExpiresOn"],
                                            param_values=[CreatedBy,
                                                   securityGroup.Name,
                                                   securityGroup.Description,
                                                   securityGroup.AllowFZUsage,
                                                   securityGroup.IsActive,
                                                   securityGroup.Hierarchy,
                                                   securityGroup.AutoApplyToNewFranchisee,
                                                   TabVar,
                                                   securityGroup.ExpiresOn
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetRoleListHelper():
    try:
        resp = await exec_stored_procedure(sp_name= "GetCorporateRoleList",
                                           param_names=[],
                                     param_values=[],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for role in resp:
            data.append(SecurityGroupList(Id=role[0],
                                 Name=role[1],
                                 Description=role[2],
                                 IsTempRole=role[3],
                                 AllowFZUsage=role[4],
                                 ParentRoleId=role[5],
                                 IsActive=role[6],
                                 CreatedOn=stringify_dt(role[7]),
                                 CreatedBy=role[8],
                                 UpdatedOn=stringify_dt(role[9]) if role[9] else role[9],
                                 UpdatedBy=role[10],
                                 IsRoleEditable=role[11],
                                 Hierarchy=role[12]).dict())
        return data

    except Exception as ex:
        raise

async def GetAssignablePermissionsHelper():
    try:
        resp = await exec_stored_procedure(sp_name= "GetAssignablePermissions",
                                           param_names=[],
                                     param_values=[],
                                     fetch_data=True)
        data =[]
        logger.debug(f'{resp}')
        for rl in resp:
            data.append(AssignablePermission(ModuleName=rl[0],
                                             ModuleDescription=rl[1],
                                             EntityId=rl[2],
                                             EntityName=rl[3],
                                             EntityDescription=rl[4],
                                             DisplayOrder=rl[5],
                                             ConfigureNumberOfDays=rl[6],
                                             IsAutoAccept=rl[7],
                                             AutoAcceptType=rl[8],
                                             IsCorporteOnly=rl[9],
                                             ApplicationPrivileges=rl[10],
                                             MaxDays=rl[11]).dict())
        return data

    except Exception as ex:
        raise

async def DeleteSecurityGroupHelper(securityGroupID:str,CreatedBy:UUID):
    try:            
        await exec_stored_procedure(sp_name= "DeleteSecurityGroup",
                                           param_names=["SecurityGroupID","UserID"],
                                            param_values=[securityGroupID,CreatedBy,
                                                   
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def UpdateSecurityGroupHelper(securityGroup:UpdateSecurityGroup,CreatedBy:UUID):
    try:
        logger.debug(f'data: {securityGroup}')
        TabVar = []
        for permi in securityGroup.Permissions:
            TabVar.append((permi.Entity_Id,permi.CanRead,permi.CanUpdate,permi.CanCreate,
                           permi.CanDelete,permi.NumberOfDays,permi.IsAutoAccept,
                           'CORP',permi.IsCorporateOnly))
        await exec_stored_procedure(sp_name= "UpdateCorporateRole",
                                           param_names=["UserId","SecurityGroup_Id","Name","Description",
                                                        "AllowFZUsage","IsActive","Hierarchy",
                                                        "Permissions","ExpiresOn","AutoApplyToNewFranchisee"],
                                            param_values=[CreatedBy,
                                                   securityGroup.SecurityGroup_Id,
                                                   securityGroup.Name,
                                                   securityGroup.Description,
                                                   securityGroup.AllowFZUsage,
                                                   securityGroup.IsActive,
                                                   securityGroup.Hierarchy,
                                                   TabVar,
                                                   securityGroup.ExpiresOn,
                                                   securityGroup.AutoApplyToNewFranchisee,
                                                   ],
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetCorporateRoleDetailsHelper(securityGroupId:UUID):
    try:
        securityGroup,permissions = await exec_stored_procedure_multiple_sets(sp_name= "GetCorporateRoleDetail",
                                           param_names=["SecurityGroup_Id"],
                                     param_values=[securityGroupId],
                                     fetch_data=True)
        perData = []
        SGData = None
        logger.debug(f'{securityGroup}')
        logger.debug(f'{permissions}')
        if len(securityGroup)>0:
            for perm in permissions:
                perData.append(SecurityGroupPermission(EntityId=perm[0],
                                                    EntityName=perm[1],
                                                    EntityDescription=perm[2],
                                                    ModuleName=perm[3],
                                                    ModuleDescription=perm[4],
                                                    DisplayOrder=perm[5],
                                                    CanRead=perm[6],
                                                    CanUpdate=perm[7],
                                                    CanCreate=perm[8],
                                                    CanDelete=perm[9],
                                                    NumberOfDays=perm[10],
                                                    MaxDays=perm[11],
                                                    IsAutoAccept=perm[12],
                                                    AutoAcceptType=perm[13],
                                                    ApplicationPrivileges=perm[14],
                                                    IsCorporteOnly=perm[15],
                                                    ).dict())
            
            SGData =(SecurityGroupDetail(Role_Id=securityGroup[0][0],
                                        RoleName=securityGroup[0][1],
                                        RoleDescription=securityGroup[0][2],
                                        RoleTitle=securityGroup[0][3],
                                        ExpiresOn= stringify_dt(securityGroup[0][4]) if securityGroup[0][4] else securityGroup[0][4],
                                        IsTempRole=securityGroup[0][5],
                                        AllowFZUsage=securityGroup[0][6],
                                        AutoApplyToNewFranchisee=securityGroup[0][7],
                                        ParentRoleId=securityGroup[0][8],
                                        IsActive=securityGroup[0][9],
                                        CreatedOn= stringify_dt(securityGroup[0][10]) if securityGroup[0][10] else securityGroup[0][10],
                                        CreatedBy=securityGroup[0][11],
                                        UpdatedOn=stringify_dt(securityGroup[0][12]) if securityGroup[0][12] else securityGroup[0][12],
                                        UpdatedBy=securityGroup[0][13],
                                        IsNameEditable=securityGroup[0][14],
                                        Hierarchy=securityGroup[0][15],
                                        securityGroupPermission=perData,
                                        ).dict())
        return SGData

    except Exception as ex:
        raise

async def ActivateDeactivateRolesHelper(isActive:bool, roles:List[DeleteSecurityGroups],CreatedBy:UUID):
    try:
        TabVar = []
        for rest in roles:
            TabVar.append((rest.role_Id,))
            
        await exec_stored_procedure(sp_name= "ActivateDeactiveCorporateRole",
                                           param_names=["UserId","IsActive","SecurityGroup_Ids"],
                                            param_values=[CreatedBy,isActive,TabVar],
                                            fetch_data=False)
    except Exception as ex:
        raise