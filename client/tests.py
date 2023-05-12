from django.test import TestCase

class ClientTests(TestCase):
    def test_index(self):
        response = self.client.get('/client/', allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the kolibro index.")
