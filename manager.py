import typer as typer
from sqlalchemy.util import asyncio

from db.base import init_models
from models.notification import Notification
from models.content import Content
from models.user import User
from models.subscription import Subscription
cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == '__main__':
    cli()
