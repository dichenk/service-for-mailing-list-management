from django.shortcuts import render, get_object_or_404, redirect
from spammy.models import Client, Newsletter, MessageToSend, AttemptToSend
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
    return redirect(reverse_lazy('spammy:newsletter'))

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('spammy:client')
class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('spammy:newsletter')
class MessageToSendDeleteView(DeleteView):
    model = MessageToSend
    success_url = reverse_lazy('spammy:mails')
