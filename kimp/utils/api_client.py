import asyncio
import atexit

import aiohttp
import orjson

from urllib.parse import urlencode, quote

_sessions = {}


def get_session(name: str) -> aiohttp.ClientSession:
    global _sessions
    _session = _sessions.get(name)
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            raise_for_status=True, json_serialize=lambda x: orjson.dumps(x).decode()
        )
        _sessions[name] = _session
    return _session


def _cleanup_sessions():
    """Cleanup function that handles event loop issues gracefully."""
    if not _sessions:
        return

    # Get all open sessions
    open_sessions = [session for session in _sessions.values() if not session.closed]
    if not open_sessions:
        return

    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except RuntimeError:
        # No event loop exists or it's closed, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        # Close all sessions
        loop.run_until_complete(
            asyncio.gather(
                *[session.close() for session in open_sessions], return_exceptions=True
            )
        )
    except Exception:
        # If async cleanup fails, try synchronous cleanup
        for session in open_sessions:
            if not session.closed:
                try:
                    session._connector.close()
                except Exception:
                    pass
    finally:
        # Clean up the sessions dict
        _sessions.clear()


atexit.register(_cleanup_sessions)


class APIClient:
    def __init__(self, name: str, base_url: str):
        self.name: str = name
        self.session: aiohttp.ClientSession = get_session(name)
        self.base_url: str = base_url

    def set_header(self, key: str, value: str):
        self.session.headers[key] = value

    def get_url(self, *path, **params):
        url = f"{self.base_url}"
        if path:
            url += "/" + "/".join(quote(str(p).lstrip("/"), safe="") for p in path)
        if params:
            url += "?" + urlencode(params)
        return url

    async def get(self, *path, headers={}, **params):
        url = self.get_url(*path, **params)
        async with self.session.get(url, headers=headers) as response:
            return await response.json(loads=orjson.loads)
