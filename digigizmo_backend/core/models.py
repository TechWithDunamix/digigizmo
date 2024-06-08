from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import uuid

class UserManager(BaseUserManager):
	def create_user(self,email = None,first_name = None,last_name = None,password = None,**kwargs):
		if not email:
			raise ValueError("Email is a required field")
		if not first_name:
			raise ValueError("first_name is a required field")
		if not last_name:
			raise ValueError("last_nameis a required field")
		if not password:
			raise ValueError("password is a required field")

		user = self.model(email = email,first_name = first_name,last_name = last_name,**kwargs)
		user.set_password(password)
		user.save(using = self._db)
		return user 

	def create_superuser(self,email,first_name,last_name,password,**kwargs):
		kwargs.setdefault("is_staff",True)
		kwargs.setdefault("is_superuser",True)
		kwargs.setdefault("is_admin",True)


		user = self.create_user(email,first_name,last_name,password,**kwargs)
		return user


class User(AbstractBaseUser,PermissionsMixin):
	id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False,unique = True)
	email = models.EmailField(unique = True)
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	is_active = models.BooleanField(default = True)
	is_superuser = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)
	is_confirmed = models.BooleanField(default = False)
	objects = UserManager()

	REQUIRED_FIELDS = ['first_name','last_name']
	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email
class Category(models.Model):
	name = models.CharField(max_length = 120)
class Product(models.Model):
	id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False,unique = True)
	category = models.ForeignKey(Category,on_delete = models.CASCADE,related_name = 'products')
	name = models.CharField(max_length = 120)
	description = models.TextField()
	image = models.ImageField(upload_to = 'product_image/')
	price = models.DecimalField(decimal_places = 2,max_digits = 10)
	discount = models.DecimalField(decimal_places = 2,max_digits = 10,default = 1.0)
	instock = models.BooleanField(default = True)
	def __str__(self):
		return self.name
class CartItem(models.Model):
	id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False,unique = True)
	user = models.ForeignKey(User,related_name = 'cart_items',on_delete = models.CASCADE)
	product = models.ForeignKey(Product,on_delete = models.CASCADE)
	quantity = models.IntegerField(default = 1)
	ordered = models.BooleanField(default = False)
	@property
	def total_price(self):
		return self.product.price * self.quantity


	def __str__(self):
		return f'{self.user.email} cart'
	
