from django.contrib import admin
from .models import City, District, Customer, CustomerImage

admin.site.register(City)
admin.site.register(District)
admin.site.register(Customer)
admin.site.register(CustomerImage)