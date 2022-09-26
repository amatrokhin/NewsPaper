from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from .tasks import notify_subs


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

        notify_subs.delay(instance.pk)
