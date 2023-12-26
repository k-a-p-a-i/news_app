from .models import ViewCounter
import django_tables2 as tables
from django_tables2.utils import A


from .models import Article
##-----------------------Получение ip-адреса_________________________#######################
def get_client_ip(request):
    x_forwrded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwrded_for:
        ip = x_forwrded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ViewCountMixin:
    def get_object(self):
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        ViewCounter.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj




##-----------------------Таблица со списком новостей_________________________#######################
class ArticleTable(tables.Table):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns['title'].column.attrs = {"td": {"style": "width:20%;"}}
        self.columns['author'].column.attrs = {"td": {"style": "width:10%;"}}
        self.columns['date'].column.attrs = {"td": {"style": "width:10%;"}}
        self.columns['category'].column.attrs = {"td": {"style": "width:15%;"}}
        self.columns['tags'].column.attrs = {"td": {"style": "width:15%;"}}

    #tags = tables.ManyToManyColumn( verbose_name='Тэги', ) #filter=lambda qs: qs.filter(tags__status=True) filter=lambda qs: qs.filter(status=True)
    title = tables.LinkColumn('news_app:single_news', verbose_name='Название', args=[A('pk')])



    class Meta:
        model = Article
        template_name = "django_tables2/bootstrap5.html"
        fields = ( 'title', "author", 'date', 'category', 'tags')



