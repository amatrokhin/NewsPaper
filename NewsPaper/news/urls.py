from django.urls import path
from .views import (
   PostsList, PostDetail, PostsSearch, NewsCreate, NewsUpdate, NewsDelete, subscribe_cat, unsubscribe_cat
)
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path('', cache_page(60)(PostsList.as_view()), name='posts_list'),  # cache 1 min for educational purposes
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostsSearch.as_view(), name='posts_search'),
   path('create/', NewsCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('search/<int:pk>/subscribe/', subscribe_cat, name='user_subscribe'),
   path('search/<int:pk>/unsubscribe/', unsubscribe_cat, name='user_unsubscribe'),
]
