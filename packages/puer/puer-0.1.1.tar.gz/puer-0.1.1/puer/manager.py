import argparse
from puer.settings import Settings


__all__ = ['Manager']


class Manager(object):
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description='Manage script for Puer framework')
        self.arg_parser.add_argument('config_name', metavar='config_name', help='configuration name')
        self.main()

    def main(self):
        # settings = Settings.from_yaml(config)
        # self.load_apps(self.settings.apps)
        pass

    def load_apps(self, apps):
        # for module in modules:
        #     for collector in self.collectors:
        #         self.collectors[collector].load_from_module(module)
        pass
