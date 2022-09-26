from django.urls import path
from .views import (
   PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete, ArticlesCreate
)


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostsSearch.as_view(), name='posts_search'),
   path('create/', NewsCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]
