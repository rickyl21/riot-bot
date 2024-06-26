import os
import httpx
import discord

from typing import Final
from dotenv import load_dotenv
from discord import Intents, Message, File
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

# Set the base directory for your project using relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True  # Enable members intent
intents.presences = True  # Enable presence intent
client = commands.Bot(command_prefix="?", intents=intents)

account_api = RiotAPI(api_key=API_KEY, region="americas")
lol_api = RiotAPI(api_key=API_KEY)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
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

    if not message.content.startswith(client.command_prefix or "!"):
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


@client.tree.command(name="opgg")
@app_commands.describe(username="Riot Username", tagline="#NA1")
async def opgg(interaction: discord.Interaction, username: str, tagline: str = "NA1"):
    try:
        account_body = await account_api.get_account_by_riot_id(username, tagline)
        puuid: str = account_body["puuid"]
        
        summoner_body = await lol_api.get_summoner_by_puuid(puuid)
        mastery_body = await lol_api.get_champion_master_by_puuid(puuid)
        
        summoner_id: str = summoner_body["id"]
        league_body = await lol_api.get_league_queues_by_summoner_id(summoner_id)
        
        queue_ranks = {"RANKED_FLEX_SR": None,
                       "CHERRY": None, "RANKED_SOLO_5x5": None}

        for queue in league_body:
            queue_ranks[queue["queueType"]] = queue

        riot_id = username + "#" + tagline

        summoner = Summoner(summoner_id, 
                            summoner_body["accountId"], 
                            summoner_body["puuid"],
                            summoner_body["profileIconId"], 
                            summoner_body["revisionDate"], 
                            summoner_body["summonerLevel"],
                            riot_id, 
                            queue_ranks)

        profile_icon_url = summoner.get_profile_icon_url(ver=DDRAGON_VER)

        solo_tier = summoner.get_tier(solo=True)
        flex_tier = summoner.get_tier(solo=False)

        solo_rank = summoner.get_rank(solo=True)
        flex_rank = summoner.get_rank(solo=False)
            
        ranked_icon_tier = summoner.get_main_rank()

        image_path = os.path.join(ASSETS_DIR, f"{ranked_icon_tier}.png")
        if not os.path.exists(image_path):
            image_path = os.path.join(ASSETS_DIR, "unranked.png")
        rank_image = File(image_path, filename="rank_emblem.png")

        embed = discord.Embed(
            title=f"{summoner.riot_id}",
            description=f"Level: {summoner.summoner_level}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=profile_icon_url)
        embed.add_field(name="Solo", value=f"{solo_tier.capitalize()} {
                        solo_rank}", inline=True)
        embed.add_field(name="Flex", value=f"{flex_tier.capitalize()} {
                        flex_rank}", inline=True)
        embed.set_image(url="attachment://rank_emblem.png")
        embed.set_footer(text=f"Revision Date: {summoner.revision_date}")

        await interaction.response.send_message(embed=embed, file=rank_image)
    except httpx.HTTPStatusError as e:
        await interaction.response.send_message(f"Error fetching summoner data")
        print(e)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
