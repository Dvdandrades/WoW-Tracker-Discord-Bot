import aiohttp
import asyncio
import time


class BlizzardAPIClient:
    def __init__(self, client_id: str, client_secret: str, region: str = "eu") -> None:

        if not client_id or not client_secret:
            raise ValueError(
                "CLIENT_ID and CLIENT_SECRET must be set in environment variables."
            )

        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.region: str = region
        self.base_url = f"https://{region}.api.blizzard.com"
        self.oauth_url: str = "https://oauth.battle.net/token"

        self._session: aiohttp.ClientSession = None
        self._access_token: str = None
        self._token_expiry: float = 0

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def get_access_token(self, retries: int = 3, backoff: float = 1) -> str:
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token
        for attempt in range(retries):
            try:
                auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
                data = {"grant_type": "client_credentials"}

                async with self._session.post(
                    self.oauth_url, auth=auth, data=data, timeout=5
                ) as response:
                    response.raise_for_status()
                    token_data = await response.json()
                    self._access_token = token_data.get("access_token")
                    self._token_expiry = time.time() + token_data.get("expires_in") - 60
                    return self._access_token
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(backoff * (2**attempt))
                else:
                    print("All retry attempts failed.")

    async def request(self, endpoint: str, namespace: str, params: dict = None) -> dict:
        token = await self.get_access_token()
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {token}"}

        default_params = {"namespace": namespace, "locale": "en_US"}
        if params:
            default_params.update(params)

        async with self._session.get(
            url, headers=headers, params=default_params
        ) as response:
            if response.status == 200:
                return await response.json()
            return None
