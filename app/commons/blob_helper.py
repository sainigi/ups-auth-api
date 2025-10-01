import os
import logging
from datetime import datetime

from azure.storage.blob.aio import BlobClient, ContainerClient, BlobLeaseClient

from commons.msi_helper import get_msi_cred

logger = logging.getLogger()
storage_account = os.environ["storage_account"]
storage_url = f'https://{storage_account}.blob.core.windows.net/'
blob_attempts = 0

async def WriteFile(container_name: str, blob_name: str, blob, overwrite: bool = False):
    global blob_attempts
    try:
        credential = await get_msi_cred()
        async with credential:
            logger.debug(f"Credential received for Blob")
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            await blob_client.upload_blob(blob, overwrite=overwrite)
            logger.info(f"Blob {blob_name} was written successfully to {container_name}")
            blob_attempts=0
    except:
        blob_attempts+=1
        if blob_attempts<4:
            await WriteFile(container_name=container_name, blob_name=blob_name, blob=blob, overwrite=overwrite)
        else:
            blob_attempts=0
        raise

async def BlobExists(container_name: str, blob_name: str) -> bool:
    global blob_attempts
    try:
        credential = await get_msi_cred()
        async with credential:
            logger.debug(f"Credential received for Blob")
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            exists = await blob_client.exists()
            blob_attempts = 0
            return exists
    except:
        blob_attempts += 1
        if blob_attempts < 4:
            return await BlobExists(container_name=container_name, blob_name=blob_name)
        else:
            blob_attempts = 0
        raise

async def ReadBlob(container_name: str, blob_name: str)-> str:
    try:
        credential = await get_msi_cred()
        async with credential:
            logger.debug(f"Credential received for Blob")
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            blob_stream = await blob_client.download_blob()
            blob_data = await blob_stream.readall()
            json_string = blob_data.decode('utf-8')
            logger.debug(f"Blob {blob_name} was read successfully from {container_name}")
            return json_string
    except :
        raise

async def write_lease_blob(container_name: str, blob_name: str, blob, blob_present, lease: BlobLeaseClient,
                           overwrite: bool = False):
    global blob_attempts
    try:
        credential = await get_msi_cred()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            if blob_present:
                await blob_client.upload_blob(blob, lease=lease, overwrite=overwrite)
                await lease.release()
            else:
                await blob_client.upload_blob(blob, overwrite=overwrite)
            blob_attempts = 0
    except Exception as ex:
        blob_attempts+=1
        if blob_attempts<4:
            await write_lease_blob(container_name=container_name, blob_name=blob_name, blob=blob,
                                   blob_present=blob_present, lease=lease, overwrite=overwrite)
        else:
            blob_attempts=0
        raise

async def read_lease_blob(container_name: str, blob_name: str) -> (str, BlobLeaseClient):
    try:
        credential = await get_msi_cred()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            lease = None
            while not lease:
                try:
                    lease = await blob_client.acquire_lease(lease_duration=30)
                    blob_stream = await blob_client.download_blob(lease=lease)
                    blob_byte_data = await blob_stream.readall()
                    json_string = blob_byte_data.decode('utf-8')
                    return json_string, lease

                except Exception:
                    continue

    except Exception as ex:
        raise
async def list_directory(container_name: str, fromDate: str,toDate: str):
    try:
        credential = await get_msi_cred()
        async with credential:
            container_client = ContainerClient(account_url=storage_url, container_name=container_name,
                                               credential=credential)
            blobs = container_client.list_blobs()

            names = []
            fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
            toDate = datetime.strptime(toDate, "%Y-%m-%d")
            async for blob in blobs:
                blob_last_modified_from = blob.last_modified.replace(tzinfo=fromDate.tzinfo)
                blob_last_modified_to = blob.last_modified.replace(tzinfo=toDate.tzinfo)

                if blob_last_modified_from >= fromDate and blob_last_modified_to <= toDate:
                    names.append(blob.name)

            return names
    except Exception as ex:
        logger.exception(f'Exception while listing directory: {ex!r}')
        raise

async def delete_blob(container_name: str, blob_name: str):
    global blob_attempts
    try:
        credential = await get_msi_cred()
        async with credential:
            blob_client = BlobClient(account_url=storage_url, container_name=container_name, blob_name=blob_name,
                                     credential=credential)
            await blob_client.delete_blob("include")
            blob_attempts = 0
    except Exception as ex:
        blob_attempts+=1
        if blob_attempts<4:
            await delete_blob(container_name=container_name, blob_name=blob_name)
        else:
            blob_attempts=0
        raise