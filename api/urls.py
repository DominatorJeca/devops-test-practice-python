from django.urls import path
from .views import UserViewSet
from rest_framework import routers
from .health import liveness, readiness

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('health/', liveness, name='health'),
    path('ready/', readiness, name='ready'),
] + router.urls