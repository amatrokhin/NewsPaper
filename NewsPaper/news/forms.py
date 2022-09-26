from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class PostsForm(forms.ModelForm):                    # responsible for form to create news
    title = forms.CharField(
        widget=forms.Textarea(attrs={
            'required': True,                       # To notify creator to fill the field
            'placeholder': 'Ваш заголовок тут',
            'cols': 120,
            'rows': 1,
        })
    )

    text = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={
            'required': True,
            'placeholder': 'Ваш текст здесь',
            'cols': 160,
        })
    )

    # somehow this works with Meta.field but not on its own
    categories = forms.ModelMultipleChoiceField(    # purely for cosmetic reasons
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'categories',
        ]

    def clean(self):                                # validation of input data
        cleaned_data = super().clean()

        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Заголовок и текст статьи не должны совпадать."
            )

        return cleaned_data


