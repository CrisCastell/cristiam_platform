from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from .views import *

app_name = 'accounts'

# define the router
router = routers.DefaultRouter()


router.register(r'accounts', AccountDetail, basename="account")
router.register(r'register', RegisterView, basename="register")
router.register(r'password', ChangePasswordView, basename="password")
urlpatterns = [
    path('', include(router.urls)),
    path('login'   , obtain_auth_token , name="login"),
    path('image', accountImage, name="image"),
    path('get-id', getUserID, name="get-id")
]