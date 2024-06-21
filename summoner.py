from PIL import Image

class Summoner:
    def __init__(self, id: str, account_id: str, puuid: str, profile_icon_id: int, revision_date: int, summoner_level: int, riot_id: str):
        self.id = id
        self.account_id = account_id
        self.puuid = puuid
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.summoner_level = summoner_level
        self.riot_id = riot_id        

    def __str__(self) -> str:
        return f"Username: {self.riot_id}\nLevel: {self.summoner_level}" 
