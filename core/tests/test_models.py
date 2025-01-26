from django.test import TestCase
from core.models import Company

class CompanyModelTestCase(TestCase):
    def test_create_company(self):
        company = Company.objects.create(name="ZapSign Test", api_token="example_token")
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(company.name, "ZapSign Test")
        self.assertEqual(company.api_token, "example_token")
