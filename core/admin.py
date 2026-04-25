from django.contrib import admin
from .models import Post

admin.site.register(Post)
from .models import Comment
admin.site.register(Comment)
from .models import Profile
admin.site.register(Profile)