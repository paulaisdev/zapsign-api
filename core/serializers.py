from rest_framework import serializers
from .models import Company, Document, Signer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'api_token']

class DocumentSerializer(serializers.ModelSerializer):
    signers = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Document
        fields = ['id', 'company', 'name', 'open_id', 'token', 'status', 'created_at', 'signers', 'pdf_path']
        read_only_fields = ['open_id', 'token', 'created_at']

    def create(self, validated_data):
        validated_data.pop("signers", None)  # Signers serão tratados no ViewSet
        return super().create(validated_data)


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ['id', 'document', 'name', 'email', 'status', 'signer_token']
        read_only_fields = ['signer_token']
