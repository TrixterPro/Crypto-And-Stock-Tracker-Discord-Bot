import ast
import subprocess
import sys
import os
from utils.Colors import Colors

def get_imports_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        root = ast.parse(f.read(), filename=filepath)

    imports = set()
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def auto_install_missing_packages():
    script_path = os.path.abspath(sys.argv[0])
    imports = get_imports_from_file(script_path)

    for package in imports:
        try:
            __import__(package)
        except ImportError:
            if package == 'mysql':
                package = 'mysql-connector-python'
            elif package == 'yaml':
                package = 'pyaml'
            elif package == 'discord':
                package = 'discord.py'
            print(f"{Colors.BOLD}[{Colors.BLUE}{Colors.BOLD}INFO{Colors.RESET}{Colors.BOLD}]  Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

auto_install_missing_packages()
