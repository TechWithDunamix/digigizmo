from rest_framework import serializers
from .models import User,Product,CartItem

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id","email","password","first_name","last_name"]

		write_only_fields = ['password']


	def create(self,validated_data):
		email = validated_data.get("email")
		password = validated_data.get("password")
		first_name = validated_data.get("first_name")
		last_name = validated_data.get("last_name")

		if not email:
			raise serializers.ValidationError("Email is required")

		if not password:
			raise serializers.ValidationError("password is required")

		if not first_name:
			raise serializers.ValidationError("First Name is required")

		if not last_name:
			raise serializers.ValidationError("Lase Name is required")


		user = User.objects.create_user(email = email,password = password,
			first_name = first_name,last_name = last_name)

		return user 

	def validate_password(self,value):
		if len(value) < 8:
			raise serializers.ValidationError("Password is to short")

		return value


	def validate_first_name(self,value):
		return str(value).capitalize()

	def validate_last_name(self,value):
		return str(value).capitalize()


class LoginSerializer(serializers.Serializer):
	email  = serializers.EmailField()
	password = serializers.CharField()

class ProductSerializer(serializers.ModelSerializer):
	category_name = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = ['id','name','description','price','discount','image','category_name']
	def get_category_name(self,instance):
		return instance.category.name 

	def get_image(self,instance):
		request = self.context.get("request")
		url = request.build_absolute_uri(instance.image)
		return url

class CartItemSerializer(serializers.ModelSerializer):
	product = serializers.SerializerMethodField()
	
	total_price = serializers.SerializerMethodField()
	class Meta:
		model = CartItem
		fields = ['id','product','quantity','total_price']


	def get_product(self,instance):
		obj = instance.product
		serializer = ProductSerializer(obj,context = {"request":self.context.get("request")})
		return serializer.data

	

	def get_total_price(self,instance):
		return int(instance.product.price) * int(instance.quantity)

	def to_representation(self,obj):
		to_representation = super().to_representation(obj)
		print(to_representation)
		return to_representation