import os
import signal
import socket
import sys
import time
import pytest
from app.settings import PROJECT_ROOT


TEST_APP_PORT = 5050


@pytest.fixture(scope='session')
def test_server(xprocess, request):
    def preparefunc(cwd):
        def check_port():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for i in range(10):
                result = sock.connect_ex(('127.0.0.1', TEST_APP_PORT))
                if result == 0:
                    return True
                time.sleep(1)
            return False

        os.environ['APP_PORT'] = str(TEST_APP_PORT)
        application_path = os.path.join(PROJECT_ROOT, 'server.py' )
        return (check_port, [sys.executable, application_path])

    pid, log = xprocess.ensure('server.py', preparefunc, restart=True)

    def fin():
        os.kill(pid, signal.SIGKILL)
    request.addfinalizer(fin)

    def get_url(url):
        return 'http://localhost:%s%s' % (TEST_APP_PORT, url)

    return get_url
