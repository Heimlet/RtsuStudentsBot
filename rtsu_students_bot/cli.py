from aiogram import executor
from typer import Typer, Argument

from .bot import dispatcher_factory

typer_app = Typer()


@typer_app.command()
def start(
        skip_updates: bool = Argument(default=False, help="Skip telegram updates on start?"),
        use_webhook: bool = Argument(default=False, help="Use webhook mode for receiving updates?")
):
    """
    Starts bot
    :param skip_updates: Skip telegram updates on start?
    :param use_webhook: Use webhook mode for receiving updates?
    """

    # Build bot
    dp = dispatcher_factory()

    if use_webhook:
        raise NotImplementedError
    else:
        executor.start_polling(
            dp,
            skip_updates=skip_updates
        )
