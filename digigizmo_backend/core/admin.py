from django.contrib import admin
from .models import User,Category,Product,CartItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CoreAdminSite(admin.AdminSite):
    site_header = 'DigiGizmo'

core_admin = CoreAdminSite(name = 'the admin')
class CostumUserAdmin(BaseUserAdmin):
	fieldsets = ((None,{'fields':('email','password','first_name','last_name','last_login')}),
		('Permissions',{'fields':('is_active',
			'is_staff',
			'is_superuser',
			'groups',
			)}),
		)
	add_fieldsets = (
		(
			None,
			{
			"classes":("wide",),
			"fields":('email','password1','password2'),
			 }))
	list_display = ('email','first_name','last_name','is_staff')
	list_filter = ('is_staff','is_superuser','is_active','groups')
	ordering = ('email',)
	filter_horizontal = ('groups','user_permissions',)

core_admin.register(User,CostumUserAdmin)
core_admin.register(Product)
core_admin.register(Category)

class CartAdmin(admin.ModelAdmin):
	list_filter = ['ordered',]
	list_display =['product','quantity']

core_admin.register(CartItem,CartAdmin)
