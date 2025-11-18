import os
import asyncio
import textwrap
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# === Configuration ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
CRCON_PATH = Path(os.getenv("CRCON_PATH", "/root/hll_rcon_tool").strip())

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing in .env")
if CHANNEL_ID == 0:
    raise ValueError("DISCORD_CHANNEL_ID is missing or invalid in .env")

intents = discord.Intents.default()
intents.message_content = False  # not needed here

bot = commands.Bot(command_prefix="!", intents=intents)

# Persistent view with the button
class RCONView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # persistent view, never times out

    @discord.ui.button(label="Restart RCON", style=discord.ButtonStyle.primary, custom_id="persistent_rcon:restart")
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        logs = await restart_rcon()

        # Discord has a 2000-char limit for messages; 1990 to be safe with backticks
        truncated = textwrap.shorten(logs, width=1990, placeholder="...\n(truncated)")

        await interaction.followup.send(
            content=f"RCON restart completed.\n```{truncated}```",
            ephemeral=True
        )

async def restart_rcon() -> str:
    output = "Stopping containers...\n"
    try:
        proc = await asyncio.create_subprocess_exec(
            "docker", "compose", "down",
            cwd=CRCON_PATH,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        stdout, _ = await proc.communicate()
        output += stdout.decode() if stdout else ""

        output += "\nStarting containers...\n"
        proc = await asyncio.create_subprocess_exec(
            "docker", "compose", "up", "-d", "--remove-orphans",
            cwd=CRCON_PATH,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        stdout, _ = await proc.communicate()
        output += stdout.decode() if stdout else ""

        if proc.returncode != 0:
            output += f"\nProcess exited with code {proc.returncode}"
    except Exception as e:
        output += f"\nFailed: {str(e)}"
    
    return output or "No output captured."

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None or not isinstance(channel, discord.TextChannel):
        print(f"Could not find text channel with ID {CHANNEL_ID}")
        return

    # Clear previous messages (up to 100)
    try:
        await channel.purge(limit=100)
    except Exception as e:
        print(f"Failed to purge messages: {e}")

    # Register the persistent view (important for button to work after restart)
    bot.add_view(RCONView())

    embed = discord.Embed(
        title="RCON Control",
        description="Restart the HLL RCON container",
        color=0x00ff00
    )

    await channel.send(embed=embed, view=RCONView())
    print("Control message posted")

# Optional: allow manual /setup command in case the message gets deleted
@bot.slash_command(name="rconsetup", description="Post the RCON control panel (admin only)")
async def setup(ctx: discord.ApplicationContext):
    if not await bot.is_owner(ctx.author):  # or check for specific role/permission
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return
    await ctx.defer(ephemeral=True)
    channel = ctx.channel
    await channel.purge(limit=100)  # optional
    embed = discord.Embed(title="RCON Control", description="Restart the HLL RCON container", color=0x00ff00)
    await channel.send(embed=embed, view=RCONView())
    await ctx.followup.send("RCON control panel posted!", ephemeral=True)

bot.run(DISCORD_TOKEN)
