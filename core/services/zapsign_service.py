import requests
import logging
import base64
from django.conf import settings
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class ZapSignService:
    BASE_URL = "https://sandbox.api.zapsign.com.br/api/v1/docs/"
    base64_pdf = None

    @staticmethod
    def create_document(api_token, document_name, signers, pdf_path):
        logger.info("Starting document creation on ZapSign.")
        logger.debug(f"Received parameters: document_name={document_name}, signers={signers}, pdf_path={pdf_path}")
        
        if urlparse(pdf_path).scheme in ("http", "https"):
            try:
                logger.debug(f"Downloading PDF file from URL: {pdf_path}")
                response = requests.get(pdf_path)
                response.raise_for_status()
                base64_pdf = base64.b64encode(response.content).decode("utf-8")
                logger.info("PDF file successfully downloaded and encoded in base64.")
            except requests.RequestException as e:
                logger.error(f"Failed to download PDF file from URL: {pdf_path}. Error: {str(e)}")
                raise RuntimeError(f"Fail to download PDF file: {str(e)}")
        else:
            try:
                logger.debug(f"Reading PDF file from local path: {pdf_path}")
                with open(pdf_path, "rb") as pdf_file:
                    base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
                logger.info("PDF file successfully read and encoded in base64.")
            except FileNotFoundError:
                logger.error(f"PDF file not found: {pdf_path}")
                raise RuntimeError(f"PDF file not found: {pdf_path}")
            except Exception as e:
                logger.error(f"Error processing PDF file: {str(e)}")
                raise RuntimeError(f"Error processing PDF file: {str(e)}")

        url = ZapSignService.BASE_URL
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "name": document_name,
            "signers": [{"name": signer["name"], "email": signer["email"]} for signer in signers],
            "base64_pdf": base64_pdf,
        }

        try:
            logger.debug(f"Sending request to ZapSign API: {url}")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Document created successfully. Response: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error integrating with ZapSign API: {str(e)}")
            raise RuntimeError(f"Error integrating with ZapSign: {e}")
