from django.shortcuts import render
from .serializers import Productmodelserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

# Create your views here.

class ProductView(APIView):
    def get(self,request):
        prod=Product.objects.all()
        dser=Productmodelserializer(prod,many=True)
        return Response(data=dser.data) 
    def post(self,request):
        ser=Productmodelserializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"OK"})
        return Response(data=ser.errors)
    
    
class SpecificProductView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        dser=Productmodelserializer(prod)
        return Response(data=dser.data)  
    def delete(self,requst,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        prod.delete()
        return Response({"msg":"Deleted"})
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        ser=Productmodelserializer(data=request.data,instance=prod)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"Updated"})
        return Response(data=ser.errors)
    
    
class ProductVset(ViewSet):
    def retrieve(self,request,*args, **kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        dser=Productmodelserializer(prod)
        return Response(data=dser.data)
    def list(self,request):
        prodlist=Product.objects.all()
        dser=Productmodelserializer(prodlist,many=True)
        return Response(data=dser.data)
    def create(self,request):
        ser=Productmodelserializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        return Response(data=ser.errors)
    def update(self,request,*args, **kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        ser=Productmodelserializer(data=request.data,instance=prod)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        return Response(data=ser.errors)
    def destroy(self,request,*args, **kwargs):
        pid=kwargs.get("pk")
        prod=Product.objects.get(id=pid)
        prod.delete()
        return Response({"msg":"DELETED"})
    
    
    @action(methods=["GET"],detail=False)
    def category(self,request,*args, **kwargs):
        cat=Product.objects.values_list("category",flat=True).distinct()
        return Response(data=cat)
    
    
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

class Productmvset(ModelViewSet):
    serializer_class=Productmodelserializer
    queryset=Product.objects.all()
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    
    
class Userset(ViewSet):
    def create(self,request):
        ser=UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"created"})
        return Response({"msg":"Failed"})
    
    
    
                
              


