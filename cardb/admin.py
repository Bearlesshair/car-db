from django.contrib import admin
import cardb.models as models


# Define the admin class
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'mileage', 'transmission', 'title', 'seller_type')
    list_filter = ('car', 'transmission', 'title', 'seller_type', 'other_info')

# Register the admin class with the associated model


admin.site.register(models.Listing, ListingsAdmin)
admin.site.register(models.Bodystyle)
admin.site.register(models.Car)
# admin.site.register(models.Listing)

