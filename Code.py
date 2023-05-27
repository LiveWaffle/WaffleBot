import disnake
import requests
from disnake.ext import tasks, commands
import csv

intents = disnake.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True

client = disnake.Client(intents=intents)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("~"), intents=intents, reload=True)


url = "https://fortnite-api.com/v2/cosmetics/br/search"
url1 = "https://fortnitecentral.genxgames.gg/api/v1/aes"

csv_path = r"your path to cid csv"

@bot.event
async def on_ready():
    print("Bot Ready")

@bot.slash_command(name="aes", description="This will give the aes key")
async def aes(ctx):
    response = requests.get(url1)

    if response.status_code == 200:
        aes_data = response.json()
        version_data = response.json()
        main_key = aes_data["mainKey"]
        version = version_data["version"]
        dynamic_Key = aes_data["dynamicKeys"]
        embed = disnake.Embed(title=f"{version} AES Key", color=0x00ff00)
        embed.add_field(name="Main Key", value=main_key, inline=False)
        for key in dynamic_Key:
            embed.add_field(name=key['name'], value=key['key'], inline=False)
        await ctx.send(embed=embed)
        
@bot.slash_command(name="cid", description="This will give the character ID")
async def cid(ctx, name: str):

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        next(data)  

        matching_rows = [row for row in data if row[3].lower() == name.lower()]
        if not matching_rows:
            await ctx.send(f"Could not find a character with the name '{name}'")
            return
        character_id = matching_rows[0][1]
        character_name = matching_rows[0][3]

        embed = disnake.Embed(title=f"Character ID for '{character_name}'", color=0x00ff00)
        embed.add_field(name="ID", value=character_id, inline=False)
        await ctx.send(embed=embed)


bot.run('your token')
