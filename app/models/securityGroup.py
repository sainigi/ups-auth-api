from enum import Enum
from uuid import UUID
from pydantic import BaseModel, validator
from typing import Optional, List
from app.commons.utils import isValidUUID
from datetime import datetime

class EntityPermission(BaseModel):
    Entity_Id:str
    CanCreate:bool
    CanDelete:bool
    CanUpdate:bool
    CanRead:bool
    NumberOfDays:Optional[int]
    IsAutoAccept:bool
    IsCorporateOnly:bool
    

class SecurityGroup(BaseModel):
    Name:str
    Description:str
    AllowFZUsage: bool
    IsActive:bool
    Hierarchy:int
    AutoApplyToNewFranchisee: bool
    Permissions: Optional[List[EntityPermission]]
    ExpiresOn:Optional[datetime]
    
class SecurityGroupList(BaseModel):
    Id:str
    Name:str
    Description:str
    IsTempRole:bool
    AllowFZUsage:bool
    ParentRoleId:Optional[str]
    IsActive:bool
    CreatedOn:str
    CreatedBy:str
    UpdatedOn:Optional[str]
    UpdatedBy:Optional[str]
    IsRoleEditable:bool
    Hierarchy:int
    
class AssignablePermission(BaseModel):
    ModuleName:str
    ModuleDescription:str
    EntityId:str
    EntityName:str
    EntityDescription:str
    DisplayOrder:int
    ConfigureNumberOfDays:int
    IsAutoAccept:bool
    AutoAcceptType:Optional[str]
    IsCorporteOnly:bool
    ApplicationPrivileges:str
    MaxDays:int

class UpdateSecurityGroup(BaseModel):
    SecurityGroup_Id:UUID
    Name:str
    Description:str
    AllowFZUsage: bool
    IsActive:bool
    Hierarchy:int
    Permissions: Optional[List[EntityPermission]]
    ExpiresOn:Optional[datetime]
    AutoApplyToNewFranchisee: Optional[bool]

class SecurityGroupPermission(BaseModel):
    EntityId:str
    EntityName:str
    EntityDescription:str
    ModuleName:str
    ModuleDescription:str    
    DisplayOrder:int
    CanRead:bool
    CanCreate:bool
    CanUpdate:bool
    CanDelete:bool
    NumberOfDays:Optional[int]
    MaxDays:int
    IsAutoAccept:bool
    AutoAcceptType:Optional[str]    
    ApplicationPrivileges:str
    IsCorporteOnly:bool

class SecurityGroupDetail(BaseModel):
    Role_Id:str
    RoleName:str
    RoleDescription:str
    RoleTitle:Optional[str]
    ExpiresOn:Optional[str]    
    IsTempRole:bool
    AllowFZUsage:bool
    AutoApplyToNewFranchisee:bool
    ParentRoleId:Optional[str]
    IsActive:bool
    CreatedOn:str
    CreatedBy:str
    UpdatedOn:Optional[str]
    UpdatedBy:Optional[str]
    IsNameEditable:bool
    Hierarchy:int
    securityGroupPermission:List[SecurityGroupPermission]
    
class DeleteSecurityGroups(BaseModel):
    role_Id:UUID