from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from datetime import date, timedelta

from .models import Post, Category


@shared_task
def notify_subs(pk):
    instance = Post.objects.get(pk=pk)

    for category in instance.categories.all():
        subs_emails = [user.email for user in category.users.all()]  # subs emails of present categories

        html_content = render_to_string(                             # convert and add context
            'mailing_new_post.html',
            {
                'post': instance,
                'category': category,
            }
        )

        msg = EmailMultiAlternatives(                                # configure message
            subject=instance.title,
            body=instance.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subs_emails
        )
        msg.attach_alternative(html_content, "text/html")  # attach html to message
        msg.send()


@shared_task()
def weekly_update():                # email all category subscribers about new posts every week
    week_ago = date.today() - timedelta(weeks=1)

    for category in Category.objects.all():
        if category.post_set.filter(time_in__gte=week_ago):          # if smth posted a week ago in category
            subs_emails = [user.email for user in category.users.all()]

            html_content = render_to_string(                         # convert and add context
                'weekly_updates_mailing.html',
                {
                    'category': category,
                    'time': week_ago.strftime("%Y-%m-%d"),
                }
            )

            msg = EmailMultiAlternatives(                            # configure message
                subject='Новые посты за неделю',
                body=f'Обновления за неделю можно посмотреть по ссылке: '
                     f'http://127.0.0.1:8000/news/search/?author=&type='
                     f'&title__icontains=&category={category.pk}&time_in__gt={week_ago.strftime("%Y-%m-%d")}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subs_emails
            )
            msg.attach_alternative(html_content, "text/html")        # attach html to message
            msg.send()
