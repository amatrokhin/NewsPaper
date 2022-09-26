from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

from .models import Post, Category


class PostsForm(forms.ModelForm):                    # responsible for form to create news

    # the following 3 fields work only if they are present in Meta.fields as well
    # otherwise these fields are present on a page but they don't transfer input to the DB
    title = forms.CharField(
        widget=forms.Textarea(attrs={
            'required': True,                       # To notify creator to fill the field
            'placeholder': gettext('Ваш заголовок тут'),
            'cols': 120,
            'rows': 1,
        })
    )

    text = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={
            'required': True,
            'placeholder': gettext('Ваш текст здесь'),
            'cols': 160,
        })
    )

    categories = forms.ModelMultipleChoiceField(    # purely for cosmetic reasons
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Post
        fields = [
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
                gettext("Заголовок и текст статьи не должны совпадать.")
            )

        return cleaned_data


