from django import forms
from .models import Article, Tag




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

