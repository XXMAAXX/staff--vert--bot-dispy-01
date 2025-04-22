import os
import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

config = {
    "welcome_audio": "sond/xx.mp3",
    "allow_roms": [
      1190942032986902558,
      1190942171818381372,
      1190942278647304213,
      1190942397119594496,
      1191132172711628831
    ],
    "welcome_message": {
        "guild":1107426801002754199,
        "channel": 1203206009368354816,
        "message": "<a:00000purplemoon:1165675032735911977><a:1_:1110998146265387058> <a:1_:1110998146265387058>  𝐀𝐧𝐲𝐨𝐧𝐞 𝐈𝐧 𝐓𝐡𝐞 𝐓𝐨𝐣 <:voice1:1171154567988248626> 𝐓𝐞𝐚𝐦 𝐈𝐬 <a:aadrs_pub:1171153390408040508> 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐓𝐨 𝐂𝐨𝐦𝐞 𝐓𝐨 𝐓𝐡𝐞 𝐀𝐮𝐝𝐢𝐨 𝐑𝐨𝐨𝐦  <a:1_:1110998146265387058>  <a:1_:1110998146265387058> <@&1156769721111281664>https://cdn.discordapp.com/attachments/1120529147500957757/1203246788421619712/solo-leveling-announces-trailer-and-release-window.webp?ex=65d065e5&is=65bdf0e5&hm=ea1c350573278f5a77f7be31&"
    }
}

bot = commands.Bot(command_prefix='!', intents=intents)

# قم بتحديد المسار الكامل لتنفيذ FFmpeg على نظامك
ffmpeg_path = "/nix/store/mpiwml99aicr7jj7g8mss6s3jf28idg0-jellyfin-ffmpeg-5.1.2-8-bin/bin/ffmpeg"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel: return
    if after.channel is None: return
    if after.channel.id is None: return

    if after.channel.id in config["allow_roms"]:
        vc = discord.utils.get(bot.voice_clients, guild=after.channel.guild)

        if vc is None:
            vc = await after.channel.connect()

        if vc is not None and vc.is_connected():
            vc.play(FFmpegPCMAudio(config["welcome_audio"], executable=ffmpeg_path), after=lambda e: print('Done', e))
            message = await (bot.get_guild(config["welcome_message"]["guild"])
                        .get_channel(config["welcome_message"]["channel"])
                        .send(config["welcome_message"]["message"]))

        while vc.is_playing():
            await asyncio.sleep(0.1)

        await vc.disconnect()

# تسجيل الخطأ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use `!help` for a list of commands.")
    else:
        print(f"An error occurred: {error}")

try:
    token = os.getenv("TOKEN") or ""
    if not token:
        raise Exception("Please add your token to the Secrets pane.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e