from uuid import UUID
from app.models.entity import GetUpdateEntityModel, GetUpdateDashboardCardModel, GetUpdateDashboardCardImageModel, CreateEntityModel
from app.commons.sp_helper import exec_stored_procedure,exec_stored_procedure_multiple_sets
import logging
import base64
from app.commons.utils import stringify_dt
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger()

#CREATE
async def CreateEntityHelper(entity: CreateEntityModel, CreatedBy: UUID):
    try:
        file_binary = None
        image_name = None
        mime_type = None
        if entity.card and entity.card.dashboardCardImage:
            card_image = entity.card.dashboardCardImage
            if card_image.CardImage:
                file_binary = base64.b64decode(card_image.CardImage)
                image_name = card_image.ImageName
                mime_type = card_image.MimeType
    
            
        await exec_stored_procedure(sp_name="[MKSIdentity].[usp_Entity_Create]",
                                    param_names=[ "Name","Description","CreatedBy","ModuleName","IsActive","DisplayOrder","ModuleDescription","ApplicablePrivileges","Heading","Subheading","AddressURL","ImgWidth","LoginType","IsNewTab","AppCategory","ImageName","CardImage","MimeType"],
                                    param_values=[entity.Name,entity.Description,str(CreatedBy),entity.ModuleName,entity.IsActive,entity.DisplayOrder,entity.ModuleDescription,entity.ApplicablePrivileges,entity.card.Heading,entity.card.Subheading,entity.card.AddressURL,entity.card.ImgWidth,entity.card.LoginType,entity.card.IsNewTab,entity.card.AppCategory,image_name,file_binary,mime_type],
                                    fetch_data=False
                                    )

    except Exception as ex:
        logger.exception(f'Exception in CreateEntityHelper: {ex!r}')
        raise


# READ - Get All Entities
async def GetEntitiesHelper():
    try:
        entities,dashboardCards,dashboardCardImages = await exec_stored_procedure_multiple_sets(sp_name="[MKSIdentity].[usp_Entity_GetAll]",param_names=[],param_values=[],fetch_data=True)
        
        entities_list = [
            GetUpdateEntityModel(
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
            GetUpdateDashboardCardModel(
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
            GetUpdateDashboardCardImageModel(
                ID=dci[0],
                DashboardCardId=dci[1],
                CardImage=base64.b64encode((dci[2])).decode('utf-8') if dci[2] else None,
                ImageName=dci[3],
                MimeType=dci[4],
            ).dict()
            for dci in dashboardCardImages
        ]
        
        
        dci_map = {dci["DashboardCardId"]: dci for dci in dashboardCardImages_list} 
                    
        for card in dashboardCards_list:
            card["dashboardCardImage"] = dci_map.get(card["ID"])
        
        cards_by_entity = {}
        for card in dashboardCards_list:
            cards_by_entity[card["EntityId"]] = card
                
        for entity in entities_list:
            entity["card"] = cards_by_entity.get(entity["ID"], {})     
        
        logger.debug(f'\n\n\nusp_Entity_GetAll==> Enitites : \n\n{entities_list} \n{type(entities_list)}')
        
        return jsonable_encoder(entities_list)   
        
    except Exception as ex:
        logger.exception(f'Exception in GetEntitiesHelper: {ex!r}')
        raise


# UPDATE - Now accepts entity_id separately from entity data
async def UpdateEntityHelper(entity_id: UUID, entity: GetUpdateEntityModel, ModifiedBy: UUID):
    """
    Updates an entity. Dashboard card fields are optional.
    """
    try:
        file_binary = None
        image_name = None
        mime_type = None
        if entity.card and entity.card.dashboardCardImage:
            card_image = entity.card.dashboardCardImage
            if card_image.CardImage is not None:
                file_binary = base64.b64decode(card_image.CardImage)
                image_name = card_image.ImageName
                mime_type = card_image.MimeType
            else:
                file_binary = b''
        print(' \n\n\nfile_binary: \n\n\n', file_binary, type(file_binary))
        print("\n\n\n entity: \n\n\n",entity)
        # Call the stored procedure
        await exec_stored_procedure(sp_name="[MKSIdentity].[usp_Entity_Update]",
                                    param_names=[ "EnitityId","Name","Description","CreatedBy","ModuleName","ModuleDescription","IsActive","DisplayOrder","CardId","AddressURL","ImgWidth","Heading","Subheading","LoginType","IsNewTab","AppCategory","Ordinal","CardImageId","CardImage","ImageName","MimeType"],
                                    param_values=[entity_id,entity.Name,entity.Description,entity.CreatedBy,entity.ModuleName,entity.ModuleDescription,entity.IsActive,entity.DisplayOrder,entity.card.ID,entity.card.AddressURL,entity.card.ImgWidth,entity.card.Heading,entity.card.Subheading,entity.card.LoginType,entity.card.IsNewTab,entity.card.AppCategory,entity.card.Ordinal,entity.card.dashboardCardImage.ID,file_binary,image_name,mime_type],
                                    fetch_data=False
                                    )
    except Exception as ex:
        logger.exception(f'Exception in UpdateEntityHelper: {ex!r}')
        raise



# DELETE - Now accepts a single entity_id instead of a list
async def DeleteEntitiesHelper(entity_id: UUID, DeletedBy: UUID):
    try:
        await exec_stored_procedure(
            sp_name="[MKSIdentity].[usp_Entity_Delete]",
            param_names=["EntityId", "DeletedBy"],
            param_values=[str(entity_id), str(DeletedBy)],
            fetch_data=False
        )
    except Exception as ex:
        logger.exception(f'Exception in DeleteEntitiesHelper: {ex!r}')
        raise
