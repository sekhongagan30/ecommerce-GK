from django.urls import path
from userauths import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = "userauths"
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("sign-up", views.RegisterApi.as_view(), name = "sign-up"),
    path("sign-in", views.LoginApi.as_view(), name = "sign-in"),
    path("sign-out", views.logout_view, name = "sign-out"),
    path('token', views.token_send, name="token_send"),
    path('success', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error' , views.error_page , name="error"),
    # user
    path('profile', views.view_profile, name="profile"),
    path('profile/update', views.ProfileUpdateView.as_view(), name="profile-update"),
]