# Just CLI interface for server & bot

import typer

from .constants import DEFAULT_ENCODING, SETTINGS_FILE
from .config import Settings

app = typer.Typer()
run_command = typer.Typer()

settings = Settings.parse_file(
    path=SETTINGS_FILE,
    encoding=DEFAULT_ENCODING
)


@run_command.command("server", help="Runs the server.")
def run_server():
    """Starts the server."""
    pass


@run_command.command("bot", help="Runs the bot")
def run_bot():
    """Starts the bot"""
    pass


@app.command("version")
def version():
    """Shows version of project."""
    pass


def main():
    """Runs the project."""
    app.add_typer(run_command, name="run", help="Run components, for example 'server'")
    app()


if __name__ == '__main__':
    main()
