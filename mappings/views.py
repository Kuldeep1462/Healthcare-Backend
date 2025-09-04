from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PatientDoctorMapping
from .serializers import MappingSerializer, PatientDoctorsSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Doctor successfully assigned to patient",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )


class MappingDetailView(generics.RetrieveDestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        patient_name = instance.patient.name
        doctor_name = instance.doctor.name
        self.perform_destroy(instance)
        return Response(
            {"message": f"Doctor '{doctor_name}' removed from patient '{patient_name}'"},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": f"Doctor '{serializer.data.get('name')}' updated successfully",
             "data": serializer.data}, status=status.HTTP_200_OK
        )


class PatientDoctorsView(generics.ListAPIView):
    serializer_class = PatientDoctorsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        return PatientDoctorMapping.objects.filter(patient_id=patient_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Get patient info for context
        if queryset.exists():
            patient = queryset.first().patient
            patient_info = {
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender
            }
        else:
            patient_info = None
        
        return Response({
            'patient': patient_info,
            'assigned_doctors': serializer.data,
            'total_doctors': queryset.count()
        })
