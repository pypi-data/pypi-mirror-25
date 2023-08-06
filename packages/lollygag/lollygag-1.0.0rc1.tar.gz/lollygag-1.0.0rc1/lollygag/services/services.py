"""
This module is used to manage Services in the application.
Override services in Services to customize functionality.
Inits Services in Inject on import so the services
are usable as dependencies
before calling register_services explicitly.
"""
import sys
import argparse
import threading
import requests
from lollygag.core.parsers.link_parser import LinkParser
from lollygag.core.crawlers.domain_crawler import DomainCrawler
from lollygag.services.config_service import ConfigService
from lollygag.services.print_service import PrintService
from lollygag.services.work.work_service import WorkService
from lollygag.dependency_injection.inject import Inject
try:
    import Queue
except ImportError:
    import queue as Queue


class Services(object):
    """
    Holds the names and default values of the application's services.
    Implements the Borg pattern, so all instances share the same state with the class itself.
    """
    # pylint: disable=too-few-public-methods
    requests = requests
    site_parser_factory = LinkParser
    argparse = argparse.ArgumentParser
    config_service = ConfigService
    log_service = PrintService
    work_service = WorkService
    threading = threading
    queue = Queue.Queue
    logging_output = sys.stdout
    crawler_factory = DomainCrawler

    def __init__(self):
        self.__dict__ = Services.__dict__


def register_services(services=None):
    """
    Register the services in dependency_injection.Inject.
    If services is None the Services class is used.
    """
    assert services is dict or services is None
    if not services:
        services = Services.__dict__
    Inject.register_features(**services)


register_services()
