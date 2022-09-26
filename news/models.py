from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):                 # table of authors
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    @staticmethod
    def update_rating(user):
        tot_posts_rating = sum(post.rating * 3 for post in user.post_set.all())
        tot_comments_rating = sum(com.rating for com in user.user.comment_set.all())

        # get all posts' comment and calculate their rating
        comments_to_posts = (post.comment_set.all() for post in user.post_set.all())
        com_to_posts_rating = (sum(com.rating for com in coms) for coms in comments_to_posts)
        tot_com_to_post_rating = sum(rating for rating in com_to_posts_rating)

        user.rating = tot_posts_rating + tot_comments_rating + tot_com_to_post_rating


class Category(models.Model):               # table of categories
    cat_name = models.CharField(max_length=30, unique=True)


POST_TYPES = [('N', 'news'), ('A', 'article')]


class Post(models.Model):                   # table of news and articles
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPES, default='A')
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):           # table for many-to-many relation between posts and categories
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):                # table of comments to posts
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
