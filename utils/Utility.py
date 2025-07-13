import mysql.connector
from mysql.connector import pooling
from utils.Colors import Colors

class Mysql:
    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.pool = pool

    def get_connection(self):
        """
        Get a connection from the pool.
        """
        return self.pool.get_connection()

    def ensure_table_exists(self, cursor):
        """
        Ensures the watchlist table exists.
        """
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                discord_id BIGINT NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                type VARCHAR(10) NOT NULL,
                PRIMARY KEY (discord_id, symbol)
            );
        """)

    def add_to_watchlist(self, discord_id: int, symbol: str, asset_type: str) -> bool:
        """
        Adds a symbol to the user's watchlist.
        Returns True on success, False if duplicate or error.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            self.ensure_table_exists(cursor)

            cursor.execute(
                "INSERT INTO watchlist (discord_id, symbol, type) VALUES (%s, %s, %s)",
                (discord_id, symbol.upper(), asset_type.lower()),
            )
            conn.commit()
            return True

        except mysql.connector.IntegrityError:
            # Duplicate entry
            return False

        except mysql.connector.Error as e:
            print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}{Colors.BOLD}] {e}{Colors.RESET}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_watchlist(self, discord_id: int, asset_type: str) -> list:
        """
        Returns a list of symbols in the user's watchlist filtered by asset type.

        Args:
            discord_id (int): The user's Discord ID.
            asset_type (str): Must be either 'crypto' or 'stock'.

        Returns:
            list: List of symbol strings (e.g., ['BTC', 'ETH']).
        """
        try:
            if asset_type.lower() not in ("crypto", "stock"):
                print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] Invalid asset type '{asset_type}'. Must be 'crypto' or 'stock'.{Colors.RESET}")
                return []

            conn = self.get_connection()
            cursor = conn.cursor()

            self.ensure_table_exists(cursor)

            cursor.execute(
                "SELECT symbol FROM watchlist WHERE discord_id = %s AND type = %s",
                (discord_id, asset_type.lower()),
            )
            return [row[0] for row in cursor.fetchall()]

        except mysql.connector.Error as e:
            print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] {e}{Colors.RESET}")
            return []

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



    def remove_from_watchlist(self, discord_id: int, symbol: str) -> bool:
        """
        Removes a symbol from the user's watchlist.
        Returns True if something was deleted, False otherwise.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            self.ensure_table_exists(cursor)

            cursor.execute(
                "DELETE FROM watchlist WHERE discord_id = %s AND symbol = %s",
                (discord_id, symbol.upper()),
            )
            conn.commit()
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}{Colors.BOLD}ERROR{Colors.RESET}{Colors.BOLD}] {e}{Colors.RESET}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def clear_watchlist(self, discord_id: int, asset_type: str) -> bool:
        """
        Deletes all entries of the given asset type from the user's watchlist.
        Returns True if any rows were deleted, else False.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            self.ensure_table_exists(cursor)

            cursor.execute(
                "DELETE FROM watchlist WHERE discord_id = %s AND type = %s",
                (discord_id, asset_type.lower())
            )
            conn.commit()
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"{Colors.BOLD}[{Colors.BRIGHT_RED}ERROR{Colors.RESET}{Colors.BOLD}] {e}{Colors.RESET}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class Formatting:
    def format_with_commas(value: str) -> str:
        """
        Formats a numeric string with commas and handles scientific notation:
        - If value < 1: preserves all decimal places (e.g., 0.00001233)
        - If value >= 1: rounds to 2 decimal places and formats with commas (e.g., 12,345.68)
        - Handles scientific notation like '1.233e-05' → '0.00001233'

        Args:
            value (str): A numeric string (e.g., '0.012312', '1.233e-05', '12345.6789').

        Returns:
            str: Formatted number as a string or "N/A" if invalid.
        """
        try:
            num = float(value)

            if num == 0:
                return "0"

            if abs(num) < 1:

                decimal_str = f"{num:.20f}".rstrip("0").rstrip(".")
                return decimal_str

            return f"{num:,.2f}" 
        except (ValueError, TypeError):
            return "N/A"
