import logging
from sys import modules
from importlib import import_module, util

from aiohttp.web import run_app

from ..core import AbstractScript
from ..application import Application
from ..route import routes


class RunServer(AbstractScript):
    def main(self):
        settings = self.manager.settings
        logging.basicConfig(level=logging.DEBUG)

        # Setting middlewares for app
        middlewares = []
        for middleware in settings.middlewares:
            middleware_path = middleware.split('.')
            package_name = '.'.join(middleware_path[:-1])
            middleware_name = middleware_path[-1:][0]
            import_module(package_name)
            middlewares.append(getattr(modules[package_name], middleware_name))

        app = Application(
            middlewares=middlewares
        )
        app["settings"] = settings
        print(settings.modules)
        for m in settings.modules:
            module_splitted = m.split('.')
            package_name = module_splitted[0:-1]
            module_cls = module_splitted[-1]
            print(package_name)
            import_module(package_name)
            if util.find_spec(package_name) is not None:
                import_module(package_name)
                c = getattr(modules[package_name], module_cls)
                if c is not None:
                    mod = c()
                    app[mod.name] = mod.value

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

        run_app(
            app,
            loop=self.manager.loop,
            host=settings.host["ip"],
            port=settings.host["port"]
        )
