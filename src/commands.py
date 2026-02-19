import aiohttp


async def get_token_price(blizzard_client) -> int:
    access_token = await blizzard_client.get_access_token()
    url = "https://eu.api.blizzard.com/data/wow/token/index"
    params = {
        "namespace": "dynamic-eu",
        "locale": "en_US",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("price") / 10000
