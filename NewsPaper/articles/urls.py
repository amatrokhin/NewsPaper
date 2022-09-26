from django.urls import path
from news.views import (
   PostsList, PostDetail, PostsSearch, NewsUpdate, NewsDelete, ArticlesCreate
)


urlpatterns = [
   path('create/', ArticlesCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]
