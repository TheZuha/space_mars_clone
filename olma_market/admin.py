from django.contrib import admin
from .models import Shops, Products, Categories, Cart, Store
from django.db import models
from django_summernote.widgets import SummernoteWidget
# Register your models here.

class OlmaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }

admin.site.register(Categories)
admin.site.register(Shops)
admin.site.register(Products, OlmaAdmin)
admin.site.register(Cart)
admin.site.register(Store, OlmaAdmin)