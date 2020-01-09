from django.contrib import admin
import cardb.models as models

admin.site.register(models.Car)
admin.site.register(models.Listing)
admin.site.register(models.Bodystyle)
