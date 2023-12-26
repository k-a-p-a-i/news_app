import django_filters
from django import forms
from .models import Article, Tag, Category
from django.contrib.auth.models import User






class ArticleFilter(django_filters.FilterSet):

    tags = django_filters.ModelChoiceFilter(
        queryset=Tag.objects.all(),
        empty_label="Все тэги",
        label="Тэги",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    start_date = django_filters.DateFilter(field_name='date__date',
                            widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                            lookup_expr='exact', label='Дата новости')

    text_info = django_filters.CharFilter(field_name='title',
                                           widget=forms.TextInput(attrs={'class': 'form-control', }),
                                           lookup_expr='icontains', label='Название новости')

    author = django_filters.ModelChoiceFilter(queryset = User.objects.all(),
                                             empty_label="Все авторы",
                                             label="Авторы",
                                           widget=forms.Select(attrs={'class': 'form-control'}),

                                           )

    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                              empty_label="Все категории",
                                              label="Категории",
                                              widget=forms.Select(attrs={'class': 'form-control'}),

                                              )

    class Meta:
        model = Article
        fields = ['author', 'text_info', 'start_date', 'tags', 'category']

        #fields = {"name": ["exact", "contains"], "country": ["exact"]}  можно таким образом указывать как искать


