from django.contrib import admin
from spammy.models import AttemptToSend, Client, MessageToSend, Newsletter

admin.site.register(Client)
admin.site.register(Newsletter)
admin.site.register(MessageToSend)
admin.site.register(AttemptToSend)
