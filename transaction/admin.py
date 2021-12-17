from django.contrib import admin

from transaction.models import Cart, SiteTransaction

# Register your models here.

admin.site.register(SiteTransaction)
admin.site.register(Cart)


