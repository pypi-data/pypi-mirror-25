import random
import threading

class ProxyManager(object):
    def __init__(self, proxy_file_path):
        self.proxies = self.load_proxies_from_file(proxy_file_path)
        self.lock = threading.Lock()
        self.proxy_number = 0
        
    @staticmethod
    def load_proxies_from_file(proxy_file_path):
        proxies = []
        with open(proxy_file_path) as proxy_file:
            for line in proxy_file.readlines():
                proxies.append(Proxy(line))
        return proxies or [Proxy()]

    def random_proxy(self):
        return random.choice(self.proxies)

    def next_proxy(self):
        if self.proxy_number >= len(self.proxies):
            self.proxy_number = 0

        with self.lock:
            proxy = self.proxies[self.proxy_number]
            self.proxy_number += 1
            return proxy

class Proxy(object):
    def __init__(self, proxy_line=None):
        if proxy_line:
            split_line = proxy_line.strip('\n').split(':')

            self.ip = split_line[0]
            self.port = split_line[1]
            self.full_proxy = '{0}:{1}'.format(self.ip, self.port)

            # If has username/password
            self.is_auth = len(split_line) == 4
            if self.is_auth:
                self.username = split_line[2]
                self.password = split_line[3]
                self.full_proxy = '{0}:{1}@{2}'.format(self.username, self.password, self.full_proxy)
        else:
            self.full_proxy = None

    def get_dict(self):
        return {
            'http': 'http://{}'.format(self.full_proxy),
            'https': 'https://{}'.format(self.full_proxy)
        } if self.full_proxy else { }
