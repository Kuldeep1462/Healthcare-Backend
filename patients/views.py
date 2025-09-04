from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Patient
from .serializers import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Patient.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Patient '{instance.name}' deleted successfully"},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        original_values = {field: getattr(instance, field, None) for field in [
            'name', 'age', 'gender', 'address', 'mobile_no'
        ]}

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        changed_fields = []
        for field, new_value in serializer.validated_data.items():
            if field in original_values and original_values[field] != new_value:
                changed_fields.append(field)

        self.perform_update(serializer)

        if not changed_fields:
            message = "No changes detected"
        elif len(changed_fields) == 1:
            message = f"{changed_fields[0]} updated successfully"
        else:
            message = f"Fields updated successfully: {', '.join(changed_fields)}"

        return Response(
            {"message": message, "data": serializer.data},
            status=status.HTTP_200_OK
        )
