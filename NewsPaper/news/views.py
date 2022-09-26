import re
from datetime import datetime

# Import class to output objects from DB
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.core.cache import cache

from .models import Post, Author, Category
from .filters import PostsFilter
from .forms import PostsForm


class PostsList(ListView):                      # responsible for table of posts on the main page
    queryset = Post.objects.all().order_by('-time_in')
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        # check if queryset is in cache, if not add
        return cache.get_or_set('posts_list', super().get_queryset(), 300)


class PostDetail(DetailView):                   # responsible for detailed post output on a page
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):      # use cache to get post
        post = cache.get(f'post-{self.kwargs["pk"]}', None)     # find post in cache or return None

        # if post not in cache find in DB and write to cache
        if not post:
            post = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', post, 300)   # store for 5 min in cache

        return post


class PostsSearch(ListView):                    # responsible for posts list with filters output
    model = Post
    ordering = '-time_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10

    def get_queryset(self):                     # redefine function to get posts list
        # check if queryset is in cache, if not add
        queryset = cache.get_or_set('posts_list', super().get_queryset(), 300)

        # save filtration in class object to reuse later
        self.filterset = PostsFilter(self.request.GET, queryset)

        return self.filterset.qs                # return extended queryset

    def get_context_data(self, **kwargs):       # add filtration object to context and return extended context
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):      # responsible for creating news
    permission_required = ('news.add_post', )

    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    # we want user to create news and articles from different pages and not by choosing type attribute
    def form_valid(self, form):
        news = form.save(commit=False)

        # take author instance corresponding to the current user
        author = self.request.user
        author = Author.objects.get(user=author)

        form.instance.author = author
        news.type = 'N'
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        cur_date = datetime.today().strftime('%Y-%m-%d')

        author = Author.objects.get(user=request.user)
        posts_today = Post.objects.filter(author=author, time_in__gte=cur_date).aggregate(Count('pk'))['pk__count']

        # only allow maximum of 3 posts a day
        if posts_today >= 3:
            return HttpResponseForbidden('Вы не можете создавать более 3-х постов в день')
        else:
            return super().get(request, *args, **kwargs)


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # responsible for creating articles
    permission_required = ('news.add_post', )

    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'

    # we want user to create news and articles from different pages and not by choosing type attribute
    def form_valid(self, form):
        news = form.save(commit=False)

        # take author instance corresponding to the current user
        author = self.request.user
        author = Author.objects.get(user=author)

        form.instance.author = author
        news.type = 'A'
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        cur_date = datetime.today().strftime('%Y-%m-%d')

        author = Author.objects.get(user=request.user)
        posts_today = Post.objects.filter(author=author, time_in__gte=cur_date).aggregate(Count('pk'))['pk__count']

        # only allow maximum of 3 posts a day
        if posts_today >= 3:
            return HttpResponseForbidden('Вы не можете создавать более 3-х постов в день')
        else:
            return super().get(request, *args, **kwargs)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):      # updates posts
    permission_required = ('news.change_post', )

    form_class = PostsForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):      # deletes posts
    permission_required = ('news.delete_post', )

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


@login_required
def subscribe_cat(request, pk):                     # subscribe user to category he currently chose in a filter
    user = request.user
    cur_category = Category.objects.get(pk=pk)

    # if user isn't subscribed to category then subscribe
    if not user.category_set.filter(name=cur_category.name).exists():
        cur_category.users.add(user)

    # reload current page with parameters applied before
    path = re.sub(r'/\d*/subscribe', '', request.get_full_path())
    return redirect(path)


@login_required
def unsubscribe_cat(request, pk):                     # unsubscribe user from category he currently chose in a filter
    user = request.user
    cur_category = Category.objects.get(pk=pk)

    # if user isn't subscribed to category then subscribe
    if user.category_set.filter(name=cur_category.name).exists():
        cur_category.users.remove(user)

    # reload current page with parameters applied before
    path = re.sub(r'/\d*/unsubscribe', '', request.get_full_path())
    return redirect(path)
