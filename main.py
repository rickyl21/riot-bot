import os
import httpx
import discord

from typing import Final
from dotenv import load_dotenv
from discord import Intents, Message
from discord import app_commands
from discord.ext import commands
from responses import get_response
from riot_api import RiotAPI
from summoner import Summoner

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
API_KEY: Final[str] = os.getenv('RIOT_API_KEY')
DDRAGON_VER = httpx.get(
    "https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True  # Enable members intent
intents.presences = True  # Enable presence intent
client = commands.Bot(command_prefix="!", intents=intents)

account_api = RiotAPI(api_key=API_KEY, region="americas")
lol_api = RiotAPI(api_key=API_KEY)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    try:
        synced = await client.tree.sync()
        print(f"Synced  {len(synced)} command(s)")
    except Exception as e:
        print(e)

    try:
        print(DDRAGON_VER)
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


@client.tree.command(name="opgg")
@app_commands.describe(username="Riot Username", tagline="#NA1")
async def opgg(interaction: discord.Interaction, username: str, tagline: str = "NA1"):
    accountBody = await account_api.get_account_by_riot_id(username, tagline)
    puuid: str = accountBody["puuid"]
    summonerBody = await lol_api.get_summoner_by_puuid(puuid)

    riotId = username + "#" + tagline
    profile_icon_id = summonerBody["profileIconId"]
    profile_icon_url = f"https://ddragon.leagueoflegends.com/cdn/{
        DDRAGON_VER}/img/profileicon/{profile_icon_id}.png"

    summoner = Summoner(summonerBody["id"], summonerBody["accountId"], summonerBody["puuid"],
                        summonerBody["profileIconId"], summonerBody["revisionDate"], summonerBody["summonerLevel"],
                        riotId)

    embed = discord.Embed(
        title=f"{summoner.riot_id}",
        description=f"Level: {summoner.summoner_level}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=profile_icon_url)
    embed.set_footer(text="Profile Icon")

    await interaction.response.send_message(embed=embed)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
