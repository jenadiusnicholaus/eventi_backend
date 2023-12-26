from django.contrib import admin
from .models import EventiGroupPlage
from .models import EventiGroup, EventiGroupMembers

# Register your models here.

admin.site.register(EventiGroup)

admin.site.register(EventiGroupPlage)

# admin.site.register(MemberShip   )

admin.site.register(EventiGroupMembers)



