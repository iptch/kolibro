from django.test import TestCase
from morango.sync.syncsession import SyncSessionClient, NetworkSyncConnection
from morango.models import SyncSession
from morango.sync.controller import MorangoProfileController
from morango.models import Certificate
from . import models
from django.core.management import call_command

class ClientTests(TestCase):
    def test_index(self):
        response = self.client.get('/client/', allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the kolibro index.")
        
    def test_sync_session(self):
        controller = MorangoProfileController("default") # <- This is the profile name defined in kolibro/settings.py
        syncConnection = controller.create_network_connection("http://localhost:8000") # <- This is the URL of the server (you have to start a server)
    
    def test_sync_model(self):
        
        if not ScopeDefinition.objects.filter():
            call_command("loaddata", "scopedefinitions")
            
        self.assertEqual(entry.name, "test")