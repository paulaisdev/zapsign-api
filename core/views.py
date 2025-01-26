from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Company, Document, Signer
from .serializers import CompanySerializer, DocumentSerializer, SignerSerializer
from .services.zapsign_service import ZapSignService
import logging

logger = logging.getLogger(__name__)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        company_name = request.data.get("company")
        document_name = request.data.get("name")
        signers = request.data.get("signers", [])
        pdf_path = request.data.get("pdf_path")

        if not all([company_name, document_name, pdf_path]):
            return self._missing_fields_response()

        company = self._get_company_by_name(company_name)
        if not company:
            return self._company_not_found_response(company_name)

        api_response = self._create_document_in_zapsign(company.api_token, document_name, signers, pdf_path)
        if not api_response:
            return Response({"error": "Failed to create document in ZapSign API."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        document = self._save_document_and_signers(company, document_name, api_response, signers, pdf_path)

        serializer = self.get_serializer(document)
        logger.info(f"Document '{document.name}' created successfully with ID: {document.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_company_by_name(self, name):
        try:
            company = Company.objects.get(name=name)
            logger.debug(f"Found company: {company.name} (ID: {company.id})")
            return company
        except Company.DoesNotExist:
            logger.error(f"Company with name '{name}' not found.")
            return None

    def _create_document_in_zapsign(self, api_token, document_name, signers, pdf_path):
        try:
            return ZapSignService.create_document(api_token, document_name, signers, pdf_path)
        except RuntimeError as e:
            logger.error(f"Error integrating with ZapSign: {str(e)}")
            return None

    def _save_document_and_signers(self, company, document_name, api_response, signers, pdf_path):
        document = Document.objects.create(
            company=company,
            name=document_name,
            open_id=api_response.get("id"),
            token=api_response.get("token"),
            status=api_response.get("status"),
            pdf_path=pdf_path
        )
        for signer in signers:
            Signer.objects.create(
                document=document,
                name=signer["name"],
                email=signer["email"],
                status="Pending"
            )
        return document

    def _missing_fields_response(self):
        logger.warning("Missing required fields in the request.")
        return Response(
            {"error": "Missing required fields: company_name, name, or pdf_path"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _company_not_found_response(self, company_name):
        logger.warning(f"Company '{company_name}' not found in the database.")
        return Response(
            {"error": f"Company '{company_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerSerializer
