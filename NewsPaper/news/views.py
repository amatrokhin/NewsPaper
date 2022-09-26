# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    queryset = Post.objects.filter(type='N').order_by('-time_in')
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    queryset = Post.objects.filter(type='N')
    template_name = 'post.html'
    context_object_name = 'post'
