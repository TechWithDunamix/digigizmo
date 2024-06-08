from django.contrib.auth.backends import ModelBackend
from .models import User
class Auth(ModelBackend):

	def authenticate(self,email = None,password = None):
		if not email:
			raise ValueError("Email is required")
		if not password:
			raise ValueError("Password is required")


		try:
			user = User.objects.get(email = email)

		except User.DoesNotExist:
			print("User does not exists")
			return None

		if user.check_password(password):
			return user
		else:
			print("invalid password")
			return None

	def get_user(self,id):
		try:
			return user.objects.get(id = id)
		except User.DoesNotExists:
			return None