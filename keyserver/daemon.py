import asyncio
import logging
import logging.config

from keyserver import hkp

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(name)s:"
                      "%(levelname)s: %(message)s "
                      "(%(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "rotate_file": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/dev/null",
            "encoding": "utf-8",
            "maxBytes": 10000000,
            "backupCount": 128,
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "asyncio": {
            "level": "WARNING",
        },
        "websockets": {
            "level": "WARNING",
        },
        "paramiko": {
            "level": "WARNING",
        },
        "rallyci.virsh": {
            "level": "DEBUG",
        },
    }
}

logging.config.dictConfig(LOGGING)


def run():
    loop = asyncio.get_event_loop()
    server = hkp.Server()
    loop.run_until_complete(server.start(loop, host="0.0.0.0", port=8080))
    loop.run_forever()


def delete_expired_keys():
    from keyserver.db import File
    db = File("/tmp/t")
    db.expire()
