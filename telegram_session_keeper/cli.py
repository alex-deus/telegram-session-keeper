#!/usr/bin/env python
import asyncio

import click

from telegram_session_keeper import db, main


@click.group()
def cli() -> None:
    ...


@cli.command
@click.option(
    "-a", "--action", type=click.Choice(["save", "display"], case_sensitive=False), default="save", show_default=True
)
@click.option("-p", "--phone", type=str, required=True, help="Phone number as digits")
def create(action: str, phone: int) -> None:
    session: str = asyncio.run(main.create_session(str(phone)))
    if action == "save":
        is_appended = db.append_session(str(phone), session)
        if is_appended:
            click.secho("Phone has been added", fg="green")
        else:
            click.secho("Phone is already exists", fg="yellow", err=True)

    elif action == "display":
        click.secho(f"{session=}", fg="green")

    else:
        click.secho(f"Unknown {action=}", fg="yellow", err=True)


@cli.command
def show_list() -> None:
    rows = db.get_sessions_list()

    click.secho(f"Phone\t\t\t\tCreated", fg="green")
    for row in rows:
        click.secho(f"{row['phone']}\t\t{row['created']}", fg="green")


@cli.command
@click.option("-p", "--phone", type=str, required=True, help="Phone number as digits")
@click.option("-t", "--timeout", type=int, default=60, help="Timeout for waiting in secs")
def get_code(phone: int, timeout: int) -> None:
    session: str | None = db.get_session(str(phone))
    if not session:
        return click.secho("Session was not found", fg="yellow", err=True)

    code: str = asyncio.run(main.wait_for_code(session, timeout))
    click.secho(f"{code=}", fg="green")


@cli.command
@click.option("-p", "--phone", type=str, required=True, help="Phone number as digits")
def remove(phone: int) -> None:
    is_removed = db.remove_session(str(phone))

    if is_removed:
        click.secho("Phone has been removed", fg="green")
    else:
        click.secho("Nothing to remove", fg="yellow", err=True)


if __name__ == "__main__":
    cli()
