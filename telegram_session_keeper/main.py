import asyncio
import re

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession

from telegram_session_keeper.settings import settings

__all__ = ["create_session", "wait_for_code"]


async def create_session(phone: str) -> str:
    client = TelegramClient(phone, settings.api_id, settings.api_hash)
    await client.connect()
    await client.send_code_request(phone)

    code = input("Input a code from Telegram/SMS: ")
    try:
        await client.sign_in(phone=phone, code=code)
    except SessionPasswordNeededError:
        password = input("Input cloud password: ")
        await client.sign_in(password=password)

    raw_session = StringSession.save(client.session)

    await client.disconnect()

    return raw_session


async def _wait_for_code(client, timeout: int = 60) -> str | None:
    future = asyncio.get_event_loop().create_future()

    @client.on(events.NewMessage)
    async def handler(event) -> None:
        if not future.done() and event.chat_id == 777000:
            results = re.search(r"(\d{5})", event.raw_text, re.MULTILINE)
            if results:
                future.set_result(results[0])

    try:
        code = await asyncio.wait_for(future, timeout=timeout)

        return code
    except asyncio.TimeoutError:
        ...


async def wait_for_code(session: str, timeout: int) -> str | None:
    client = TelegramClient(StringSession(session), settings.api_id, settings.api_hash)

    await client.connect()

    task = asyncio.create_task(_wait_for_code(client, timeout=60))
    code: str | None = await task

    await client.disconnect()

    return code
