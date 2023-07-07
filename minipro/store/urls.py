from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
router=DefaultRouter()

router.register("prod",ProductVset,basename="prod")
router.register("promv",Productmvset,basename="pmv")
router.register("user",Userset,basename="us")

urlpatterns = [
    path('product',ProductView.as_view()),
    path('product/<int:id>',SpecificProductView.as_view()),
    path('token',views.obtain_auth_token)
]+router.urls
