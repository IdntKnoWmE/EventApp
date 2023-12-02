# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegisterViewSet, EventAuthViewSet, UserInterestViewSet, EventRateViewSet


router = DefaultRouter(trailing_slash=False)
router.register('register', EventRegisterViewSet, basename='register')
router.register('auth', EventAuthViewSet, basename='auth')
router.register('events', EventViewSet, basename='event')
router.register('interest', UserInterestViewSet, basename='interest')
router.register('rate', EventRateViewSet, basename='rate')

urlpatterns = [
    path('', include(router.urls)),
]
