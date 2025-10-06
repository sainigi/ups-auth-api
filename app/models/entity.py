from typing import Optional
from pydantic import BaseModel,HttpUrl
from uuid import UUID
from typing import List

class GetDashboardCardImageModel(BaseModel):
    ID:int
    DashboardCardId:UUID
    CardImage: str = None 
    ImageName: str
    MimeType: str 

class GetDashboardCardModel(BaseModel):
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
    dashboardCardImage: Optional[GetDashboardCardImageModel]


class GetEntityModel(BaseModel):
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
    card: Optional[GetDashboardCardModel]

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



#READ
class EntityResponse(GetEntityModel):
    EntityId: UUID
    CreatedBy: str
    CreatedOn: str
    ModifiedBy: Optional[str] = None
    ModifiedOn: Optional[str] = None
    ApplicablePrivileges: str = "RECD"

#UPDATE
class UpdateEntityModel(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    IsActive: Optional[bool] = None
    ModuleName: Optional[str] = None
    ModuleDescription: Optional[str] = None
    DisplayOrder: Optional[int] = None
    dashboard_card: Optional[GetDashboardCardModel] = None
    ApplicablePrivileges: str = "RECD"

#DELETE
class DeleteEntity(BaseModel):
    pass  # No fields,will get ID from query string

    