from typing import Optional
from pydantic import BaseModel,HttpUrl
from uuid import UUID
from typing import List

class GetUpdateDashboardCardImageModel(BaseModel):
    ID:int
    DashboardCardId:UUID
    CardImage: str = None 
    ImageName: str
    MimeType: str 

class GetUpdateDashboardCardModel(BaseModel):
    ID: UUID
    EntityId: UUID
    AddressURL: str
    ImgWidth: int = None
    Heading: str
    Subheading: str
    Ordinal: int = None
    LoginType: str
    IsNewTab: bool
    AppCategory: str
    dashboardCardImage: Optional[GetUpdateDashboardCardImageModel]


class GetUpdateEntityModel(BaseModel):
    ID: UUID
    Name: str
    Description: str
    CreatedOn: str
    CreatedBy: str
    IsActive: bool
    ModuleName: str
    ModuleDescription: str
    DisplayOrder: int
    IsAutoAccept: bool
    ApplicablePrivileges: str = None
    card: Optional[List[GetUpdateDashboardCardModel]]

class CreateDashboardCardImageModel(BaseModel):
    CardImage: str = None 
    ImageName: str
    MimeType: str 

class CreateDashboardCardModel(BaseModel):
    AddressURL: str
    ImgWidth: int = None
    Heading: str
    Subheading: str
    LoginType: str
    IsNewTab: bool
    AppCategory: str
    dashboardCardImage: Optional[CreateDashboardCardImageModel]
    
class CreateEntityModel(BaseModel):
    Name: str
    Description: str
    CreatedBy: str
    ModuleName: str
    ModuleDescription: str
    ApplicablePrivileges: str = "RECD"
    card: Optional[CreateDashboardCardModel]


    