import logging
from datetime import date, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ...models import Category

logger = logging.getLogger(__name__)


# email all category subscribers about new posts every week
def my_job():
    #  Your job processing logic here...
    week_ago = date.today() - timedelta(weeks=1)

    for category in Category.objects.all():
        if category.post_set.filter(time_in__gte=week_ago):                 # if smth posted a week ago in category
            subs_emails = [user.email for user in category.users.all()]

            html_content = render_to_string(                                # convert and add context
                'weekly_updates_mailing.html',
                {
                    'category': category,
                    'time': week_ago.strftime("%Y-%m-%d"),
                }
            )

            msg = EmailMultiAlternatives(                                   # configure message
                subject='Новые посты за неделю',
                body=f'Обновления за неделю можно посмотреть по ссылке: '
                     f'http://127.0.0.1:8000/news/search/?author=&type='
                     f'&title__icontains=&category={category.pk}&time_in__gt={week_ago.strftime("%Y-%m-%d")}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subs_emails
            )
            msg.attach_alternative(html_content, "text/html")               # attach html to message
            msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # add our work to our task manager
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute=0, hour=12, day_of_week='sun'),      # every sunday at 12:00
            id="my_job",                                                    # unique id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # delete old tasks that were faild to do or are no longer needed every week
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
