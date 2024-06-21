from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord import app_commands
from discord.ext import commands
from responses import get_response
import httpx

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
API_KEY: Final[str] = os.getenv('RIOT_API_KEY')

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True  # Enable members intent
intents.presences = True  # Enable presence intent
client = commands.Bot(command_prefix="!", intents=intents)


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
async def opgg(interaction: discord.Interaction, username: str, tagline: str):
    # await interaction.response.send_message(f"{username}#{tagline}")
    accountResponse = httpx.get(
        f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tagline}?api_key={API_KEY}")
    accountBody = accountResponse.json()
    puuid: str = accountBody["puuid"]
    summonerResponse = httpx.get(
        f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}")
    summonerBody = summonerResponse.json()
    print(summonerBody)

    await interaction.response.send_message(f"{summonerBody}")


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
