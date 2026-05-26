from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserMessageSerializer, UserSerializer
from .permissions import IsAdminUserOrUnauthorizedUserOnlyCreate
from users.models import UserMessage
from rest_framework import status


# Create your views here.

class UserMessageView(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrUnauthorizedUserOnlyCreate]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    user = UserSerializer(data=request.data)
    if user.is_valid():
        user.save()
        return Response(
            data={"message": "User was successfully created!"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            data={"message": user.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
