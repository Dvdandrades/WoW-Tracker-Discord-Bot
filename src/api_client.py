import aiohttp
import asyncio


class BlizzardAPIClient:
    def __init__(self, client_id: str, client_secret: str):

        if not client_id or not client_secret:
            raise ValueError(
                "CLIENT_ID and CLIENT_SECRET must be set in environment variables."
            )

        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.oath_url: str = "https://oauth.battle.net/token"
        self.api_url: str = "https://eu.api.blizzard.com"
        self.namespace: str = "dynamic-eu"
        self._access_token: str = None

    async def get_access_token(self, retries=3, backoff=1) -> str:
        for attempt in range(retries):
            try:
                auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
                data = {"grant_type": "client_credentials"}
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.oath_url, auth=auth, data=data, timeout=5
                    ) as response:
                        response.raise_for_status()
                        token_data = await response.json()
                        token = token_data.get("access_token")
                        return token
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff * (2**attempt))
                else:
                    print("All retry attempts failed.")
