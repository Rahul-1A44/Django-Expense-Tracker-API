from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import ExpenseIncomeViewSet, UserRegistrationView, api_root_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expense')

urlpatterns = [
    path('', api_root_view, name='api_root'), 

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/auth/register/', UserRegistrationView.as_view(), name='register_user'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]