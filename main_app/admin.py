from django.contrib import admin
from .models import Watch, Bid, Transaction, Tag
# Register your models here.
admin.site.register(Watch)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Tag)

