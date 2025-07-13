try:
    from utils.PackageHandler import auto_install_missing_packages
    from utils.Colors import Colors
    print(f'[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}] Verifying packages...')
    auto_install_missing_packages()
    
    from utils.Utility import Mysql
    import discord
    from discord.ext import commands
    import os
    import asyncio
    from utils.config import basicconfig
    import mysql.connector
    from mysql.connector import pooling
    import yaml
    import alpha_vantage


    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix=basicconfig.PREFIX, intents=intents)
    bot.help_command = None

    loaded_extensions = []

    async def initiate_mysql():
        try:
            pool = pooling.MySQLConnectionPool(
                pool_name="bot_pool",
                pool_size=5,
                host=basicconfig.MYSQL_HOST,
                port=basicconfig.MYSQL_PORT,
                user=basicconfig.MYSQL_USER,
                password=basicconfig.MYSQL_PASSWORD,
                database=basicconfig.MYSQL_DATABASE
            )

            bot.mysql = Mysql(pool)
            print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] MySQL connection pool created successfully.")

        except mysql.connector.Error as e:
            print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Failed to create MySQL connection pool: {e}")
            raise
    
    async def disconnect_mysql():
        """Disconnects the MySQL client if it exists."""
        if hasattr(bot, 'mysql'):
            try:
                bot.mysql_client.close()
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}] MySQL connection closed successfully.")
            except Exception as e:
                print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] An error occurred while closing the MySQL connection: {e}")
        
    async def handle_console_command(command):
        command = command.lower().strip()
        try:
            if command == "shutdown":
                print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}] Shutting down the bot...")
                await bot.close()
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] Successfully shut down the bot.")
                exit(f'[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] Bot has been shut down.')
                
            elif command == "restart mysql":
                print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}] Restarting MySQL connection...")
                await disconnect_mysql()
                await initiate_mysql()
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] MySQL connection restarted successfully.")
            elif command == "shutdown mysql":
                print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}] Shutting down MySQL connection...")
                await disconnect_mysql()
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] MySQL connection shut down successfully.")
            elif command == "start mysql":
                print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}] Starting MySQL connection...")
                try:
                    await initiate_mysql()
                    print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] MySQL connection started successfully.")
                except Exception as e:
                    print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error starting MySQL connection: {e}")
            elif command == "reload cogs":
                print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}] Reloading all cogs...")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        ext_name = f"cogs.{filename[:-3]}"
                        try:
                            await bot.reload_extension(ext_name)
                            print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] Successfully reloaded {filename[:-3]}")
                        except commands.ExtensionNotLoaded:
                            try:
                                await bot.load_extension(ext_name)
                                print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] {filename[:-3]} was not loaded, so loaded it instead.")
                            except Exception as load_e:
                                print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error loading {filename[:-3]}: {load_e}")
                        except Exception as e:
                            print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error reloading {filename[:-3]}: {e}")
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] All cogs reloaded successfully.")
            
            elif command.startswith("reload "):
                cog_name = command.split(" ", 1)[1]
                ext_name = f"cogs.{cog_name}"
                try:
                    await bot.reload_extension(ext_name)
                    print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] Successfully reloaded {cog_name} cog.")
                except commands.ExtensionNotLoaded:
                    try:
                        await bot.load_extension(ext_name)
                        print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] {cog_name} was not loaded, so loaded it instead.")
                    except Exception as load_e:
                        print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error loading {cog_name}: {load_e}")
                except Exception as e:
                    print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error reloading {cog_name}: {e}")
                    
            elif command == "clear logs":
                log_dir = "Logs"
                for filename in os.listdir(log_dir):
                    if filename == "latest.log":
                        continue
                    file_path = os.path.join(log_dir, filename)
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                            print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] Cleared log file: {filename}")
                        except Exception as e:
                            print(f"[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}] Error clearing log file {filename}: {e}")
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}{Colors.BOLD}] All log files cleared successfully.")
            elif command in ("help", "?"):
                print(f"{Colors.BLUE}{Colors.BOLD}{Colors.UNDERLINE}Available commands:{Colors.RESET}")
                print(f"{Colors.MAGENTA}1. {Colors.CYAN}shutdown{Colors.RESET}         - {Colors.YELLOW}Shuts down the bot.{Colors.RESET}")
                print(f"{Colors.MAGENTA}3. {Colors.CYAN}restart mysql{Colors.RESET}    - {Colors.YELLOW}Restarts the MySQL connection.{Colors.RESET}")
                print(f"{Colors.MAGENTA}4. {Colors.CYAN}shutdown mysql{Colors.RESET}   - {Colors.YELLOW}Shuts down the MySQL connection.{Colors.RESET}")
                print(f"{Colors.MAGENTA}5. {Colors.CYAN}start mysql{Colors.RESET}      - {Colors.YELLOW}Starts the MySQL connection.{Colors.RESET}")
                print(f"{Colors.MAGENTA}6. {Colors.CYAN}reload cogs{Colors.RESET}      - {Colors.YELLOW}Reloads all cogs.{Colors.RESET}")
                print(f"{Colors.MAGENTA}7. {Colors.CYAN}reload <cog>{Colors.RESET}     - {Colors.YELLOW}Reloads a specific cog.{Colors.RESET}")
                print(f"{Colors.MAGENTA}10. {Colors.CYAN}clear LOGS{Colors.RESET}      - {Colors.YELLOW}Clears all log files except latest.log.{Colors.RESET}")
                print(f"{Colors.MAGENTA}11. {Colors.CYAN}help or ?{Colors.RESET}       - {Colors.YELLOW}Displays this help message.{Colors.RESET}")
            else:
                print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] Unknown command. Use 'help' or '?' to see available commands.{Colors.RESET}")
        except SystemExit as e:
            print(e)

    async def console_loop():
        print("Type 'help' or '?' for available commands.")
        while True:
            command = await asyncio.to_thread(input, f"{Colors.RESET}> ")
            await handle_console_command(command)
        

    # Loading all the cogs
    async def load_all_extensions():
        """Asynchronously loads all the extensions (cogs) from the cogs folder."""
        
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}] Successfully loaded {filename[:-3]}")
            else:
                pass


    @bot.event
    async def on_ready():

        await load_all_extensions()
        await initiate_mysql()
        synced = await bot.tree.sync()
        print(f"[{Colors.GREEN}{Colors.BOLD}LOGS{Colors.RESET}{Colors.BOLD}] Successfully synced all slash commands")
        print(
        f'''\n
        {Colors.BRIGHT_GREEN}{Colors.BOLD}BOT IS ONLINE!{Colors.RESET} ({bot.user})
    \n''')
        asyncio.create_task(console_loop())
        
            

        


    @bot.command()
    async def sync(ctx):
        await bot.tree.sync()
        await ctx.reply('**✅ Successfully synced all the slash commands**')

    # Load a cog
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def loadcog(ctx, cogname: str = None):
        if cogname:
            try:
                await bot.load_extension(f'cogs.{cogname}')
                await ctx.send(f'Loaded {cogname} cog successfully.')
            except Exception as e:
                await ctx.send(f'Error loading {cogname} cog: {e}')
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send('Loaded all cogs successfully.')

    # Unload a cog
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def unloadcog(ctx, cogname: str = None):
        if cogname:
            try:
                await bot.unload_extension(f'cogs.{cogname}')
                await ctx.send(f'Unloaded {cogname} cog successfully.')
            except Exception as e:
                await ctx.send(f'Error unloading {cogname} cog: {e}')
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.unload_extension(f'cogs.{filename[:-3]}')
            await ctx.send('Unloaded all cogs successfully.')

    @bot.command()
    async def reloadcog(ctx, cogname: str):
        try:
            await bot.reload_extension(f'cogs.{cogname}')
            await ctx.reply(f'Reloaded {cogname} cog successfully.')
        except Exception as e:
            await ctx.reply(f'Error Reloading {cogname} cog: {e}')




    import logging
    from datetime import datetime

    # Ensure the Logs directory exists
    log_dir = "Logs"
    os.makedirs(log_dir, exist_ok=True)

    # Rename 'latest.log' if it exists
    latest_log_path = os.path.join(log_dir, "latest.log")
    if os.path.exists(latest_log_path):
        # Create a new name for the old log file with Date-Time format
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_log_name = f"{timestamp}.log"
        new_log_path = os.path.join(log_dir, new_log_name)
        os.rename(latest_log_path, new_log_path)

    # Set up the logging handler for 'latest.log'
    handler = logging.FileHandler(filename=latest_log_path, mode="w", encoding="utf-8")

    # Start the bot with custom log handler
    bot.run(token=basicconfig.TOKEN, log_handler=handler)

except discord.errors.LoginFailure:
    class Wrong_Config(Exception):
        pass
    raise Wrong_Config('\n\n\n------------------[ERROR]-----------------\nPlease configure your bot in the config.yml file\nPossible causes of this error:\n- Wrong TOKEN in config.yml.\n- Config.yml file was missing so the bot created a new one. (Could be this reason if you are starting the bot for the first time)\n- The format for config.yml was wrong so the bot replaced it with the default config file Please reconfigure it\n\nPossible solution: Just follow the instructions in the config.yml file correctly\n\n')