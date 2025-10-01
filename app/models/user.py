from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Location(BaseModel):
    Unit:int

class User(BaseModel):
    firstName:str
    lastName:str
    Email: str
    AlternateEmail:Optional[str]
    PhoneNumber:Optional[str]
    PrimaryRole: Optional[UUID]
    password: str
    locations:Optional[List[Location]]
    
class UserInfo(BaseModel):
    user_id:str
    firstName:str
    lastName:str
    businessUnit:Optional[str]
    PhoneNumber:Optional[str]
    AlternateEmail:Optional[str]
    userRole:Optional[str]
    IsLocked:bool
    IsActive:bool   
    IsLocked:bool 
    password_salt: str
    password_hash: str
    
class UserDetail(BaseModel):
    user_id:str
    firstName:str
    lastName:str
    businessUnit:Optional[str]
    PhoneNumber:Optional[str]
    AlternateEmail:Optional[str]
    userRole:Optional[str]
    userName:str  
    isActive: bool
    IsLocked:bool

class DashboardCards(BaseModel):
    Id:str
    redirectionLink:str
    imgWidth:int
    CardImage:str
    ImageName:str
    ImageExt:str
    Heading:str
    SubHeading:str  
    Order: int
    LoginType:str
    AppCategory:str
    MimeType:str
    IsNewTab:bool
    
class userClaims(BaseModel):
    firstName:str
    lastName:str
    userName:str
    userRole:str
    user_id:str
    businessUnit:Optional[str]
    PhoneNumber:Optional[str]
    AlternateEmail:Optional[str]
    exp:datetime
    
class EncryptPassword(BaseModel):
    salt:str
    hash:str

class UserCred(BaseModel):
    userName:str
    Password:str

class UserList(BaseModel):
    id:str
    createdOn:str
    userName:str
    firstName:str
    lastName:str
    franchiseeId:Optional[int]
    franchiseeName:Optional[str]
    isActive:bool
    isLocked:bool
    lastLoginDate:Optional[str]
    securityGroupName:Optional[str]
    isDeleted:bool

class UserHeirarchy(BaseModel):
    id:str
    userName:str
    firstName:str
    lastName:str

class AssignableRole(BaseModel):
    ID:str
    Name:str

class DeleteUsers(BaseModel):
    UserId:UUID

class UpdateUser(BaseModel):
    UserId:UUID
    firstName:str
    lastName:str
    AlternateEmail:Optional[str]
    IsActive:bool
    PhoneNumber:Optional[str]
    PrimaryRole: UUID
    locations:Optional[List[Location]]
    
class DashboardCardOrder(BaseModel):
    DashboardCardId:UUID
    Ordinal:int

class UserAccess(BaseModel):
    AppName:str
    EntityName:str
    CanRead:bool
    CanCreate:bool
    CanUpdate:bool
    CanDelete:bool
    NumberOfDays:Optional[int]
    ModuleName:str
    ModuleDescription:str
    EntityDescription:str
    DisplayOrder:int
    
class AssignableRestaurant(BaseModel):
    unit:int
    street:Optional[str]
    brand:Optional[str]

class UserInormation(BaseModel):
    user_id:str
    firstName:str
    lastName:str
    businessUnit:Optional[str]
    PhoneNumber:Optional[str]
    AlternateEmail:Optional[str]
    isActive: bool
    userName:str
    IsLocked:bool
    PrimaryRoleId:Optional[str]
    restaurants:Optional[List[AssignableRestaurant]]