from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class MappingSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'patient_details', 'doctor_details', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        if PatientDoctorMapping.objects.filter(patient=data['patient'], doctor=data['doctor']).exists():
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        return data

class PatientDoctorsSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'doctor', 'created_at']
