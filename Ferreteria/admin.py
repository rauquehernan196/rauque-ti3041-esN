from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'archivado')
    list_editable = ('archivado',)
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'archivado')