from django.contrib import admin
from django.db.models.functions import Length
from django.db.models import Count

from .models import Article, Category, Tag, ShowImage





class ArticleFilter(admin.SimpleListFilter):
    title = 'Длина новости'
    parameter_name = 'text' #отображается в адресной строке

    def lookups(self, request, model_admin):
        return [('S', ("Короткие, <100зн")),
                ('M', ("Средние, 100-500зн")),
                ('L', ("Длинные, >500зн")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500, text_len__gte=100)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)


class ArticleImageInline(admin.TabularInline):
    model = ShowImage
    extra = 3
    readonly_fields = ('id', 'image_tag')


class ArticeAdmin(admin.ModelAdmin):
    ordering = ["-date", "author"]
    list_display =['pk', 'title', 'author', 'anouncement', 'date', 'category', 'symbols_count', 'image_tag']
    list_filter = ['title', 'date', 'author', ArticleFilter]
    list_display_links = ['pk', 'author']
    list_editable = ['title']
    list_per_page = 10
    inlines = [ArticleImageInline, ]
    filter_horizontal = ['tags']
    @admin.display(description="Длина", ordering="_symbols")
    def symbols_count(self, article):
        return f"Кол-во символов: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length("text"))
        return queryset

class TagAdmin(admin.ModelAdmin):
    list_display =['title', 'status', 'tag_count' ]
    list_filter = ['title', 'status']
    actions = ['set_true', 'set_false']
    search_fields = ['title__icontains',] #поля для поиска __fuction
    @admin.display(description="Кол-во использований", ordering="tag_count")
    def tag_count(self, tag_for_count):
        return f"{tag_for_count.tag_count}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count("article"))
        return queryset

    @admin.action(description="Активировать выбранные тэги")
    def set_true(self, request,queryset ):
        amount = queryset.update(status=True)
        self.message_user(request, f"Активировано {amount} тэгов")

    @admin.action(description="Деактивировать выбранные тэги")
    def set_false(self, request, queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f"Деактивировано {amount} тэгов")

@admin.register(ShowImage)
class ShowImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'article', 'image_tag']

admin.site.register(Category)
admin.site.register(Article, ArticeAdmin)
admin.site.register(Tag, TagAdmin)



