from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])  # 모든 사용자에게 허용
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response("Login Successful", status=status.HTTP_200_OK)
    else:
        return Response("Invalid username or password", status=status.HTTP_401_UNAUTHORIZED)

# 로그아웃
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response("Logged out successfully", status=status.HTTP_200_OK)

# 회원 가입
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 본인 정보 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        # Only allow users to update their own profile
        if user == request.user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not authorized to update this profile", status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

# 패스워드 변경
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.data)
    if form.is_valid():
        user = form.save()
        # Updating the user's session to prevent them from being logged out after a password change
        update_session_auth_hash(request, user)
        return Response("Password changed successfully", status=status.HTTP_200_OK)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원 탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    # 비밀번호 확인
    if 'password' not in request.data:
        return Response("Password is required for account deletion", status=status.HTTP_400_BAD_REQUEST)
    password = request.data['password']
    if not request.user.check_password(password):
        return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)
    
    # 비밀번호 확인 후 계정 삭제
    request.user.delete()
    return Response("Account deleted successfully", status=status.HTTP_204_NO_CONTENT)
