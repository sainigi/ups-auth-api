from typing import Optional
from pydantic import BaseModel,HttpUrl
from uuid import UUID
from typing import List

class GetUpdateDashboardCardImageModel(BaseModel):
    ID:Optional[int] = None
    DashboardCardId:Optional[UUID] = None
    CardImage: Optional[str] = None
    ImageName: Optional[str] = None
    MimeType: Optional[str] = None

class GetUpdateDashboardCardModel(BaseModel):
    ID: Optional[UUID] = None
    EntityId: Optional[UUID] = None
    AddressURL: Optional[str] = None
    ImgWidth: Optional[int] = None
    Heading: Optional[str] = None
    Subheading: Optional[str] = None
    Ordinal: Optional[int] = None
    LoginType: Optional[str] = None
    IsNewTab: Optional[bool] = None
    AppCategory: Optional[str] = None
    dashboardCardImage: Optional[GetUpdateDashboardCardImageModel] = None


class GetUpdateEntityModel(BaseModel):
    ID: UUID
    Name: Optional[str]
    Description: Optional[str]
    CreatedOn: Optional[str]
    CreatedBy: Optional[str]
    IsActive: Optional[bool]
    ModuleName: Optional[str]
    ModuleDescription: Optional[str]
    DisplayOrder: Optional[int]
    IsAutoAccept: Optional[bool]
    ApplicablePrivileges: Optional[str] = None
    card: Optional[GetUpdateDashboardCardModel] = None

class CreateDashboardCardImageModel(BaseModel):
    CardImage: Optional[str] 
    ImageName: Optional[str]
    MimeType: Optional[str] 

class CreateDashboardCardModel(BaseModel):
    AddressURL: str
    ImgWidth: Optional[int]
    Heading: str
    Subheading: Optional[str]
    LoginType: Optional[str]
    IsNewTab: bool
    Ordinal: int
    AppCategory: str
    dashboardCardImage: Optional[CreateDashboardCardImageModel]
    
class CreateEntityModel(BaseModel):
    Name: str
    Description: str
    IsActive: bool
    ModuleName: str
    ModuleDescription: str
    DisplayOrder: Optional[int]
    ApplicablePrivileges: str = "RECD"
    card: Optional[CreateDashboardCardModel]


    