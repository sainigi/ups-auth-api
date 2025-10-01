import os

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

from commons.msi_helper import get_msi_cred

ns_name = os.environ["ns_name"]
sb_ns_endpoint = f'sb://{ns_name}.servicebus.windows.net'
service_bus_attempts= 0

async def send_message_to_queue(msg: str, queue_name: str):
    global service_bus_attempts
    try:
        credential = await get_msi_cred()
        async with credential:
            sb_client = ServiceBusClient(sb_ns_endpoint, credential)
            async with sb_client:
                sender = sb_client.get_queue_sender(queue_name=queue_name)
                async with sender:
                    await sender.send_messages(
                        ServiceBusMessage(msg))
        service_bus_attempts = 0
    except:
        service_bus_attempts+=1
        if service_bus_attempts<4:
            await send_message_to_queue(msg=msg, queue_name=queue_name)
        else:
            service_bus_attempts=0
        raise
