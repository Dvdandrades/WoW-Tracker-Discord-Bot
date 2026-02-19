import aiohttp

from api_client import BlizzardAPIClient

async def token_price() -> int:
    access_token = await BlizzardAPIClient.get_access_token()
    url = f"https://eu.api.blizzard.com/data/wow/token/index"
    params = {
        "namespace": BlizzardAPIClient.namespace,
        "locale": "en_US",
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            price = data.get("price") / 10000
            return price

