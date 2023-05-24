from django.test import TestCase
from morango.sync.controller import MorangoProfileController
from morango.models import Certificate, Filter, ScopeDefinition, SharedKey, SyncSession
from django.test.utils import override_settings
from . import models
import os
import socket
import subprocess
import time
import contextlib
from functools import wraps
import requests
import mock
import json
import uuid

from django.conf import settings
from django.test import TestCase
from django.db import connections
from requests.exceptions import RequestException
from django.test.testcases import LiveServerTestCase
from morango.models.certificates import Key
from morango.api.viewsets import CertificateViewSet
from morango.apps import syncable_models
SERVERS = {
    "a": "kolibro.settings",
    "b": "kolibro.settings",
}

TESTAPP_RELATIVE_PATH = "./"

def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port

class TestAppServer(object):
    def __init__(self, autostart=True, settings="settings"):
        self.env = os.environ.copy()
        self.env["DJANGO_SETTINGS_MODULE"] = settings
        self.port = get_free_tcp_port()
        self.addr = "0.0.0.0:{}".format(self.port)
        self.baseurl = "http://127.0.0.1:{}".format(self.port)
        self._setup_database()
        if autostart:
            self.start()

    def _setup_database(self):
        subprocess.check_call(
            ["python", "manage.py", "migrate"],
            cwd=TESTAPP_RELATIVE_PATH,
            env=self.env,
        )

    def start(self):
        self._instance = subprocess.Popen(
            ["python", "manage.py", "runserver", str(self.addr)],
            cwd=TESTAPP_RELATIVE_PATH,
            env=self.env,
        )
        self._wait_for_server_start()

    def _wait_for_server_start(self, timeout=20):
        for i in range(timeout * 2):
            try:
                resp = requests.get(self.baseurl + "/api/morango/v1/morangoinfo/1/", timeout=3)
                if resp.status_code > 0:
                    return
            except RequestException:
                pass
            time.sleep(0.5)

        raise Exception("Server did not start within {} seconds".format(timeout))

    def kill(self):
        with contextlib.suppress(OSError):
            self._instance.kill()

class Setup(object):
    def __enter__(self):
        self.servers = {
            name: TestAppServer(settings=settings) for name, settings in SERVERS.items()
        }
        return self.servers

    def __exit__(self, typ, val, traceback):
        for server in self.servers.values():
            server.kill()

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            assert "servers" not in kwargs

            with self as servers:
                kwargs["servers"] = servers
                return f(*args, **kwargs)

        return wrapper
    
class PerformanceTest(TestCase):
    
    @Setup()
    def test_stuff(self, servers):
        a = servers['a']
        b = servers['b']
        resp = requests.get(servers["a"].baseurl + "/api/morango/v1/morangoinfo/1/", timeout=3)
        self.assertEqual(resp.status_code, 200)
        
        

class ClientTests(TestCase):
    def setUp(self):
        self.root_cert = Certificate.generate_root_certificate("server")
        
        self.subset_cert = Certificate(
            parent=self.root_cert,
            profile="default",
            scope_definition=ScopeDefinition.objects.get(id="server"),
            scope_version=1,
            scope_params=json.dumps(
                {"dataset_id": self.root_cert.id}
            ),
            private_key=Key(),
        )
        self.root_cert.sign_certificate(self.subset_cert)
        self.subset_cert.save()
        
    def test_sync_session(self):
        controller = MorangoProfileController("default") # <- This is the profile name defined in kolibro/settings.py
        syncConnection = controller.create_network_connection("http://localhost:8000") # <- This is the URL of the server (you have to start a server)        

        remote_cert = syncConnection.get_remote_certificates(primary_partition="3a829e806aac3ccc88cc278155e24011")[0]

        # local = syncConnection.push_signed_client_certificate_chain(root, models.SyncEntry.ScopeDefinitions.SERVER, {})
        signedRoot = syncConnection.certificate_signing_request(
            remote_cert, "server", {"dataset_id": remote_cert.id}, userargs={ "username": "smu" }, password="opensource4good"
        )
        # syncConnection.push_signed_client_certificate_chain(self.signedRoot, "server", {"dataset_id": "3a829e806aac3ccc88cc278155e24011"})
        syncSession = syncConnection.create_sync_session(signedRoot, remote_cert)
        
        pull = syncSession.get_pull_client()
        #push = syncSession.get_push_client()
        
        scope_def = ScopeDefinition.objects.get(id="server")
        scope = scope_def.get_scope({"dataset_id": remote_cert.id})
        
        pull.initialize(sync_filter=scope.write_filter)
    
    def test_sync_model(self):
        entry = models.SyncEntry.objects.create(name="test")
        self.assertEqual(entry.name, "test")