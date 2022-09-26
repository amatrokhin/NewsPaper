from .models import *
from rest_framework import serializers


'''
Define serializers for a REST API/
They define how models will be translated into data and back
'''


class CategorySerializer(serializers.HyperlinkedModelSerializer):  # class to acces many_to_many field in PostSerializer
    class Meta:
        model = Category
        fields = ['id', 'name', ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    time_in = serializers.DateTimeField(format='%Y-%b-%d')
    link = serializers.SerializerMethodField()                     # for custom link field, see get_link
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'link', 'type', 'time_in', 'title', 'text', 'rating', 'categories', ]

    def get_link(self, obj):                                       # this is to add the link
        link = 'http://127.0.0.1:8000/api/'

        if obj.type == 'N':
            link += 'news/'

        elif obj.type == 'A':
            link += 'articles/'

        link += str(obj.id)

        return link
