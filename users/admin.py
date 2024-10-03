from django.contrib import admin
from .models import CustomUser, Orders



# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Orders)