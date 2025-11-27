# most of this code is from https://github.com/malmeloo/FindMy.py/blob/main/examples/fetch_reports_async.py

import asyncio
import logging

from _login import get_account_async
from classes import TrackerRequest

from findmy import KeyPair

STORE_PATH = "/mnt/storage/account.json"

ANISETTE_SERVER = None

ANISETTE_LIBS_PATH = "/mnt/storage/ani_libs.bin"

logging.basicConfig(level=logging.INFO)


async def fetch_reports(request: TrackerRequest) -> str:
    acc = await get_account_async(STORE_PATH, ANISETTE_SERVER, ANISETTE_LIBS_PATH)
    response = {}

    try:
        print(f"Logged in as: {acc.account_name} ({acc.first_name} {acc.last_name})")

        # should probably use asyncio.gather here for multiple trackers
        for tracker in request.trackers:
            name = tracker.name
            priv_key = tracker.privateKey
            key = KeyPair.from_b64(priv_key)
            location = await acc.fetch_location(key)
            
            response[name] = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timestamp": location.timestamp.isoformat(),
                "status": location.status,
            }
            
    finally:
        await acc.close()

        # Make sure to save account state when you're done!
        # Otherwise you have to log in again...
        acc.to_json(STORE_PATH)

    return response