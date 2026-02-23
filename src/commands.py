from dataclasses import dataclass

from .api_client import BlizzardAPIClient


@dataclass
class CharacterInfo:
    name: str
    level: int
    race: str
    character_class: str
    spec: str
    ilvl: int
    faction: str


async def get_token_price(blizzard_client: BlizzardAPIClient) -> float:
    data = await blizzard_client.request("/data/wow/token/index", "dynamic-eu")
    return data.get("price") / 10000


async def get_character_info(
    blizzard_client: BlizzardAPIClient, character_data: str
) -> CharacterInfo:
    try:
        name, realm = character_data.split("-")
    except ValueError:
        raise ValueError("Character data must be in the format 'Name-Realm'")

    endpoint = f"/profile/wow/character/{realm.lower()}/{name.lower()}"
    data = await blizzard_client.request(endpoint=endpoint, namespace="profile-eu")

    if not data:
        raise ValueError("Character not found. Please check the name and realm.")

    return CharacterInfo(
        name=data.get("name"),
        level=data.get("level"),
        race=data.get("race").get("name"),
        character_class=data.get("character_class").get("name"),
        spec=data.get("active_spec").get("name"),
        ilvl=data.get("equipped_item_level"),
        faction=data.get("faction").get("name"),
    )
