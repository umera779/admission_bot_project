from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FAQ, AdmissionInfo

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category']
    list_filter = ['category']

@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['category']