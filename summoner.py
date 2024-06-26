from PIL import Image

class Summoner:
    def __init__(self, id: str, account_id: str, puuid: str, profile_icon_id: int, revision_date: int, summoner_level: int, riot_id: str, queue_ranks: dict[str: any]):
        self.id = id
        self.account_id = account_id
        self.puuid = puuid
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.summoner_level = summoner_level
        self.riot_id = riot_id    
        self.queue_ranks = queue_ranks    

    def __str__(self) -> str:
        return f"Username: {self.riot_id}\nLevel: {self.summoner_level}" 
    
    def get_tier(self, solo: bool) -> str:
        if solo:
            if self.queue_ranks["RANKED_SOLO_5x5"]:
                return self.queue_ranks["RANKED_SOLO_5x5"]["tier"].lower()
        else:
            if self.queue_ranks["RANKED_FLEX_SR"]:
                return self.queue_ranks["RANKED_FLEX_SR"]["tier"].lower()
        return "unranked"
    
    def get_rank(self, solo: bool) -> str:
        NUMERAL_MAP: dict[str: int] = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5"}
        
        if solo:
            if self.queue_ranks["RANKED_SOLO_5x5"]:
                return NUMERAL_MAP[self.queue_ranks["RANKED_SOLO_5x5"]["rank"]]
        else:
            if self.queue_ranks["RANKED_FLEX_SR"]:
                return NUMERAL_MAP[self.queue_ranks["RANKED_FLEX_SR"]["rank"]]
        return ""
    
    def get_profile_icon_url(self, ver: str) -> str:
        return f"https://ddragon.leagueoflegends.com/cdn/{ver}/img/profileicon/{self.profile_icon_id}.png"
    
    def get_main_rank(self) -> str:
        if self.queue_ranks['RANKED_SOLO_5x5']:
            return self.get_tier(solo=True)
        elif self.queue_ranks["RANKED_FLEX_SR"]:
            return self.get_tier(solo=False)
        else:
            return "unranked"
