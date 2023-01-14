import typer as typer
from sqlalchemy.util import asyncio

from db.base import init_models
from models.content import Content  # noqa: F401
from models.notification import Notification  # noqa: F401
from models.subscription import Subscription  # noqa: F401
from models.user import User  # noqa: F401

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())


if __name__ == '__main__':
    cli()
