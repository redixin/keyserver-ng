import asyncio
import configparser
import importlib
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
        "file": {
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
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
        "asyncio": {
             "level": "WARNING",
        }
    }
}


def run():
    import sys
    if len(sys.argv) < 2:
        filename = "/etc/keyserver-ng/config.ini"
    else:
        filename = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(filename)
    log_cfg = config["logging"]
    LOGGING["handlers"]["file"]["level"] = log_cfg["level"]
    LOGGING["handlers"]["file"]["filename"] = log_cfg["file"]
    LOGGING["handlers"]["file"]["maxBytes"] = int(log_cfg["rotate_bytes"])
    LOGGING["handlers"]["console"]["level"] = log_cfg["console_level"]
    if not config.getboolean("logging", "log_console"):
        LOGGING["loggers"][""]["handlers"] = ["file"]

    logging.config.dictConfig(LOGGING)

    db_module = importlib.import_module(config["database"]["module"])
    db = db_module.DB(**config["database"])
    server = hkp.Server(db)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
            server.start(loop,
                         host=config["keyserver"]["listen_addr"],
                         port=config["keyserver"]["listen_port"],
                         )
    )
    loop.run_forever()


def delete_expired_keys():
    from keyserver.db import File
    db = File("/tmp/t")
    db.expire()
