from django.contrib import admin
from .models import Product, Category

# Register your models here.
# You can add a lenght for field display in django admin console
# You can use a minus symbol '-' before field name to sort in descending order

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)