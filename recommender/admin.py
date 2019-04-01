from django.contrib import admin

from .models import Movie, Review, Member

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Member)