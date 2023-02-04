from django.db import models


class Client(models.Model):
    email = models.EmailField(
        blank=False,
        max_length=100,
        verbose_name='Электронка'
    )
    mame = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        default=None,
        blank=False
    )
    comment = models.TextField(verbose_name='Комментарий', default=None)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.mame}\n'


class Newsletter(models.Model):
    FREQUENCYS = (
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц')
    )
    STATUSES = (
        ('completed,', 'завершена'),
        ('created', 'создана'),
        ('launched,', 'запущена')
    )
    client = models.ForeignKey(
        Client,
        max_length=100,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        null=True
    )
    posting_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Время рассылки',
        blank=True
    )
    frequency = models.CharField(choices=FREQUENCYS, default='once a day', max_length=20)
    mailing_status = models.CharField(choices=STATUSES, default='created', max_length=20)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.posting_time}\n{self.frequency}\n{self.mailing_status}\n'


class MessageToSend(models.Model):
    newsletter = models.OneToOneField(
        Newsletter,
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
        null=True
    )
    letter_subject = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Тема письма',
        default=None,
    )
    body_of_the_letter = models.TextField(
        blank=True,
        max_length=1000,
        verbose_name='Тело письма',
        default=None,
    )

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщение для рассылок'

    def __str__(self):
        return f'{self.letter_subject}\n{self.body_of_the_letter}\n'


class AttemptToSend(models.Model):

    date_of_last_attempt = models.CharField(max_length=100, verbose_name='Дата последней попытки', default=None)
    time_of_last_attempt = models.CharField(max_length=150, verbose_name='Время последней попытки', default=None)
    attempt_status = models.CharField(max_length=150, verbose_name='Статус попытки', default=None)
    mail_server_response = models.TextField(verbose_name='Ответ сервера', default=None)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'

    def __str__(self):
        return f'{self.date_of_last_attempt}\n{self.mail_server_response}\n'
