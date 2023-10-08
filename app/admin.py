from django.contrib import admin
from.models import *
# Register your models here.
admin.site.register(Stock)
# admin.site.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'query_text')

admin.site.register(Query, QueryAdmin)