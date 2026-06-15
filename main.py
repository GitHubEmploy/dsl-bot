"""
Discord Moderation & Utility Bot

Basic Discord bot with ping, info, and moderation commands.

Requires: discord.py (python -m pip install -r requirements.txt)
Setup: Copy config.py to config_local.py and fill in your token.
"""

import discord
from discord.ext import commands
import config


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# --- Utility Commands ---

@bot.command(name="ping")
async def ping(ctx):
    """Check the bot's latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")


@bot.command(name="info")
async def info(ctx):
    """Display bot information."""
    embed = discord.Embed(
        title="DSL Bot",
        description="A simple moderation and utility bot.",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Prefix", value=config.PREFIX, inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Servers", value=f"{len(bot.guilds)}", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


# --- Moderation Commands ---

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    """Kick a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} | Reason: {reason}")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need the `Kick Members` permission to use this command.")


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    """Ban a member from the server."""
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention} | Reason: {reason}")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need the `Ban Members` permission to use this command.")


@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Delete a number of messages from the current channel."""
    if amount < 1:
        await ctx.send("Amount must be at least 1.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"Deleted {len(deleted) - 1} message(s).", delete_after=3)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need the `Manage Messages` permission to use this command.")


if __name__ == "__main__":
    bot.run(config.TOKEN)
