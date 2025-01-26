from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)  # Nome da empresa
    api_token = models.CharField(max_length=255)  # Token da API ZapSign

    def __str__(self):
        return self.name


class Document(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=255)  # Nome do documento
    open_id = models.CharField(max_length=255, blank=True, null=True)  # ID retornado pela ZapSign
    token = models.CharField(max_length=255, blank=True, null=True)  # Token do documento
    status = models.CharField(max_length=50, blank=True, null=True)  # Status do documento
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação
    pdf_path = models.CharField(max_length=500) 
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"


class Signer(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="signers")
    name = models.CharField(max_length=255)  # Nome do signatário
    email = models.EmailField()  # Email do signatário
    status = models.CharField(max_length=50, blank=True, null=True)  # Status do signatário
    signer_token = models.CharField(max_length=255, blank=True, null=True)  # Token associado ao signatário

    def __str__(self):
        return f"{self.name} - {self.email}"
