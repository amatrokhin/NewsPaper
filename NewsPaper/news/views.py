# Import class to output objects from DB
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from .models import Post
from .filters import PostsFilter
from .forms import PostsForm


class PostsList(ListView):                      # responsible for table of posts on the main page
    queryset = Post.objects.all().order_by('-time_in')
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):                   # responsible for detailed post output on a page
    # queryset = Post.objects.filter(type='N')
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):                    # responsible for posts list with filters output
    model = Post
    ordering = '-time_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10

    def get_queryset(self):                     # redefine function to get posts list
        queryset = super().get_queryset()       # get standart queryset

        # save filtration in class object to reuse later
        self.filterset = PostsFilter(self.request.GET, queryset)

        return self.filterset.qs                # return extended queryset

    def get_context_data(self, **kwargs):       # add filtration object to context and return extended context
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):                   # responsible for creating news
    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    # we want user to create news and articles from different pages and not by choosing type attribute
    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'N'
        return super().form_valid(form)


class ArticlesCreate(CreateView):                   # responsible for creating articles
    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    # we want user to create news and articles from different pages and not by choosing type attribute
    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'A'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
