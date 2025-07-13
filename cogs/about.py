import discord
from discord.ext import commands
from discord import app_commands

class About(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="about", description="Get information about the bot and its developer.")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📈 Crypto & Stock Tracker",
            description="A modular Discord bot for real-time stock & crypto tracking.",
            color=discord.Color.blurple()
        )

        embed.add_field(name="👨‍💻 Developer", value="**Trix**", inline=True)
        embed.add_field(name="💻 GitHub", value="[TrixterPro](https://github.com/TrixterPro)", inline=True)
        embed.add_field(name="💬 Discord", value="`codewithtrix`", inline=True)

        embed.add_field(
            name="🛠️ Built With",
            value="• Python `discord.py`\n• MySQL\n• Alpha Vantage API",
            inline=False
        )

        embed.set_thumbnail(url=interaction.client.user.avatar.url if interaction.client.user.avatar else discord.Embed.Empty)
        embed.set_footer(text="Thank you for using the bot 💖")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(About(bot))
