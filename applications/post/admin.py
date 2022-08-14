from django.contrib import admin

# Register your models here.
from applications.post.models import Post, Image, Like, Comment, Rating

admin.site.register(Image)
# admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Rating)

class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInAdmin]


admin.site.register(Post, PostAdmin)
