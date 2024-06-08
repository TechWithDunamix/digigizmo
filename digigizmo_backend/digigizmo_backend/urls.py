
from django.contrib import admin
from django.urls import path,include
from core.admin import core_admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', core_admin.urls),
    path('api/v1/',include("core.urls"))
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
