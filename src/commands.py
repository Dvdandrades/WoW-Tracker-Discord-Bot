from .api_client import BlizzardAPIClient
import asyncio


async def get_token_price(blizzard_client: BlizzardAPIClient) -> float:
    data = await blizzard_client.request("/data/wow/token/index", "dynamic-eu")
    return data.get("price") / 10000


async def get_character_info(
    blizzard_client: BlizzardAPIClient, character_data: str
) -> dict:
    try:
        name, realm = character_data.split("-")
    except ValueError:
        raise ValueError("Character data must be in the format 'Name-Realm'")

    summary_task = blizzard_client.request(
        endpoint=f"/profile/wow/character/{realm.lower()}/{name.lower()}", 
        namespace="profile-eu"
    )
    media_task = blizzard_client.request(
        endpoint=f"/profile/wow/character/{realm.lower()}/{name.lower()}/character-media", 
        namespace="profile-eu"
    )
    stats_task = blizzard_client.request(
        endpoint=f"/profile/wow/character/{realm.lower()}/{name.lower()}/statistics", 
        namespace="profile-eu"
    )

    data, media, stats = await asyncio.gather(summary_task, media_task, stats_task)

    if not data or not stats:
        raise ValueError("Character not found. Please check the name and realm.")

    image_url = None
    if media and "assets" in media:
        assets = {a["key"]: a["value"] for a in media["assets"]}
        image_url = assets.get("avatar")

    return {
        "name": data.get("name"),
        "level": data.get("level"),
        "race": data.get("race").get("name"),
        "character_class": data.get("character_class").get("name"),
        "spec": data.get("active_spec").get("name"),
        "ilvl": data.get("equipped_item_level"),
        "faction": data.get("faction").get("name"),
        "image_url": image_url,
        "stats": {
            "health": stats.get("health"),
            "stamina": stats.get("stamina"),
            "crit": f"{stats.get('melee_crit').get('value'):.2f}%",
            "haste": f"{stats.get('melee_haste').get('value'):.2f}%",
            "mastery": f"{stats.get('mastery').get('value'):.2f}%",
            "versatility": f"{stats.get('versatility')}"
        }
    }