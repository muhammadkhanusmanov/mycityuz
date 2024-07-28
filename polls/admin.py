from django.contrib import admin
from .models import Posts, Reaction,Saved

admin.site.register([Posts, Reaction,Saved])
