"""
Holds the ConfigService service.
"""
from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods

DEFAULT_CONFIG = {
    'threads': 10,
    'loglevel': 'all',
    'urls': '',
    'skip': [
        r'\.pdf$',
        r'\.jpg$',
        r'\.png$',
        r'\.jpeg$',
        "^#",
        r"\.css$",
        r"\.ico$",
        r"\.docx?$",
        r"\.xlsx?$"
    ]
}


class ConfigService(object):
    """
    Stores configuration details.
    Parses arguments in argumentParser on construction.
    Arguments not in argumentParser will fall back to the DEFAULT_CONFIG.
    Implements the Borg pattern so all instances share state with the class itself.
    """
    argumentParser = Inject("argparse", HasMethods("add_argument", "parse_args"))
    state = {}

    threads = DEFAULT_CONFIG['threads']
    loglevel = DEFAULT_CONFIG['loglevel']
    urls = DEFAULT_CONFIG['urls']
    skip = DEFAULT_CONFIG['skip']

    def __init__(self):
        self.__dict__ = ConfigService.state

    def setup(self):
        """
        Initialize ConfigService.state if it hasn't been already.
        Parses args from the standard input.
        """
        if not ConfigService.state:
            self.__init_args()
            args = self.__parse_args()
            for key in args:
                ConfigService.state[key] = args[key]

    def __parse_args(self):
        arguments = self.argumentParser.parse_args()
        config = {}
        for key in DEFAULT_CONFIG:
            attr = getattr(arguments, key, None)
            if attr:
                config[key] = attr
            else:
                config[key] = DEFAULT_CONFIG[key]
        return config

    def __init_args(self):
        helps = {
            'urls': "Base url(s) you wish to crawl",
            'threads': "Maximum number of concurrent threads",
            'loglevel': "Level of logging [all, info, debug, warn, error, none]",
            'skip': "Regex patterns, when any of them is found in the url, it's skipped"
        }
        self.argumentParser.add_argument("--urls", "-u", nargs="+",
                                         help=helps['urls'],
                                         required=False)
        self.argumentParser.add_argument("--threads", "-t",
                                         help=helps['threads'],
                                         required=False)
        self.argumentParser.add_argument("--loglevel", "-l",
                                         help=helps['loglevel'],
                                         required=False)
        self.argumentParser.add_argument("--skip", "-s",
                                         help=helps['skip'],
                                         required=False)
