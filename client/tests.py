from django.test import TestCase
from morango.sync.syncsession import SyncSessionClient, NetworkSyncConnection
from morango.models import SyncSession
from morango.sync.controller import MorangoProfileController

class ClientTests(TestCase):
    def test_index(self):
        response = self.client.get('/client/', allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the kolibro index.")
        
    def test_sync_session(self):
        controller = MorangoProfileController("default") # <- This is the profile name defined in kolibro/settings.py
        syncConnection = controller.create_network_connection("http://localhost:8000") # <- This is the URL of the server (you have to start a server)