from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register('tasks',views.TaskViewSet)
router.register('users',views.UserViewSet, basename='users')
# router.register('users',views.UserRegistrationViewset, basename= 'registration')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
]