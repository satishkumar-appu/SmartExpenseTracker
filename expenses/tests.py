from django.test import TestCase
from django.urls import reverse


class ViewSecurityTest(TestCase):

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(
            response.status_code,
            302
        )