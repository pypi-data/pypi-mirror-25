import re
import os
import sys
import subprocess
from unittest import TestCase


def parse_crawler_output(output, pattern=None):
    result = {
        'errors': [],
        'results': [],
        'custom': []
    }
    for line in output.split('\n'):
        if '[Error]' in line:
            info = re.sub(r'\[Error\]Thread=\[WSc\[\d+\]--\d+\][  ]*', '', line)
            result['errors'].append(info)
        elif pattern and re.search(pattern, line):
            result['custom'].append(line)
        else:
            finds = re.search(r'Link=\[(.*)\] StatusCode=\[(.*)\] Size=\[(.*)\]', line)
            if finds:
                result['results'].append((finds.group(1), finds.group(2), finds.group(3)))
    return result


class CrawlerTest(TestCase):
    IS_WINDOWS = sys.platform.startswith("win")

    @classmethod
    def setUpClass(cls):
        uris = [cls.URI] if not isinstance(cls.URI, list) else cls.URI
        commands = [os.path.join(cls.HERE, "crawler_example.py"), "-u"] + uris
        print("Commands:", commands)
        crawler_process = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=cls.IS_WINDOWS)
        (output, error) = crawler_process.communicate()
        print(output, error)
        cls.output = output.decode("utf-8") if output else ""
        cls.results = parse_crawler_output(cls.output, r'boi')
