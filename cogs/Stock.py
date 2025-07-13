import discord
from discord.ext import commands
from discord import app_commands
from utils.api import get_stock_price
from utils.Utility import Formatting

class Stock(commands.GroupCog, name='stock'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='price', description='Get the current price of a specified stock symbol.')
    @app_commands.describe(symbol='The stock symbol to look up', market='The market currency (default: USD)')
    async def price(self, interaction: discord.Interaction, symbol: str, market: str = 'USD'):
        market = market.upper()
        symbol = symbol.upper()
        
        stock_details = get_stock_price(symbol=symbol, market=market)

        if stock_details is None:
            await interaction.response.send_message(
                f"❌ Could not fetch price for `{symbol}` in `{market}`.",
                ephemeral=True
            )
            return

        open_price = Formatting.format_with_commas(stock_details.get("open"))
        high_price = Formatting.format_with_commas(stock_details.get("high"))
        low_price = Formatting.format_with_commas(stock_details.get("low"))
        current_price = Formatting.format_with_commas(stock_details.get("price"))
        volume = Formatting.format_with_commas(stock_details.get("volume"))
        change_percent = stock_details.get("change_percent")
        timestamp = stock_details.get("timestamp")

        embed = discord.Embed(
            title=f"📈 {symbol} Market Summary",
            description=f"💱 Showing values in **{market}**\n📊 **Change:** `{change_percent}`",
            color=discord.Color.blurple()
        )

        embed.add_field(name="🟢 Open", value=f"`{open_price}`", inline=True)
        embed.add_field(name="📈 High", value=f"`{high_price}`", inline=True)
        embed.add_field(name="📉 Low", value=f"`{low_price}`", inline=True)
        embed.add_field(name="💵 Current Price", value=f"`{current_price}`", inline=True)

        embed.add_field(name="💰 Volume", value=f"`{volume}` Shares", inline=False)

        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"📅 Last updated on {timestamp}")

        await interaction.response.send_message(embed=embed)

        
    @app_commands.command(name='compare', description='Compare the current prices of two stock symbols.')
    @app_commands.describe(symbol1='The first stock symbol to compare.')
    @app_commands.describe(symbol2='The second stock symbol to compare.')
    @app_commands.describe(market='The fiat market currency to compare against (default is USD).')
    async def compare(self, interaction: discord.Interaction, symbol1: str, symbol2: str, market: str = 'USD'):
        await interaction.response.defer(ephemeral=False)

        symbol1 = symbol1.upper()
        symbol2 = symbol2.upper()
        market = market.upper()

        data1 = get_stock_price(symbol1, market=market)
        data2 = get_stock_price(symbol2, market=market)

        if not data1 or not data2:
            return await interaction.followup.send(
                f"❌ Could not retrieve data for `{symbol1}` or `{symbol2}`.",
                ephemeral=True
            )

        embed = discord.Embed(
            title=f"📊 {symbol1} vs {symbol2}",
            description=f"Currency: **{market}**",
            color=discord.Color.dark_gold()
        )

        def format_line(key: str, label: str) -> str:
            v1 = data1.get(key, "N/A")
            v2 = data2.get(key, "N/A")

            if key != "timestamp":
                v1 = Formatting.format_with_commas(v1)
                v2 = Formatting.format_with_commas(v2)

            return f"**{symbol1}**: `{v1}`\n**{symbol2}**: `{v2}`"

        embed.add_field(name="💵 Current Price", value=format_line("price", "Price"), inline=True)
        embed.add_field(name="📈 High", value=format_line("high", "High"), inline=True)
        embed.add_field(name="📉 Low", value=format_line("low", "Low"), inline=True)
        embed.add_field(name="🟢 Open", value=format_line("open", "Open"), inline=True)
        embed.add_field(name="💰 Volume", value=format_line("volume", "Volume"), inline=True)
        embed.add_field(name="📊 % Change", value=format_line("change_percent", "Change %"), inline=True)
        embed.add_field(name="🕒 Last Updated", value=format_line("timestamp", "Updated"), inline=False)

        embed.set_footer(text="Source: Alpha Vantage")

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stock(bot))