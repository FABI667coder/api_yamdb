from django.contrib import admin

from reviews.models import Comments, Review, User, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date')
    search_fields = ('author', 'text')
    list_filter = ('author', 'pub_date')
    empty_value_diplay = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date')
    search_fields = ('author', 'text')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(User)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
