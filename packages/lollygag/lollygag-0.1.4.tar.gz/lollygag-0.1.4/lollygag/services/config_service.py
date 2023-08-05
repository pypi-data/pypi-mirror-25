from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods

DEFAULT_CONFIG = {
    'threads': 10,
    'loglevel': 'all',
    'url': '',
    'skip': [
        r'\.pdf$'
        , r'\.jpg$'
        , r'\.png$'
        , r'\.jpeg$', "^#"
        , r"\.css$"
        , r"\.ico$"
        , r"\.docx?$"
        , r"\.xlsx?$"
    ]
}

class ConfigService(object):
    """
    Stores configuration details
    Parses arguments in argumentParser on construction
    Arguments not in argumentParser will fall back to the DEFAULT_CONFIG
    """
    argumentParser = Inject("argparse", HasMethods("add_argument", "parse_args"))

    def __init__(self):
        self.reset()

    def reset(self):
        self.__init_args()
        self.__dict__ = self.__parse_args()

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
        self.argumentParser.add_argument("--url", "-u", \
            help="Base url you wish to crawl", required=False)
        self.argumentParser.add_argument("--threads", "-t", \
            help="Maximum number of concurrent threads", required=False)
        self.argumentParser.add_argument("--loglevel", "-l", \
            help="Level of logging, possible values = [all, info, debug, warn, error, none]"\
            , required=False)
        self.argumentParser.add_argument("--skip", "-s", \
            help="Regex patterns, when any of them is found in the url, it's skipped"\
            , required=False)
