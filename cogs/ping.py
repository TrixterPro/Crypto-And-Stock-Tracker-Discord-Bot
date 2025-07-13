import discord
from discord.ext import commands
from discord import app_commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description="Shows the ping of the bot!")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = self.bot.latency * 1000
        embed = discord.Embed(title="Pong!",
                              description=f"🏓 Latency is {bot_latency:.2f}ms",
                              color=discord.Color.green())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(PingCog(bot))