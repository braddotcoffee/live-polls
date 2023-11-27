import asyncio
from threading import Thread
from quart import copy_current_app_context


def run_with_context(callback, *args, **kwargs):
    Thread(
        target=asyncio.run,
        args=(copy_current_app_context(callback)(*args, **kwargs),),
    ).start()
