from django.contrib import admin
from .models import APIRequest, APIResponse

@admin.register(APIRequest)
class APIRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_used', 'created_at')
    search_fields = ('user_input', 'model_used')
    readonly_fields = ('created_at',)

@admin.register(APIResponse)
class APIResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'api_request', 'model_name', 'created_at')
    search_fields = ('model_name', 'raw_response')
    readonly_fields = ('created_at',)

