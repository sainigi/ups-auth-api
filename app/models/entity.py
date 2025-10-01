from typing import Optional
from pydantic import BaseModel,HttpUrl
from uuid import UUID
from typing import List


#CREATE
class DashboardCard(BaseModel):
    CardId: UUID
    Heading: str
    Subheading: Optional[str] = None
    AddressURL: Optional[str] = None
    imgWidth: Optional[int] = None
    LoginType: Optional[str] = None
    IsNewTab: Optional[bool] = None
    AppCategory: Optional[str] = None
    ImageName: Optional[str] = None
    CardImage: Optional[str] = None
    MimeType: Optional[str] = None
    Ordinal: Optional[int] = 0  

class Entity(BaseModel):
    Name: str
    Description: str
    IsActive: bool
    ModuleName: str
    ModuleDescription: str
    DisplayOrder: Optional[int] = None
    dashboard_card: Optional[DashboardCard] = None
    ApplicablePrivileges: Optional[str] = None 
    # ApplicablePrivileges will be hardcoded as RECD in  stored procedure


#READ
class EntityResponse(Entity):
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
    dashboard_card: Optional[DashboardCard] = None
    ApplicablePrivileges: str = "RECD"

#DELETE
class DeleteEntity(BaseModel):
    pass  # No fields,will get ID from query string

    