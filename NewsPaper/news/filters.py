from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, ChoiceFilter
from django.forms.widgets import NumberInput, CheckboxSelectMultiple, CheckboxInput

from .models import Post, Category, POST_TYPES


class PostsFilter(FilterSet):                    # responsible for filters functionalty

    time_in__gt = DateFilter(                    # filer to show posts after certain date
        field_name='time_in',
        lookup_expr='gt',
        label='Показать посты начиная от',
        widget=NumberInput(attrs={'type': 'date'}),
    )

    category = ModelMultipleChoiceFilter(        # filter to show posts of a specific category
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категории',
        conjoined=True,
        widget=CheckboxSelectMultiple(),
    )

    type = ChoiceFilter(                         # filter to show only news or articles or both
        choices=POST_TYPES,
        empty_label='любой'
    )

    class Meta:

        model = Post
        fields = {
            'title': ['icontains'],              # filter by words/set of symbols in title
        }
