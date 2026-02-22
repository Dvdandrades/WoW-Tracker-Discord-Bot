import aiohttp


async def get_token_price(blizzard_client: object) -> int:
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


async def get_character_info(blizzard_client: object, character_data: str) -> dict:
    try:
        name, realm = character_data.split("-")
    except ValueError:
        raise ValueError("Character data must be in the format 'Name-Realm'")

    data = await blizzard_client.get_character_summary(
        realm_slug=realm, character_name=name
    )
    if not data:
        raise ValueError("Character not found. Please check the name and realm.")

    return {
        "name": data.get("name"),
        "level": data.get("level"),
        "race": data.get("race").get("name"),
        "class": data.get("character_class").get("name"),
        "spec": data.get("active_spec").get("name"),
        "ilvl": data.get("equipped_item_level"),
        "faction": data.get("faction").get("name"),
    }
