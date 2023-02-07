from django.conf import settings
from django.core.mail import send_mail
import psycopg2
import pandas as pd
import time

adding_periods = {'once a day': 1, 'once a week': 7, 'once a month': 30}

query_part = '''
WHERE (
	posting_date <= CURRENT_DATE 
	OR (
		posting_time <= CURRENT_TIME
		AND posting_date = CURRENT_DATE
	)
)
AND(
	mailing_status = 'launched'	
	)
'''

'''change date of newsletter using frequency'''
def query_big(data):
    return f'UPDATE spammy_newsletter SET posting_date = CURRENT_DATE ' \
           f'+ {adding_periods[data]} {query_part} AND frequency=\'{data}\';'


'''take data for doing maillist'''
query_small = f'SELECT ' \
              f'letter_subject,' \
              f'body_of_the_letter,' \
              f'email ' \
              f'FROM spammy_newsletter ' \
              f'INNER JOIN spammy_newsletter_client ' \
              f'ON newsletter_id=spammy_newsletter.id ' \
              f'INNER JOIN spammy_client ' \
              f'ON client_id=spammy_client.id ' \
              f'INNER JOIN spammy_messagetosend ' \
              f'ON spammy_messagetosend.newsletter_id=spammy_newsletter.id ' \
              f'{query_part};'


def make_newsletter(*args, **kwargs):
    df = connect_do_db(query_small) # take data from db

    '''need to change next mailing date '''
    if len(df):
        '''write query to change next mailing date'''
        set_date_next_maling = ''
        for i in adding_periods.keys():
            set_date_next_maling += query_big(i)

        '''make query to db to change next mailing date '''
        connect_do_db(set_date_next_maling)

    '''send emails all addresses from df:'''
    for index, row in df.iterrows():
        print(row)
        sub = row[0]
        bod = row[1]
        ema = row[2]
        send_a_message(sub, bod, [ema])
        time.sleep(0.5)



def send_a_message(sub, mes, recip):
    send_mail(
        subject=sub,
        message=mes,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recip, #['ju2ll@ya.ru'],
    )


def connect_do_db(query, *args, **kwargs):
    conn = psycopg2.connect(host='localhost', dbname='mailing', user='oleg', password='12345')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                try:
                    info_from_db = cur.fetchall()
                except:
                    info_from_db = None
    finally:
        conn.close()
    return pd.DataFrame(info_from_db)