from azure.identity.aio import DefaultAzureCredential
cred_attempts = 0
credential = DefaultAzureCredential()

async def is_credential_expired(credential):
    try:
        await credential.get_token("https://management.azure.com/.default")
        return False
    except:
        return True

async def get_msi_cred():
    global cred_attempts, credential
    try:
        if await is_credential_expired(credential):
            credential = DefaultAzureCredential()
        return credential

    except:
        cred_attempts+=1
        if cred_attempts<4:
            return await get_msi_cred()
        else:
            cred_attempts=0
        raise