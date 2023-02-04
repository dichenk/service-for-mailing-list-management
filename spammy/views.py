import psycopg2
import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from spammy.models import Client, Newsletter, MessageToSend, AttemptToSend
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
import time


def spamming_system(request):
    return render(request, 'spammy/index.html')


class ClientListView(ListView):
    model = Client


class NewsletterListView(ListView):
    model = Newsletter


class MessageToSendListView(ListView):
    model = MessageToSend


class AttemptToSendListView(ListView):
    model = AttemptToSend


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'mame', 'comment')
    success_url = reverse_lazy('spammy:client')


class NewsletterCreateView(CreateView):
    model = Newsletter
    fields = ('client', 'posting_time', 'frequency')
    success_url = reverse_lazy('spammy:create_mail')


class MessageToSendCreateView(CreateView):
    model = MessageToSend
    fields = ('newsletter', 'letter_subject', 'body_of_the_letter')
    success_url = reverse_lazy('spammy:mails')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'mame', 'comment')
    success_url = reverse_lazy('spammy:client')


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    fields = ('client', 'posting_time', 'frequency')
    success_url = reverse_lazy('spammy:create_mail')


class MessageToSendUpdateView(UpdateView):
    model = MessageToSend
    fields = ('newsletter', 'letter_subject', 'body_of_the_letter')
    success_url = reverse_lazy('spammy:mails')


def change_status(request, pk):
    maillist_item = get_object_or_404(Newsletter, pk=pk)
    if maillist_item.mailing_status == 'created':
        maillist_item.mailing_status = 'launched'
    else:
        maillist_item.mailing_status = 'created'
    maillist_item.save()
    check_myself()
#    send_a_message()
    return redirect(reverse_lazy('spammy:newsletter'))

def check_myself():
    print('hello')
    conn = psycopg2.connect(host='localhost', dbname='mailing', user='oleg', password='12345')
    info_from_db = None
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM spammy_newsletter')
                info_from_db = cur.fetchall()
    finally:
        conn.close()
    df = pd.DataFrame(info_from_db)
    for i in df:
        tm = df.iloc[i][1]
        print(tm)
        tm = (tm.hour * 60 + tm.minute) * 60 + tm.second
        tm_now = time.gmtime()
        print(tm_now)
        tm_now = (tm_now.tm_hour * 60 + tm_now.tm_min) *60 + tm_now.tm_sec
        if tm - tm_now < 0:
            print('самое время')

def send_a_message():
    send_mail(
        subject='hello',
        message='hello world',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['ju2ll@ya.ru'],
    )
