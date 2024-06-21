class Summoner:
    def __init__(self, id: str, accountId: str, puuid: str, profileIconId: int, revisionDate: int, summonerLevel: int):
        self.id = id
        self.accountId = accountId
        self.puuid = puuid
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel

    def __str__(self):
        return f"Username: {self.accountId}\nLevel: {self.summonerLevel}"
