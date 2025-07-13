import discord
from discord.ext import commands
from discord import app_commands
from utils.api import get_crypto_price
from utils.Utility import Formatting

class Crypto(commands.GroupCog, name='crypto'):
    def __init__(self, bot):
        self.bot = bot

    # =====PRICE COMMAND=====

    @app_commands.command(name='price', description='This command shows the price of crypto currency.')
    @app_commands.describe(symbol='The symbol of the crypto currency: e.g., BTC, ETH, AAPL')
    @app_commands.describe(market="The fiat market currency to compare against (default is 'USD').")
    async def price(self, interaction: discord.Interaction, symbol: str, market:str = "USD"):
    
        market = market.upper()
        symbol = symbol.upper()
        crypto_details = get_crypto_price(symbol=symbol, market=market)
        
        if crypto_details is None:
            await interaction.response.send_message(
                f"Could not fetch price for `{symbol}` in `{market.upper()}`.",
                ephemeral=True
            )
            return

        

        open_price = Formatting.format_with_commas(crypto_details.get("open"))
        high_price = Formatting.format_with_commas(crypto_details.get("high"))
        low_price = Formatting.format_with_commas(crypto_details.get("low"))
        close_price = Formatting.format_with_commas(crypto_details.get("close"))
        volume = Formatting.format_with_commas(crypto_details.get("volume"))
        timestamp = Formatting.format_with_commas(crypto_details.get("timestamp"))

        
        embed = discord.Embed(
            title=f"📊 {symbol.upper()} Market Summary",
            description=f"💱 Showing values in **{market.upper()}**",
            color=discord.Color.from_str("#00c18c")  # Soft green-blue tone
        )

        embed.add_field(name="🟢 Open Price", value=f"`{open_price}` {market.upper()}", inline=True)
        embed.add_field(name="📈 High", value=f"`{high_price}` {market.upper()}", inline=True)
        embed.add_field(name="📉 Low", value=f"`{low_price}` {market.upper()}", inline=True)
        embed.add_field(name="🔴 Close Price", value=f"`{close_price}` {market.upper()}", inline=True)

        embed.add_field(
            name="💰 Volume Traded",
            value=f"`{volume}` Coins/Tokens",
            inline=False
        )

        embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.display_avatar.url)

        embed.set_footer(text=f"📅 Data last updated on {timestamp}")
        
        await interaction.response.send_message(embed=embed)
        
        
        
    # ====COMPARE COMMAND=====
    
    @app_commands.command(name="compare", description="Compare two cryptocurrencies")
    @app_commands.describe(symbol1='The first symbol you want to compare.')
    @app_commands.describe(symbol2='The second symbol you want to compare.')
    @app_commands.describe(market='The fiat market currency to compare against (default is USD).')
    async def compare(self, interaction: discord.Interaction, symbol1: str, symbol2: str, market: str = 'USD'):
        await interaction.response.defer(ephemeral=False)

        data1 = get_crypto_price(symbol1, market=market)
        data2 = get_crypto_price(symbol2, market=market)

        if not data1 or not data2:
            return await interaction.followup.send(
                f"❌ Could not retrieve data for `{symbol1.upper()}` or `{symbol2.upper()}`.",
                ephemeral=True
            )

        embed = discord.Embed(
            title=f"🔄 Comparing {symbol1.upper()} vs {symbol2.upper()}",
            color=discord.Color.teal()
        )

        def format_entry(label, key):
            if key == "timestamp":
                v1 = data1.get(key, "N/A")
                v2 = data2.get(key, "N/A")
            else:
                v1 = Formatting.format_with_commas(data1.get(key, "N/A"))
                v2 = Formatting.format_with_commas(data2.get(key, "N/A"))

            return f"**{symbol1.upper()}**: {v1}\n**{symbol2.upper()}**: {v2}"

        embed.add_field(name="💰 Price", value=format_entry("Price", "open"), inline=True)
        embed.add_field(name="📈 High", value=format_entry("High", "high"), inline=True)
        embed.add_field(name="📉 Low", value=format_entry("Low", "low"), inline=True)
        embed.add_field(name="📊 Volume", value=format_entry("Volume", "volume"), inline=True)
        embed.add_field(name="🕒 Last Updated", value=format_entry("Time", "timestamp"), inline=False)


        await interaction.followup.send(embed=embed)
        
        
        
async def setup(bot):
    await bot.add_cog(Crypto(bot))