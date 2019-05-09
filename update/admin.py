from django.contrib import admin

# Register your models here.
from .models import Category,Ticket,Event

admin.site.register(Category),
admin.site.register(Ticket),
admin.site.register(Event),

