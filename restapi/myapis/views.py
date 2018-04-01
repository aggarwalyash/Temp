from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.filters import (
        SearchFilter,OrderingFilter,
    )
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,DestroyAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly,
    )
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .models import *

User = get_user_model()

from .serializers import (
    UserCreateSerializer,UserLoginSerializer,UsersSerializer,ProfileCreateUpdateSerializer
    )

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UsersAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    # def get(self,request):
    #     users = User.objects.all()
    #     serializer = UsersSerializer(users,many=True)
    #     return Response(serializer.data,status=HTTP_200_OK)

class ProfileCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateUpdateSerializer
