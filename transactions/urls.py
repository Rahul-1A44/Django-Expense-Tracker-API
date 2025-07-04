from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExpenseIncomeViewSet

router = DefaultRouter()
router.register('expenses', ExpenseIncomeViewSet, basename='expenses')

urlpatterns = router.urls
