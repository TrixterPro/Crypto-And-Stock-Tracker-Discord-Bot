import yaml
import os

CONFIG_PATH = "config.yml"

DEFAULT_CONFIG = {
    "TOKEN": "",
    "PREFIX": "!",
    "ALPHA_VANTAGE_API_KEY": "",
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": 3306,
    "MYSQL_USER": "",
    "MYSQL_PASSWORD": "",
    "MYSQL_DATABASE": ""
}

class basicconfig:
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as file:
            file.write("# Your discord bot token - get it by creating an application at https://discord.com/developers/applications\n")
            yaml.dump({"TOKEN": DEFAULT_CONFIG["TOKEN"]}, file)

            file.write("\n# Prefix is for the discord bot prefixed commands (such as !help, '!' is the prefix here)\n")
            yaml.dump({"PREFIX": DEFAULT_CONFIG["PREFIX"]}, file)

            file.write("\n# Alpha Vantage API key - get it from https://www.alphavantage.co/support/#api-key\n")
            yaml.dump({"ALPHA_VANTAGE_API_KEY": DEFAULT_CONFIG["ALPHA_VANTAGE_API_KEY"]}, file)

            file.write("\n# MySQL server host (e.g., localhost or IP address)\n")
            yaml.dump({"MYSQL_HOST": DEFAULT_CONFIG["MYSQL_HOST"]}, file)

            file.write("\n# MySQL server port (integer)\n")
            yaml.dump({"MYSQL_PORT": DEFAULT_CONFIG["MYSQL_PORT"]}, file)

            file.write("\n# MySQL username\n")
            yaml.dump({"MYSQL_USER": DEFAULT_CONFIG["MYSQL_USER"]}, file)

            file.write("\n# MySQL password (leave empty if no password is set)\n")
            yaml.dump({"MYSQL_PASSWORD": DEFAULT_CONFIG["MYSQL_PASSWORD"]}, file)

            file.write("\n# MySQL database name\n")
            yaml.dump({"MYSQL_DATABASE": DEFAULT_CONFIG["MYSQL_DATABASE"]}, file)

    # Read and validate config
    try:
        with open(CONFIG_PATH, "r") as file:
            _config = yaml.safe_load(file)
        if not isinstance(_config, dict) or set(_config.keys()) != set(DEFAULT_CONFIG.keys()):
            raise ValueError("Invalid configuration structure.")
    except (yaml.YAMLError, ValueError):
        # Rename old file only after it is closed
        os.rename(CONFIG_PATH, "old-config.yml")

        _config = DEFAULT_CONFIG.copy()
        with open(CONFIG_PATH, "w") as reset_file:
            reset_file.write("# Your discord bot token - get it by creating an application at https://discord.com/developers/applications\n")
            yaml.dump({"TOKEN": _config["TOKEN"]}, reset_file)

            reset_file.write("\n# Prefix is for the discord bot prefixed commands (such as !help, '!' is the prefix here)\n")
            yaml.dump({"PREFIX": _config["PREFIX"]}, reset_file)

            reset_file.write("\n# Alpha Vantage API key - get it from https://www.alphavantage.co/support/#api-key\n")
            yaml.dump({"ALPHA_VANTAGE_API_KEY": _config["ALPHA_VANTAGE_API_KEY"]}, reset_file)

            reset_file.write("\n# MySQL server host (e.g., localhost or IP address)\n")
            yaml.dump({"MYSQL_HOST": _config["MYSQL_HOST"]}, reset_file)

            reset_file.write("\n# MySQL server port (integer)\n")
            yaml.dump({"MYSQL_PORT": _config["MYSQL_PORT"]}, reset_file)

            reset_file.write("\n# MySQL username\n")
            yaml.dump({"MYSQL_USER": _config["MYSQL_USER"]}, reset_file)

            reset_file.write("\n# MySQL password (leave empty if no password is set)\n")
            yaml.dump({"MYSQL_PASSWORD": _config["MYSQL_PASSWORD"]}, reset_file)

            reset_file.write("\n# MySQL database name\n")
            yaml.dump({"MYSQL_DATABASE": _config["MYSQL_DATABASE"]}, reset_file)

    # Config values accessible as class variables
    TOKEN = _config.get("TOKEN", "")
    PREFIX = _config.get("PREFIX", "!")
    ALPHA_VANTAGE_API_KEY = _config.get("ALPHA_VANTAGE_API_KEY", "")
    MYSQL_HOST = _config.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = _config.get("MYSQL_PORT", 3306)
    MYSQL_USER = _config.get("MYSQL_USER", "")
    MYSQL_PASSWORD = _config.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = _config.get("MYSQL_DATABASE", "")
