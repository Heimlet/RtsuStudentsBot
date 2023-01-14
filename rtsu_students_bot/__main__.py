# Just CLI interface for server & bot

import typer

import uvicorn

from .config import settings

app = typer.Typer()
run_command = typer.Typer()


@run_command.command("server", help="Runs the server.")
def run_server():
    """Starts the server."""

    logging_format = uvicorn.config.LOGGING_CONFIG

    logging_format["formatters"]["access"]["fmt"] = settings.logging.format
    logging_format["formatters"]["default"]["fmt"] = settings.logging.format

    uvicorn.run(
        app="rtsu_students_bot.server.app:app",
        host=settings.server.host,
        port=settings.server.port,
    )


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
