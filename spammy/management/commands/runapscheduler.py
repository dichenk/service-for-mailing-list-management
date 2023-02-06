import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import pandas as pd
import time
import datetime
import psycopg2

logger = logging.getLogger(__name__)


def my_job():
    send_a_message()
    df = read_newsletter()
    send_immediately = df[df[4] < datetime.date.today()]
  #  send_today = df[df[4] == datetime.date.today()]
    send_today = df[df[1] < datetime.datetime.now().time()]

    print(len(send_immediately))
    print('pause 1')
    print(len(send_today))
    print('pause 2')



# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
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


def send_a_message():
    send_mail(
        subject='hello',
        message='hello world',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['ju2ll@ya.ru'],
    )


def read_newsletter():
    conn = psycopg2.connect(host='localhost', dbname='mailing', user='oleg', password='12345')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM spammy_newsletter')
                info_from_db = cur.fetchall()
    finally:
        conn.close()
    return pd.DataFrame(info_from_db)


def is_the_time_for_sending(tm):
    tm = (tm.hour * 60 + tm.minute) * 60 + tm.second
    tm_now = time.gmtime()
    tm_now = (tm_now.tm_hour * 60 + tm_now.tm_min) * 60 + tm_now.tm_sec
    return tm - tm_now <= 0



