from django.shortcuts import get_object_or_404
from .models import User,Product,CartItem
from .serializers import UserRegisterSerializer,LoginSerializer,ProductSerializer,CartItemSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
class ProductPagination(PageNumberPagination):
	page_size = 24
class UserRegisterView(GenericAPIView,CreateModelMixin):
	authentication_classes =  []
	permission_classes = [AllowAny]
	serializer_class = UserRegisterSerializer
	queryset = User.objects.all()


	def post(self,request,*args,**kwargs):
		serializer = UserRegisterSerializer(data = request.data)

		if serializer.is_valid():
			user = serializer.create(serializer.data)
			token,_ = Token.objects.get_or_create(user = user)
			response = serializer.data
			response['token'] = token.key
			response['confirmed'] = user.is_confirmed
			return Response(response,status = status.HTTP_201_CREATED)

		response = serializer.errors
		return Response(response,status = status.HTTP_400_BAD_REQUEST)




class UserLogin(GenericAPIView):
	authentication_classes = []
	permission_classes = [AllowAny]
	serializer_class = LoginSerializer
	queryset = User.objects.all()

	def post(self,request,*args,**kwargs):

		serializer = self.get_serializer_class()(data = request.data)
		if serializer.is_valid():
			user = authenticate(email = serializer.data.get("email"),password = serializer.data.get("password"))
			if not user:
				return Response({"error":"Invalid user credentials"},status = status.HTTP_400_BAD_REQUEST)
			token,_ = Token.objects.get_or_create(user = user)
			return Response({"detail":"Login successfull",'token':token.key,'email':request.data.get("email"),'confirmed':user.is_confirmed},status = status.HTTP_200_OK)

		return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class ProductView(GenericAPIView):
	authentication_classes = []
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	pagination_class = ProductPagination
	
	def get(self,request,id = None,*args,**kwargs):
		if not id:
			q = request.GET.get("q")
			qs = self.get_queryset().filter(instock = True).all()
			if q:
				qs = qs.filter(name__icontains = q).order_by("?").all()
			paginated_qs = self.paginator.paginate_queryset(qs, self.request, view=self)
			serializer = self.get_serializer_class()(instance = paginated_qs,context = {"request":request},many = True)
			data = serializer.data
			response = self.paginator.get_paginated_response(data)
			# print(response.json())
			return response
			# return Response(response,status = status.HTTP_200_OK)

		if id:
			qs = get_object_or_404(Product,id = id)
			serializer = self.get_serializer_class()(instance = qs,context = {"request":request})
			response = serializer.data
			return Response(response,status = status.HTTP_200_OK)



class CartView(GenericAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	# serializer_class = CartSerializer
	queryset = Product.objects.all()

	def get(self,request,*args,**kwargs):
		cart_qs = CartItem.objects.filter(user = request.user,ordered = False).all()
		if not cart_qs.exists():
			response = {"detail":"Your Cart is empty"}
			return Response(response,status = status.HTTP_404_NOT_FOUND)
		serializer = CartItemSerializer(cart_qs,many = True,context = {"request":request})
		product = [x.product for x in cart_qs]
		prices = [x.price for x in product]
		price = sum(prices)
		response = serializer.data
		response = {"cart_items":serializer.data,
					"total_price":price,'confirmed':request.user.is_confirmed}
		return Response(response,status = status.HTTP_200_OK)



	def post(self,request,product_id,*args,**kwargs):
		product = get_object_or_404(Product,id = product_id)
		cart_item,created = CartItem.objects.get_or_create(user = request.user,product = product)
		if not created:
			CartItem.objects.create(user = request.user,product = product)
		response = {"detail":"success"}
		return Response(response,status = status.HTTP_201_CREATED)

	def put(self,request,product_id,*args,**kwargs):
		quantity = request.data.get("quantity")
		product = get_object_or_404(Product,id = product_id)
		cart_item = CartItem.objects.get(user = request.user,product = product)
		cart_item.quantity = quantity
		cart_item.save()
		response = {"detail":"success"}
		return Response(response,status = status.HTTP_201_CREATED)

	def delete(self,request,product_id,*args,**kwargs):

		product = get_object_or_404(Product,id = product_id)
		cart_item = CartItem.objects.get(user = request.user,product = product)
		cart_item.delete()
		response = {"detail":"success"}
		return Response(response,status = status.HTTP_200_OK)
		
		

class Order(GenericAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = CartItem.objects.all()

	def post(self,request,*args,**kwargs):
		qs = request.user.cart_items.all()
		for new_qs in qs:
			new_qs.ordered = True
			new_qs.save()

		response = {"detail":"success"}
		return Response(response,status = status.HTTP_200_OK)
