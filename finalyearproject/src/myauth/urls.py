from django.urls import path
from .views import UserRegistrationView, LoginView, UserLogoutView ,UserDashboardView , AnalyticsViewSet

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='user-login') ,
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('analytics/',AnalyticsViewSet.as_view(),name='analytics'),
    path('dashboard/<int:user_id>/', UserDashboardView.as_view(), name='user-dashboard'),
]