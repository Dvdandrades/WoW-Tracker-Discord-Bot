import aiohttp
import asyncio
import time


class BlizzardAPIClient:
    def __init__(self, client_id: str, client_secret: str) -> None:

        if not client_id or not client_secret:
            raise ValueError(
                "CLIENT_ID and CLIENT_SECRET must be set in environment variables."
            )

        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.oath_url: str = "https://oauth.battle.net/token"
        self._access_token: str = None
        self._token_expiry: float = 0

    async def get_access_token(self, retries: int = 3, backoff: float = 1) -> str:
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token
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
                        self._access_token = token_data.get("access_token")
                        self._token_expiry = (
                            time.time() + token_data.get("expires_in") - 60
                        )
                        return self._access_token
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff * (2**attempt))
                else:
                    print("All retry attempts failed.")
