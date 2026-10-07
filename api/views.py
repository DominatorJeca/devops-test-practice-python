from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        data = request.data

        if self.get_queryset().filter(dni=data.get('dni', '')).exists():
            return Response({'detail': 'User already exists'}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)