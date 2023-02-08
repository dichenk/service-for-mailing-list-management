from django.urls import path

from config import settings
from spammy.views import spamming_system, ClientListView, NewsletterListView, MessageToSendListView, AttemptToSendListView, ClientCreateView, NewsletterCreateView, MessageToSendCreateView, ClientUpdateView, NewsletterUpdateView, MessageToSendUpdateView, change_status, ClientDeleteView, NewsletterDeleteView, MessageToSendDeleteView
from spammy.apps import SpammyConfig
from django.conf.urls.static import static

app_name = SpammyConfig.name

urlpatterns = [
    path('', spamming_system),
    path('index.html', spamming_system),

    path('clients', ClientListView.as_view(), name='client'),
    path('newsletter', NewsletterListView.as_view(), name='newsletter'),
    path('mails', MessageToSendListView.as_view(), name='mails'),
    path('maillistlog', AttemptToSendListView.as_view(), name='maillistlog'),

    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('create_newsletter', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('create_mail', MessageToSendCreateView.as_view(), name='create_mail'),

    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('update_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('update_mail/<int:pk>', MessageToSendUpdateView.as_view(), name='update_mail'),
    path('status/<int:pk>/', change_status, name='status'),

    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('delete_mail/<int:pk>', MessageToSendDeleteView.as_view(), name='delete_mail'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)