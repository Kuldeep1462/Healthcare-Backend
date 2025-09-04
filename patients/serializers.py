from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'address', 'mobile_no', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_mobile_no(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits")
        return value
