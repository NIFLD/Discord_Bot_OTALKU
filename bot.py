import discord
from discord.ext import commands, tasks
import datetime
import os

# intents = discord.Intents.default()
intents = discord.Intents.all()
client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix="!" , intents = intents)

# async def on_ready():
#     print(f'Logged in as {bot.user.name} - {bot.user.id}')
#     for guild in bot.guilds:
#         print(f'Bot is in guild: {guild.name} (id: {guild.id})')


@bot.command(name="rename_channel")
async def rename_channel(ctx, channel_name : str, new_name: str):
    # channel = bot.get_channel(channel_id)
     
    text_channels = ctx.guild.text_channels
    channel = discord.utils.get(text_channels, name=channel_name)
    
    if channel is None:
        await ctx.send("Channel is not found!")
        return 
    
    try:
        await channel.edit(name = new_name)
        await ctx.send("Channel name is change.")
    # except Exception as e:
    #     await ctx.send("Error to change channel name.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to rename that channel.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to rename channel: {e}")


@tasks.loop(seconds=5)  
async def change_channel_name():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_channel_name = f"Channel Name - {current_time}"  #

    guild_name = "NI"
    channel_name = "nini - {current_time}"
    guild = discord.utils.get(bot.guilds, name=guild_name)
    # channel = guild.get_channel(channel_name)

    if guild is None:
        print(f"Guild with name '{guild_name}' not found.")
        return

    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel is None:
        print(f"Channel with name '{channel_name}' not found in guild '{guild_name}'.")
        return

    try:
        await channel.edit(name=new_channel_name)
        print(f"Successfully changed channel name to '{new_channel_name}'")
    except discord.Forbidden:
        print("I don't have permission to rename that channel.")
    except discord.HTTPException as e:
        print(f"Failed to rename channel: {e}")

# 启动定时任务
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('Bot is ready!')
    change_channel_name.start()  # 启动定时任务

bot.run(os.getenv("BOT_TOKEN"))