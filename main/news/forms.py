from django import forms
from django.forms import inlineformset_factory

from .models import Article, Tag, ShowImage, Category

class MultipleFileInput(forms.ClearableFileInput):
    #для множественного выбора изображений
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    # для множественного выбора изображений
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result




ImagesFormSet = inlineformset_factory(Article, ShowImage, fields=("image",),extra=1,max_num=4,
    widgets={
        "image_field": MultipleFileField(),
    })


class ArticleForm(forms.ModelForm):
    image_field = MultipleFileField()
    class Meta:
        model = Article
        fields = ["title", "anouncement", "text",  "category", "tags"]

        tags = forms.ModelMultipleChoiceField( queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple  )

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'anouncement': forms.Textarea(attrs={"class": "form-control", "rows": 1}),
            'text': forms.Textarea(attrs={"class": "form-control"}),
            #'image': forms.FileInput(attrs={"class": "form-control"}), #для добавления только одной картинки
            'category': forms.Select(attrs={"class": "form-control"}),
                }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["title", "status"]

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Введите название тэга'}, ),
            'status': forms.CheckboxInput(),
                }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

        widgets = {'name': forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Введите название категории'},), }
