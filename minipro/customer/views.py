from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .forms import Regform,Logform
from django.contrib import messages
from store.models import Product
from customer.models import Cart,Order
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First!!")
            return redirect("login")
    return inner


dec=[signin_required,never_cache]


# Create your views here.
@method_decorator(dec,name="dispatch") 
class home(ListView):
    template_name="home.html"
    model=Product
    context_object_name="data"
    
    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context["data"]=Product.objects.all()
    #     return context

# class Regview(View):
#     def get(self,request):
#         form=Regform()
#         return render(request,"reg.html",{"form":form})
#     def post(self,request):
#         form_data=Regform(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             return redirect("login")
#         else:
#             return render(request,"reg.html",{"form":form_data})
        
        
class Regview(CreateView):
    template_name="reg.html"
    form_class=Regform
    success_url=reverse_lazy("login")     
        

        
        
# class Logview(View):
#     def get(self,request):
#         form=Logform()
#         us=request.user
#         return render(request,"log.html",{"form":form,"user":us})
#     def post(self,request):
#         form_data=Logform(data=request.POST)
#         if form_data.is_valid():
#             user=form_data.cleaned_data.get("username")
#             pswd=form_data.cleaned_data.get("password")
#             user_ob=authenticate(request,username=user,password=pswd)
#             if user_ob:
#                 login(request,user_ob)
#                 messages.success(request,"Login Successfull !!")
#                 return redirect("home")
#             else:
#                 messages.error(request,"Login Failed !! Invalid username and password")
#                 return render(request,"log.html",{"form":form_data})

class Logview(FormView):
    template_name="log.html"
    form_class=Logform
    def post(self,request,*args,**kwargs):
        form_data=Logform(data=request.POST)
        if form_data.is_valid():
            user=form_data.cleaned_data.get("username")
            pswd=form_data.cleaned_data.get("password")
            user_ob=authenticate(request,username=user,password=pswd)
            if user_ob:
                login(request,user_ob)
                messages.success(request,"Login Successfull !!")
                return redirect("home")
            else:
                messages.error(request,"Login Failed !! Invalid username and password")
                return render(request,"log.html",{"form":form_data})
            
            
class Logoutview(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")
 
@method_decorator(dec,name="dispatch")   
class Productdetailview(DetailView):
    template_name="product-details.html"
    model=Product
    context_object_name="product"
    pk_url_kwarg="pid"
    
@method_decorator(dec,name="dispatch")     
class AddCart(View):
    def get(self,request,*args,**kwargs):
        prod=Product.objects.get(id=kwargs.get("id"))
        user=request.user
        Cart.objects.create(product=prod,user=user)
        messages.success(request,"Product added to cart!!!")
        return redirect("home")
    
@method_decorator(dec,name="dispatch") 
class Cartlistview(ListView):
    template_name="cart-list.html"
    model=Cart
    context_object_name="cartitem"
    
    def get_queryset(self):
        cart=Cart.objects.filter(user=self.request.user,status="cart")
        total=Cart.objects.filter(user=self.request.user,status="cart").aggregate(tot=Sum("product__price"))
        return {"items":cart,"total":total}
    
    
# class Cartdelete(View):
dec
def deletecart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    messages.error(request,"cart item removed!!!")
    return redirect("cartview")

@method_decorator(dec,name="dispatch") 
class Checkoutview(View):
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    def post(self,request,*args,**kwargs):
        id=kwargs.get("cid")
        cart=Cart.objects.get(id=id)
        prod=cart.product
        user=request.user
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        Order.objects.create(product=prod,user=user,address=address,phone=phone)
        cart.status="Order Placed"
        cart.save()
        messages.success(request,"Order Placed Successfully!!")
        return redirect("home")
    
@method_decorator(dec,name="dispatch") 
class Orderview(ListView):
    # def get(self,request,*args,**kwargs):
    #     return render(request,"orderview.html")
    template_name="orderview.html"
    model=Order
    context_object_name="orderitem"
    

    def get_queryset(self):
        order=Order.objects.filter(user=self.request.user)
        return {"items":order}
    
dec  
def deleteorder(request,id):
    order=Order.objects.get(id=id)
    order.status="Cancel"
    order.save()
    messages.success(request,"Order Cancelled!!")
    return redirect("vieworder")
    
    

    
    
    
        