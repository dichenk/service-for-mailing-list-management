from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'print(\'wow\')'  # a unique code

    def do(self):
         print('wow' + time.time())

def my_cron_job():
    print('ho-ho-ho')