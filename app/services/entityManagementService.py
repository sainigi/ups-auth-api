from uuid import UUID
from app.models.entity import GetEntityModel, UpdateEntityModel, GetDashboardCardModel,GetDashboardCardImageModel,CreateEntityModel
from app.commons.sp_helper import exec_stored_procedure,exec_stored_procedure_multiple_sets
import logging
from typing import List,Optional
from datetime import datetime
from app.commons.utils import stringify_dt,get_varbinary_from_image_string
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger()
#CREATE
async def CreateEntityHelper(entity: CreateEntityModel, CreatedBy: UUID):
    try:
        if entity.card.dashboardCardImage.CardImage:
            CardImage = get_varbinary_from_image_string(entity.card.dashboardCardImage.CardImage)
            
        await exec_stored_procedure(sp_name="usp_Entity_Create",
                                    param_names=[ "Name","Description","CreatedBy","ModuleName","ModuleDescription","ApplicablePrivileges","Heading","Subheading","AddressURL","ImgWidth","LoginType","IsNewTab","AppCategory","ImageName","CardImage","MimeType"],
                                    param_values=[entity.Name,entity.Description,str(CreatedBy),entity.ModuleName,entity.ModuleDescription,entity.ApplicablePrivileges,entity.card.Heading,entity.card.Subheading,entity.card.AddressURL,entity.card.ImgWidth,entity.card.LoginType,entity.card.IsNewTab,entity.card.AppCategory,entity.card.dashboardCardImage.ImageName,CardImage,entity.card.dashboardCardImage.MimeType],
                                    fetch_data=False
                                    )

    except Exception as ex:
        logger.exception(f'Exception in CreateEntityHelper: {ex!r}')
        raise


# READ - Get All Entities
async def GetEntitiesHelper():
    try:
        entities,dashboardCards,dashboardCardImages = await exec_stored_procedure_multiple_sets(sp_name="usp_Entity_GetAll",param_names=[],param_values=[],fetch_data=True)
        
        entities_list = [
            GetEntityModel(
                ID=ent[0],
                Name=ent[1],
                Description=ent[2],
                CreatedOn=stringify_dt(ent[3]),
                CreatedBy=ent[4],
                IsActive=ent[5],
                ModuleName=ent[6],
                ModuleDescription=ent[7],
                DisplayOrder=ent[8],
                IsAutoAccept=ent[9],
                ApplicablePrivileges=ent[10],
            ).dict()
            for ent in entities
        ]

        dashboardCards_list = [
            GetDashboardCardModel(
                ID=dc[0],
                EntityId=dc[1],
                AddressURL=dc[2],
                ImgWidth=dc[3],
                Heading=dc[4],
                Subheading=dc[5],
                Ordinal=dc[6],
                LoginType=dc[7],
                IsNewTab=dc[8],
                AppCategory=dc[9],
            ).dict()
            for dc in dashboardCards
        ]

        dashboardCardImages_list = [
            GetDashboardCardImageModel(
                ID=dci[0],
                DashboardCardId=dci[1],
                CardImage=dci[2],
                ImageName=dci[3],
                MimeType=dci[4],
            ).dict()
            for dci in dashboardCardImages
        ]
        
        
        dci_map = {dci["DashboardCardId"]: dci for dci in dashboardCardImages_list} 
                    
        for card in dashboardCards_list:
            card["dashboardCardImage"] = dci_map.get(card["ID"], None)
        
        cards_by_entity = {}
        for card in dashboardCards_list:
            cards_by_entity.setdefault(card["EntityId"], []).append(card)
                
        for entity in entities_list:
            entity["card"] = cards_by_entity.get(entity["ID"], [])     
        
        logger.debug(f'\n\n\nusp_Entity_GetAll==> Enitites : \n\n{entities_list} \n{type(entities_list)}')
        
        return jsonable_encoder(entities_list)   
        
    except Exception as ex:
        logger.exception(f'Exception in GetEntitiesHelper: {ex!r}')
        raise


# UPDATE - Now accepts entity_id separately from entity data
async def UpdateEntityHelper(entity_id: UUID, entity: UpdateEntityModel, ModifiedBy: UUID):
    """
    Updates an entity. Dashboard card fields are optional.
    """
    try:
        # Prepare parameters for stored procedure
        sp_params = {
            "EntityId": entity_id,
            "Name": entity.Name,
            "Description": entity.Description,
            "ModuleName": entity.ModuleName,
            "ModuleDescription": entity.ModuleDescription,
            "ApplicablePrivileges": getattr(entity, "ApplicablePrivileges", None),
            # Card-related fields optional
            "CardId": None,
            "Heading": None,
            "Subheading": None,
            "AddressURL": None,
            "ImgWidth": None,
            "LoginType": None,
            "IsNewTab": False,
            "AppCategory": None,
            "ImageName": None,
            "MimeType": None
        }

        # Fill dashboard card data only if provided
        if entity.dashboard_card:
            dc = entity.dashboard_card
            sp_params.update({
                "CardId": getattr(dc, "CardId", None),
                "Heading": getattr(dc, "Heading", None),
                "Subheading": getattr(dc, "Subheading", None),
                "AddressURL": str(getattr(dc, "AddressURL", None)),
                "ImgWidth": getattr(dc, "ImgWidth", None),
                "LoginType": getattr(dc, "LoginType", None),
                "IsNewTab": getattr(dc, "IsNewTab", False),
                "AppCategory": getattr(dc, "AppCategory", None),
                "ImageName": getattr(dc, "ImageName", None),
                "MimeType": getattr(dc, "MimeType", None)
            })

        # Call the stored procedure
        await exec_stored_procedure(
            sp_name="MKSIdentity.usp_Entity_Update",
            param_names=[
                "EntityId", "Name", "Description", "ModuleName", "ModuleDescription",
                "ApplicablePrivileges", "Heading", "Subheading",
                "AddressURL", "ImgWidth", "LoginType", "IsNewTab",
                "AppCategory", "ImageName", "MimeType"
            ],
            param_values=[sp_params[key] for key in [
                "EntityId", "Name", "Description", "ModuleName", "ModuleDescription",
                "ApplicablePrivileges", "Heading", "Subheading",
                "AddressURL", "ImgWidth", "LoginType", "IsNewTab",
                "AppCategory", "ImageName", "MimeType"
            ]],
            fetch_data=False
        )

    except Exception as ex:
        logger.exception(f'Exception in UpdateEntityHelper: {ex!r}')
        raise



# DELETE - Now accepts a single entity_id instead of a list
async def DeleteEntitiesHelper(entity_id: UUID, DeletedBy: UUID):
    try:
        await exec_stored_procedure(
            sp_name="MKSIdentity.usp_Entity_Delete",
            param_names=["EntityId", "DeletedBy"],
            param_values=[str(entity_id), str(DeletedBy)],
            fetch_data=False
        )
    except Exception as ex:
        logger.exception(f'Exception in DeleteEntitiesHelper: {ex!r}')
        raise
