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
    def make_newsletter(data):
        adding_periods = {'once a day': 1, 'once a week': 7, 'once a month': 30}
        print(data)
        for index, row in data.iterrows():
            period = df.loc[index][2]  # set next date of emails sending
            variable = datetime.date.today() + datetime.timedelta(days=adding_periods[period])
            df.loc[index][4] = variable
            '''
            newsletter_id = data.iloc[i][0]
            client_list_db = read_data_from_db('spammy_newsletter_client')
            letter_list = read_data_from_db('spammy_messagetosend')
            # to send
            
            
            print(adding_periods)
            print(period)
            print(df)
            
            print(df)
            '''

    df = read_data_from_db('spammy_newsletter')
    '''if the mailing date in the past: send letters and set next sending date'''
    maillist_table = df[(df[4] < datetime.date.today()) & (df[3] == 'launched')]
#    print(f'amount of past dates: {len(maillist_table)}')
    if len(maillist_table):
        make_newsletter(maillist_table)

    '''if the mailing date is today ant the time is now: send letters and set next sending date'''
    maillist_table = df[(df[4] == datetime.date.today()) & (df[1] <= datetime.datetime.now().time()) & (df[3] == 'launched')]
#    print(f'amount of today past maillists: {len(maillist_table)}')
    if len(maillist_table):
        make_newsletter(maillist_table)




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


def send_a_message(sub, mes, recip):
    send_mail(
        subject=sub,
        message=mes,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recip, #['ju2ll@ya.ru'],
    )

'''reading data from db'''
def read_data_from_db(name_of_db):
    conn = psycopg2.connect(host='localhost', dbname='mailing', user='oleg', password='12345')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM {name_of_db}')
                info_from_db = cur.fetchall()
    finally:
        conn.close()
    return pd.DataFrame(info_from_db)



