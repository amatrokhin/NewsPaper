from django.urls import path
from .views import IndexView, upgrade_me
from news.views import unsubscribe_cat

urlpatterns = [
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    # for deleting subscriptions from personal cabinet
    path('<int:pk>/unsubscribe/', unsubscribe_cat, name='user_unsubscribe'),
]