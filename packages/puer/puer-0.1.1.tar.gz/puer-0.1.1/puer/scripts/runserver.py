import logging
from sys import modules
from importlib import import_module

from aiohttp.web import run_app

from motor.motor_asyncio import AsyncIOMotorClient

import jinja2
import aiohttp_jinja2

from ..core import AbstractScript
from ..application import Application
from ..umongo_instance import uMongoInstance
from ..route import routes


class RunServer(AbstractScript):
    def main(self):
        logging.basicConfig(level=logging.DEBUG)

        settings = self.manager.settings

        # Init database and ODM instance
        db = AsyncIOMotorClient(
            settings.db["ip"],
            settings.db["port"]
        )
        uMongoInstance().init(
            getattr(db, settings.db["name"])
        )

        # Setting middlewares for app
        middlewares = []
        for middleware in settings.middlewares:
            middleware_path = middleware.split('.')
            package_name = '.'.join(middleware_path[:-1])
            middleware_name = middleware_path[-1:][0]
            import_module(package_name)
            middlewares.append(getattr(modules[package_name], middleware_name))

        self.manager.aiohttp_app = Application(
            middlewares=middlewares
        )

        # Setting signals for app
        for signal in settings.signals:
            app_signals = getattr(self.manager.aiohttp_app, signal)
            for app_signal in settings.signals[signal]:
                app_signal_path = app_signal.split('.')
                package_name = '.'.join(app_signal_path[:-1])
                app_signal_name = app_signal_path[-1:][0]
                import_module(package_name)
                app_signals.append(getattr(modules[package_name], app_signal_name))

        # Setting routes for app
        for res in routes:
            name = res[3]
            self.manager.aiohttp_app.router.add_route(res[0], res[1], res[2], name=name)
        aiohttp_jinja2.setup(self.manager.aiohttp_app, loader=jinja2.FileSystemLoader('templates'))

        if settings.serve_static:
            self.manager.aiohttp_app.router.add_static(
                '/static/',
                path='static',
                name='static'
            )

        run_app(
            self.manager.aiohttp_app,
            host=settings.host["ip"],
            port=settings.host["port"]
        )
