from aiogram import executor
from typer import Typer, Argument

from .config import settings
from .bot import get_app, handlers

typer_app = Typer()


@typer_app.command()
def start(
        skip_updates: bool = Argument(default=False, help="Skip telegram updates on start?"),
        use_webhook: bool = Argument(default=False, help="Use webhook for receiving updates?")
):
    """
    Starts bot
    :param skip_updates: Skip telegram updates on start?
    :param use_webhook: Use webhook mode for receiving updates?
    """

    # Build bot
    dp = get_app()

    # Build startup-handler

    startup_handler = handlers.startup.startup_handler_factory()

    if use_webhook:
        # Check for `webhook` settings are not `None`

        if settings.webhooks is None:
            print("Please, fill webhook's settings.")
            exit(-1)

        startup_handler = handlers.startup.startup_handler_factory(f"{settings.webhooks.host}{settings.webhooks.path}")

        executor.start_webhook(
            dispatcher=dp,
            on_startup=startup_handler,
            skip_updates=True,
            host=settings.webhooks.webapp_host,
            port=settings.webhooks.webapp_port,
            webhook_path=settings.webhooks.path,
            check_ip=False
        )
    else:
        executor.start_polling(
            dp,
            skip_updates=skip_updates,
            on_startup=startup_handler
        )
