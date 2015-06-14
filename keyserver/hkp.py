import asyncio
import logging
from urllib import parse

from aiohttp import web

from keyserver.key import PublicKey, PrivateKey
from keyserver.db import File

LOG = logging.getLogger(__name__)


class Server:

    def __init__(self):
        self.db = File("/tmp/t")

    @asyncio.coroutine
    def root(self, request):
        LOG.debug(request)

    @asyncio.coroutine
    def add(self, request):
        LOG.debug(request)
        LOG.debug(request.content_type)
        keytext = yield from request.post()
        key = PublicKey(keytext["keytext"])
        LOG.info("Import request %r" % key)
        # TODO: check for:
        # * duplicate request
        # * already imported keys
        # * expired keys
        self.db.add_request(key)
        ciphertext = key.encrypt("wat")
        return web.Response(text="Check email")

    @asyncio.coroutine
    def confirm(self, request):
        secret = parse.parse_qs(request.query_string)["secret"][0]
        LOG.info("Confirming secret %s" % secret)
        try:
            self.db.confirm(secret)
            return web.Response(text="Ok")
        except:
            LOG.exception("Failed to validate secret")
        return web.Response(text="Fail")

    @asyncio.coroutine
    def lookup(self, request):
        LOG.debug(request)
        LOG.debug(request.headers)
        qs = parse.parse_qs(request.query_string)
        LOG.debug(qs)
        if qs["op"] == ["get"]:
            mr = "mr" in qs["options"]
            for keyid in qs["search"]:
                key = self.db.get_key_by_id(keyid)
                return web.Response(body=key.key)


    @asyncio.coroutine
    def start(self, loop, host="127.0.0.1", port=80):
        app = web.Application(loop=loop)
        app.router.add_route("GET", "/", self.root)
        app.router.add_route("GET", "/confirm", self.confirm)
        app.router.add_route("GET", "/pks/lookup", self.lookup)
        app.router.add_route("POST", "/pks/add", self.add)
        srv = yield from loop.create_server(app.make_handler(), host, port)
        return srv
