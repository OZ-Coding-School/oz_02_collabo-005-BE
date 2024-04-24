from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            name = serializer.validated_data['name']
            phone_number = serializer.validated_data['phone_number']
            birthday = serializer.validated_data.get('birthday')

            # 일반 사용자 생성
            user = User.objects.create_user(email=email, password=password, name=name, phone_number=phone_number, birthday=birthday)

            # 혹은 슈퍼유저 생성
            # user = User.objects.create_superuser(email=email, password=password, name=name, phone_number=phone_number, birthday=birthday)
            
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailCheckView(APIView):
    def get(self, request):
        email = request.GET.get('email', None)
        
        if email:
            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                return JsonResponse({"email": email, "exists": True}) # 중복 이메일이 있을시
            else:
                return JsonResponse({"email": email, "exists": False}) # 중복 이메일이 없을시
        else:
            return JsonResponse({"error": "Email parameter is missing"}, status=400)
    