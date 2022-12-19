from django.contrib import admin
from .models import auction_list, bids, comments, Category


admin.site.register(auction_list)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(Category)