from temporalio.client import Client

async def get_temporal_client():
    return await Client.connect(
        "temporal:7233"
    )