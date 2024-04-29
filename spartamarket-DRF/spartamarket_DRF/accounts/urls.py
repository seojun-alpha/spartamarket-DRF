from django.urls import path
from accounts.views import register_user, login_user  # user_profile은 더 이상 사용되지 않음

urlpatterns = [
    path('', register_user),  # 빈 경로에 대한 처리 추가
    path('api/accounts/', register_user),
    path('api/accounts/login/', login_user),
]
