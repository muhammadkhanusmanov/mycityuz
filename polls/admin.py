from django.contrib import admin
from .models import Posts, Reaction

admin.site.register([Posts, Reaction])
