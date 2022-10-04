from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'year', 'name', 'type']
    list_filter = ['make','year', 'type']
    search_fields = ['make', 'name']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    # inlines = [CarModelInline]
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name', 'description']
# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
