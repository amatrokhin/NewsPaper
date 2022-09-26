from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post


'''
 send mail to category subscribers when news/articles are created
 
 receiver substitutes post_save.connect(notify_category_subs, sender=Post)
 @receiver(post_save, sender=Post) -> this doesn't work as instance.categories.all() returns empty queryset

 m2m_changed: this signal is sent when ManyToManyField is changed on an instance
 sender: in the aboce case we must acess the intemediate class, aka use through attribute on a m2m-field
 dispatch_uid: just in case, to prevent double email sending if our function is touched multiple times
'''


@receiver(m2m_changed, sender=Post.categories.through, dispatch_uid='prevent_double_email')
def notify_category_subs(sender, instance, action, **kwargs):
    if action == 'post_add':

        for category in instance.categories.all():
            subs_emails = [user.email for user in category.users.all()]  # subs emails of present categories

            html_content = render_to_string(  # convert and add context
                'mailing.html',
                {
                    'post': instance,
                    'category': category,
                }
            )

            msg = EmailMultiAlternatives(  # configure message
                subject=instance.title,
                body=instance.text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subs_emails
            )
            msg.attach_alternative(html_content, "text/html")  # attach html to message
            msg.send()


'''
previousy we overrode post in NewsCreate and AtriclesCreate like the following

def post(self, request, *args, **kwargs):   # override post to send emails to those, who subscribed
    #this does everything with DB for us
    url = super().post(request).url

    # only send mails if created but not updated
    if 'create' in request.path:
        # this is for operating in html
        post = Post(
            author=Author.objects.get(user=request.user),
            title=request.POST['title'],
            text=request.POST['text'],
        )

        categories = [Category.objects.get(pk=pk) for pk in request.POST.getlist('categories')]

        for category in categories:
            subscribers = [user for user in category.users.all()]       # subs of present categories

            for subscriber in subscribers:
                html_content = render_to_string(                        # convert and add context
                    'mailing.html',
                    {
                        'post': post,
                        'subscriber': subscriber,
                        'category': category,
                    }
                )

                msg = EmailMultiAlternatives(                           # send message
                    subject=post.title,
                    body=post.text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")       # attach html to message

                msg.send()

    return redirect(url)
'''
