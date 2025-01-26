from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Company

class DocumentAPITestCase(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="ZapSign Test", api_token="valid_token")
        self.valid_payload = {
            "company": self.company.id,
            "name": "Test Document",
            "signers": [
                {"name": "John Doe", "email": "john.doe@example.com"},
                {"name": "Jane Smith", "email": "jane.smith@example.com"}
            ],
            "pdf_path": "./core/tests/assets/TestZapSignBackend.pdf"
        }

    @patch("core.services.zapsign_service.ZapSignService.create_document")
    def test_create_document(self, mock_create_document):
        # Configura o retorno do mock
        mock_create_document.return_value = {
            "id": "doc_12345",
            "token": "token_12345",
            "status": "Pending"
        }

        response = self.client.post("/api/documents/", self.valid_payload, format="json")

        # Valida o retorno esperado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["id"], 1)


        # Verifica se o mock foi chamado com os argumentos corretos
        mock_create_document.assert_called_once_with(
            "valid_token",
            "Test Document",
            [
                {"name": "John Doe", "email": "john.doe@example.com"},
                {"name": "Jane Smith", "email": "jane.smith@example.com"}
            ],
            "./core/tests/assets/TestZapSignBackend.pdf"
        )
