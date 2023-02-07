from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_editable = ('group',)
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
