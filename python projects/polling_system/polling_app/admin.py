from django.contrib import admin

# Register your models here.
from .models import Questions,phone_no
admin.site.register(Questions)
admin.site.register(phone_no)