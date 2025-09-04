from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Doctor '{instance.name}' deleted successfully"},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()

        original_values = {field: getattr(instance, field, None) for field in [
            'name', 'specialization'
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
