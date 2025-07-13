import discord
from discord.ext import commands
from discord import app_commands, ui
from utils.Utility import Mysql
from utils.api import get_crypto_price
from utils.Utility import Formatting


class Watchlist(commands.GroupCog, name='watchlist'):
    def __init__(self, bot):
        self.bot = bot

    # ==== ADD COMMAND ====
    @app_commands.command(name='add', description='Adds an asset to the respective watchlist.')
    @app_commands.describe(symbol='The symbol of the asset you want to add, e.g., BTC, AAPL, etc.')
    @app_commands.describe(asset='The asset type of the symbol.')
    @app_commands.choices(asset=[
        app_commands.Choice(name='Crypto', value="Crypto"),
        app_commands.Choice(name='Stock', value="Stock")
    ])
    async def add(self, interaction: discord.Interaction, symbol: str, asset: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=True)
        
        check = get_crypto_price(symbol=symbol)
        if not check:
            await interaction.response.send_message(
                f"❌ The symbol `{symbol.upper()}` is invalid or not found as {asset.name}. Please check and try again.",
                ephemeral=True
            )
            return
        
        
        interaction_user_id = interaction.user.id
        mysql: Mysql = self.bot.mysql
        watchlist_func = mysql.add_to_watchlist(discord_id=interaction_user_id, symbol=symbol, asset_type=asset.name)
        
        if watchlist_func:
            embed = discord.Embed(title='Success',
                                description=f'**Successfully added {symbol.upper()} ({asset.name}) in your watchlist.**\n-# Use `/watchlist view` to view your watchlist\n-# Use `/watchlist remove` to remove an asset from the watchlist',
                                color=discord.Color.green())
        
        if not watchlist_func:
            embed = discord.Embed(
                title='Already Added',
                description=f'**{symbol.upper()} ({asset.name}) is already in your watchlist.**\n-# Use `/watchlist view` to view your watchlist\n-# Use `/watchlist remove` to remove an asset from the watchlist',
                color=discord.Color.orange()
            )
        
        await interaction.followup.send(embed=embed)
        
    # ==== VIEW COMMAND ====
    @app_commands.command(name='view', description='Shows your current watchlist for the asset.')
    @app_commands.describe(market="The market currency in which you want to view the watchlist, eg. USD, INR, etc.")
    @app_commands.describe(asset='The asset type of the symbol.')
    @app_commands.choices(asset=[
        app_commands.Choice(name='Crypto', value='Stock'),
        app_commands.Choice(name='Stock', value='Stock')
    ])
    async def view(self, interaction: discord.Interaction, asset: app_commands.Choice[str], market: str = "USD"):
        await interaction.response.defer()
        try:
            market = market.upper()  
            interaction_user = interaction.user

            mysql: Mysql = self.bot.mysql
            watchlist = mysql.get_watchlist(discord_id=interaction_user.id, asset_type=asset.name)
            
            if watchlist:
                embed = discord.Embed(
                    title=f"{interaction_user.name}'s Watchlist",
                    description="-# Use `/watchlist add` to add an asset to your watchlist\n-# Use `/watchlist remove` to remove an asset from your watchlist",
                    color=discord.Color.green()
                )
                if interaction_user.avatar:
                    avatar_url = interaction_user.avatar.url
                    
                if not interaction_user.avatar:
                    avatar_url = interaction_user.default_avatar.url
                    
                embed.set_thumbnail(url=avatar_url)
                number_of_symbols = 0
                for symbol in watchlist:
                    crypto_details = get_crypto_price(symbol=symbol, market=market)
                    number_of_symbols +=1
                    
                    open_price = Formatting.format_with_commas(crypto_details.get("open"))
                    high_price = Formatting.format_with_commas(crypto_details.get("high"))
                    low_price = Formatting.format_with_commas(crypto_details.get("low"))
                    close_price = Formatting.format_with_commas(crypto_details.get("close"))
                    volume = Formatting.format_with_commas(crypto_details.get("volume"))
                    timestamp = Formatting.format_with_commas(crypto_details.get("timestamp"))
                    
                    embed.add_field(name=f"{number_of_symbols}. {symbol}", value=f"**🟢 Open Price**\n`{open_price} {market}`\n\n**📈 High**\n`{high_price} {market}`\n\n**📉 Low**\n`{low_price} {market}`\n\n**🔴 Close Price**\n`{close_price} {market}`\n\n**💰 Volume Traded**\n`{volume} Coins/Tokens`\n-# updated at {timestamp}", inline=False)
                    
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Watchlist Empty",
                    description="You don't have any assets in your watchlist.\n-# Use `/watchlist add` to add an asset.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send(
                f"Could not fetch price for `{symbol}` in `{market.upper()}`.",
                ephemeral=True
            )
     
     
    # ==== REMOVE COMMAND ====
    
    @app_commands.command(name='remove', description='Removes an asset to the respective watchlist.')
    @app_commands.describe(symbol='The symbol of the asset you want to remove from your watchlist, e.g., BTC, AAPL, etc.')
    async def remove(self, interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(ephemeral=True)
        
        mysql: Mysql= self.bot.mysql
        check = mysql.remove_from_watchlist(discord_id=interaction.user.id, symbol=symbol)
        
        if not check:
            await interaction.followup.send(
                f"❌ The symbol `{symbol.upper()}` was not found in your watchlist.",
                ephemeral=True
            )
            return
        embed = discord.Embed(
            title='Removed',
            description=f'**Successfully removed {symbol.upper()} from your watchlist.**\n-# Use `/watchlist view` to view your watchlist\n-# Use `/watchlist add` to add an asset to your watchlist',
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)
        
    
    @app_commands.command(name='list', description='List symbols for given asset in your watchlist.')
    @app_commands.describe(asset='The asset type to list (Crypto or Stock).')
    @app_commands.choices(asset=[
        app_commands.Choice(name='Crypto', value='Crypto'),
        app_commands.Choice(name='Stock', value='Stock')
    ])
    async def list(self, interaction: discord.Interaction, asset: app_commands.Choice[str]):
        await interaction.response.defer()

        mysql: Mysql = self.bot.mysql
        symbols = mysql.get_watchlist(discord_id=interaction.user.id, asset_type=asset.value)

        if symbols:
            embed = discord.Embed(
                title=f"{interaction.user.name}'s {asset.name} Watchlist",
                description="\n".join(f"- `{symbol}`" for symbol in symbols),
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Total: {len(symbols)} assets")

            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                    title="No Assets Found",
                    description="Your watchlist is empty. Use `/watchlist add` to add some!",
                    color=discord.Color.red()
                )
            await interaction.followup.send(
                embed=embed)
            
    # ==== CLEAR COMMAND ====

    @app_commands.command(name='clear', description='Clear your entire watchlist for the selected asset type.')
    @app_commands.describe(asset='The asset type to clear from your watchlist (Crypto or Stock).')
    @app_commands.choices(asset=[
        app_commands.Choice(name='Crypto', value='crypto'),
        app_commands.Choice(name='Stock', value='stock')
    ])
    async def clear(self, interaction: discord.Interaction, asset: app_commands.Choice[str]):
        mysql: Mysql = self.bot.mysql

        user_id = interaction.user.id
        embed = discord.Embed(
            title="⚠️ Confirm Watchlist Clear",
            description=f"Are you sure you want to **clear all `{asset.name}` assets** from your watchlist?\n\nThis action **cannot be undone.**",
            color=discord.Color.orange()
        )

        avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        embed.set_author(name=interaction.user.name, icon_url=avatar_url)

        button = ui.Button(
            label='Confirm',
            emoji='🗑️',
            style= discord.ButtonStyle.red
        )
        
        view = ui.View(timeout=None)
        view.add_item(button)
        
        async def confirm_callback(interaction: discord.Interaction):
            if interaction.user.id != user_id:
                await interaction.response.send_message("This button isn't for you!", ephemeral=True)
                return

            success = mysql.clear_watchlist(discord_id=user_id, asset_type=asset.name)

            if success:
                embed = discord.Embed(
                    title="✅ Watchlist Cleared",
                    description=f"All `{asset.name}` assets have been removed from your watchlist.",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="📂 Watchlist Already Empty",
                    description=f"You had no `{asset.name}` assets in your watchlist.",
                    color=discord.Color.light_grey()
                )

            await interaction.response.edit_message(embed=embed, view=None)
            
        button.callback = confirm_callback
        
        await interaction.response.send_message(embed=embed, view=view)

        


    
                
        
        

async def setup(bot):
    await bot.add_cog(Watchlist(bot))