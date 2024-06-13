import discord
from discord.ext import commands, tasks
import datetime

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


@tasks.loop(hours=12)  # 每隔一小时执行一次
async def change_channel_name():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_channel_name = f"Channel Name - {current_time}"  # 可以根据需要定义新的频道名称

    guild_id = 123456789012345678  # 伺服器 ID
    channel_id = 123456789012345678  # 頻道 ID
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    if channel:
        try:
            await channel.edit(name=new_channel_name)
            print(f"Successfully changed channel name to '{new_channel_name}'")
        except discord.Forbidden:
            print("I don't have permission to rename that channel.")
        except discord.HTTPException as e:
            print(f"Failed to rename channel: {e}")
    else:
        print(f"Channel with ID {channel_id} not found.")

# 启动定时任务
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('Bot is ready!')
    change_channel_name.start()  # 启动定时任务

# bot.run('MTI1MDQxNTU2OTM1NDYyMDk3OA.Gv_kUP.k7NaZqyTXwYIb-8SrN57xOuBldanWe9TpcaIDY')
bot.run(os.getenv("BOT_TOKEN"))