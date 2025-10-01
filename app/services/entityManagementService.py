from uuid import UUID
from app.models.entity import Entity, UpdateEntityModel, DeleteEntity
from app.commons.sp_helper import exec_stored_procedure
import logging
from typing import List,Optional
from app.commons.db_helper import getCursor

logger = logging.getLogger()
#CREATE
async def CreateEntityHelper(entity: Entity, CreatedBy: UUID):
    try:
        card_image_bytes: Optional[bytes] = None
        # Prepare dashboard card values individually
        if entity.dashboard_card:
            dashboard_card_params = [
                entity.dashboard_card.Heading,
                entity.dashboard_card.Subheading or None,
                entity.dashboard_card.AddressURL or None,
                entity.dashboard_card.imgWidth or None,
                entity.dashboard_card.LoginType or None,
                entity.dashboard_card.IsNewTab if entity.dashboard_card.IsNewTab is not None else 0,
                entity.dashboard_card.AppCategory or None,
                entity.dashboard_card.ImageName or None,
                card_image_bytes,
                entity.dashboard_card.MimeType or None
            ]
        else:
            dashboard_card_params = [None] * 9

        await exec_stored_procedure(
            sp_name="MKSIdentity.usp_Entity_Create",
            param_names=[
                "Name",
                "Description",
                "CreatedBy",
                "ModuleName",
                "ModuleDescription",
                "ApplicablePrivileges",
                "Heading",
                "Subheading",
                "AddressURL",
                "ImgWidth",
                "LoginType",
                "IsNewTab",
                "AppCategory",
                "ImageName",
                "CardImage",
                "MimeType"
            ],
            param_values=[
                entity.Name,
                entity.Description,
                str(CreatedBy),
                entity.ModuleName,
                entity.ModuleDescription,
                entity.ApplicablePrivileges
            ] + dashboard_card_params,
            fetch_data=False
        )

    except Exception as ex:
        logger.exception(f'Exception in CreateEntityHelper: {ex!r}')
        raise


# READ - Get All Entities
async def GetEntitiesHelper():
    try:
        cursor, conn = await getCursor()

        # Call your stored procedure
        cursor.execute("{CALL MKSIdentity.usp_Entity_GetAll}")

        # First result set → Entities
        entities = cursor.fetchall()
        columns_entities = [col[0] for col in cursor.description]

        # Next result set → Cards
        cursor.nextset()
        cards = cursor.fetchall()
        columns_cards = [col[0] for col in cursor.description]

        # Next result set → Images
        cursor.nextset()
        images = cursor.fetchall()
        columns_images = [col[0] for col in cursor.description]

        conn.close()

        return {
            "entities": [dict(zip(columns_entities, row)) for row in entities],
            "cards": [dict(zip(columns_cards, row)) for row in cards],
            "images": [dict(zip(columns_images, row)) for row in images],
        }
    except Exception as ex:
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
                "ImgWidth": getattr(dc, "imgWidth", None),
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
