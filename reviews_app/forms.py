from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Price, GameReview


class AddReviewForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрано', label='Категория')
    price = forms.ModelChoiceField(queryset=Price.objects.all(), empty_label='Бесплатно', required=False, label='Цена')

    class Meta:
        model = GameReview
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')


