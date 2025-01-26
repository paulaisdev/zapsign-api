from unittest.mock import patch
from django.test import TestCase
from unittest.mock import patch
from core.models import Company
from core.services.zapsign_service import ZapSignService
from core.services.zapsign_service import ZapSignService

class ZapSignServiceTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="ZapSign Test", api_token="valid_token")

    @patch("core.services.zapsign_service.requests.post")
    def test_create_document_sucess(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "id": "doc_12345",
            "token": "token_12345",
            "status": "Pending"
        }

        response = self.client.post("/api/documents/", {
            "company": self.company.id,
            "name": "Test Document",
            "signers": [
                {"name": "John Doe", "email": "john.doe@example.com"},
                {"name": "Jane Smith", "email": "jane.smith@example.com"}
            ],
            "pdf_path": "./core/tests/assets/TestZapSignBackend.pdf"
        }, format="json")
        self.assertEqual(response.status_code, 201)
    


    @patch("core.services.zapsign_service.open", side_effect=FileNotFoundError)
    def test_create_document_failure(self, mock_open):
        with self.assertRaises(RuntimeError) as context:
            ZapSignService.create_document(
                api_token="invalid_token",
                document_name="Test Document",
                signers=[{"name": "John Doe", "email": "john.doe@example.com"}],
                pdf_path="core/tests/assets/InvalidFile.pdf"
            )
        self.assertIn("PDF file not found", str(context.exception))

