from django.urls import path
from.views import*

urlpatterns = [
path('reg',Regview.as_view(),name="reg"),
path('lgout',Logoutview.as_view(),name="lgout"),
path('pdet/<int:pid>',Productdetailview.as_view(),name="pdet"),
path('vcart/<int:id>',AddCart.as_view(),name="cart"),
path('cartv',Cartlistview.as_view(),name="cartview"),
path('dcart/<int:id>',deletecart,name="decart"),
path('oderc/<int:cid>',Checkoutview.as_view(),name="orderp"),
path('orderv',Orderview.as_view(),name="vieworder"),
path('delorder/<int:id>',deleteorder,name="delorder")

]