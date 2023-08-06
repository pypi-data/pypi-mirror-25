import signal
import time
import requests
from js9 import j


class Grafana:
    def __init__(self, container, ip, port, url):
        self.container = container
        self.ip = ip
        self.port = port
        self.url = url
        self.client = j.clients.grafana.get(url='http://%s:%d' % (
            ip, port), username='admin', password='admin')

    def apply_config(self):
        f = self.container.client.filesystem.open('/opt/grafana/conf/defaults.ini')
        try:
            template = self.container.client.filesystem.read(f)
        finally:
            self.container.client.filesystem.close(f)

        template = template.replace(b'3000', str(self.port).encode())
        if self.url:
            template = template.replace(b'root_url = %(protocol)s://%(domain)s:%(http_port)s/', b'root_url = %s' % self.url.encode())
        self.container.client.filesystem.mkdir('/etc/grafana/')
        self.container.upload_content('/etc/grafana/grafana.ini', template)

    def is_running(self):
        for process in self.container.client.process.list():
            if 'grafana-server' in process['cmdline']:
                    return True, process['pid']
        return False, None

    def stop(self, timeout=30):
        is_running, pid = self.is_running()
        if not is_running:
            return

        self.container.client.process.kill(pid, signal.SIGTERM)
        start = time.time()
        end = start + timeout
        is_running, _ = self.is_running()
        while is_running and time.time() < end:
            time.sleep(1)
            is_running, _ = self.is_running()

        if is_running:
            raise RuntimeError('Failed to stop grafana.')

        if self.container.node.client.nft.rule_exists(self.port):
            self.container.node.client.nft.drop_port(self.port)

    def start(self, timeout=30):
        is_running, _ = self.is_running()
        if is_running:
            return

        self.apply_config()

        if not self.container.node.client.nft.rule_exists(self.port):
            self.container.node.client.nft.open_port(self.port)

        self.container.client.system(
            'grafana-server -config /etc/grafana/grafana.ini -homepath /opt/grafana')
        time.sleep(1)

        start = time.time()
        end = start + timeout
        is_running, _ = self.is_running()
        while not is_running and time.time() < end:
            time.sleep(1)
            is_running, _ = self.is_running()

        if not is_running:
            if self.container.node.client.nft.rule_exists(self.port):
                self.container.node.client.nft.drop_port(self.port)
            raise RuntimeError('Failed to start grafana.')

    def add_data_source(self, database, name, ip, port, count):
        data = {
            'type': 'influxdb',
            'access': 'proxy',
            'database': database,
            'name': name,
            'url': 'http://%s:%u' % (ip, port),
            'user': 'admin',
            'password': 'passwd',
            'default': True,
        }

        now = time.time()
        while time.time() - now < 10:
            try:
                self.client.addDataSource(data)
                if len(self.client.listDataSources()) == count + 1:
                    continue
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                pass

    def delete_data_source(self, name):
        count = len(self.client.listDataSources())
        now = time.time()
        while time.time() - now < 10:
            try:
                self.client.deleteDataSource(name)
                if len(self.client.listDataSources()) == count - 1:
                    continue
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                pass
