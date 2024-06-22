import httpx
from typing import Dict, Any

class RiotAPI:
    def __init__(self, api_key: str, region: str = "na1"):
        self.api_key = api_key
        self.region = region
        self.base_url = f"https://{region}.api.riotgames.com"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-Riot-Token": self.api_key,
            "Content-Type": "application/json"
        }

    async def get_account_by_riot_id(self, username: str, tagline: str) -> Dict[str, Any]:
        url = f"{self.base_url}/riot/account/v1/accounts/by-riot-id/{username}/{tagline}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
    async def get_summoner_by_puuid(self, puuid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        
    async def get_champion_master_by_puuid(self, puuid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()