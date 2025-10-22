from django.db import models
from django.urls import reverse


class TelegramRegistration(models.Model):
    # id - PrimaryKey is added to DB by default
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram ID")
    full_name = models.CharField(max_length=2000, verbose_name="User Full Name")
    registration_date = models.CharField(max_length=2000, verbose_name="Registration Date")
    blocked = models.BooleanField(max_length=2000, verbose_name="Is Blocked?")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.full_name

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Telegram Registration'  # our model name in singular
        verbose_name_plural = 'Telegram Registrations'  # our model name in plural
        ordering = ['full_name', '-registration_date']  # sorting


class SiteRegistration(models.Model):
    # id - PrimaryKey is added to DB by default
    username = models.CharField(max_length=2000, verbose_name="Username")
    registration_date = models.CharField(max_length=2000, verbose_name="Registration Date")
    email = models.CharField(max_length=2000, verbose_name="E-mail", default=None)
    blocked = models.BooleanField(max_length=2000, verbose_name="Is Blocked?")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.username

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Site Registration'  # our model name in singular
        verbose_name_plural = 'Site Registrations'  # our model name in plural
        ordering = ['username', '-registration_date']  # sorting


class PasswordReset(models.Model):
    # id - PrimaryKey is added to DB by default
    username = models.CharField(max_length=2000, verbose_name="Username")
    token = models.CharField(max_length=2000, verbose_name="Token")
    created_date = models.DateField(verbose_name="Password Reset Link Creation Time")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.username

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Password Reset'  # our model name in singular
        verbose_name_plural = 'Password Resets'  # our model name in plural
        ordering = ['username']  # sorting


class Olympiad(models.Model):
    title = models.CharField(max_length=2000, verbose_name="Olympiad Title")
    start_date = models.CharField(max_length=2000, verbose_name="Olympiad Start Date")
    stage = models.CharField(max_length=2000, verbose_name="Olympiad Stage", default='None')
    schedule = models.CharField(max_length=2000, verbose_name="Olympiad Schedule", default='None')
    website = models.CharField(max_length=2000, verbose_name="Olympiad Website", default='None')
    is_recognized = models.BooleanField(max_length=2000, verbose_name="Is in Official List?")

    subject = models.ForeignKey('Subject', on_delete=models.PROTECT, verbose_name="Subject")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.title

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Olympiad'  # our model name in singular
        verbose_name_plural = 'Olympiads'  # our model name in plural
        ordering = ['subject', 'start_date']  # sorting


class NotificationSubscription(models.Model):
    user_identifier = models.CharField(max_length=2000, verbose_name="User or Telegram ID")

    title = models.CharField(max_length=2000, verbose_name="Olympiad Title")
    start_date = models.CharField(max_length=2000, verbose_name="Olympiad Start Date")
    stage = models.CharField(max_length=2000, verbose_name="Olympiad Stage", default='None')
    schedule = models.CharField(max_length=2000, verbose_name="Olympiad Schedule", default='None')
    website = models.CharField(max_length=2000, verbose_name="Olympiad Website", default='None')

    is_recognized = models.BooleanField(max_length=2000, verbose_name="Is in Official List?")

    subject = models.ForeignKey('Subject', on_delete=models.PROTECT, verbose_name="Subject")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.title

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Notification Subscription'  # our model name in singular
        verbose_name_plural = 'Notification Subscriptions'  # our model name in plural
        ordering = ['user_identifier', 'start_date']  # sorting


class Subject(models.Model):
    name = models.CharField(max_length=2000, verbose_name="Subject Name")
    slug = models.SlugField(max_length=2000, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="subjects/", verbose_name="Photo")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subject', kwargs={'subject_slug': self.slug})

    class Meta:
        verbose_name = 'Subject'  # our model name in singular
        verbose_name_plural = 'Subjects'  # our model name in plural
        ordering = ['name']  # sorting


class SecretToken(models.Model):
    # id - PrimaryKey is added to DB by default
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram ID")
    secret_token = models.CharField(max_length=2000, verbose_name="Secret Token")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.telegram_id

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Secret Token'  # our model name in singular
        verbose_name_plural = 'Secret Tokens'  # our model name in plural
        ordering = ['telegram_id', ]  # sorting


class UserTelegramConnection(models.Model):
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram ID")
    username = models.CharField(max_length=2000, verbose_name="Username")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.telegram_id

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'User Telegram Connection'  # our model name in singular
        verbose_name_plural = 'User Telegram Connections'  # our model name in plural
        ordering = ['telegram_id', ]  # sorting


class Feedback(models.Model):
    # id - PrimaryKey is added to DB by default
    username = models.CharField(max_length=2000, verbose_name="Username")
    feedback_text = models.CharField(max_length=2000, verbose_name="Feedback")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.username

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Feedback'  # our model name in singular
        verbose_name_plural = 'Feedbacks'  # our model name in plural
        ordering = ['username']  # sorting


class TechnicalSupport(models.Model):
    # id - PrimaryKey is added to DB by default
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram ID")
    support_request = models.CharField(max_length=2000, verbose_name="Support Request")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.telegram_id

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Technical Support Request'  # our model name in singular
        verbose_name_plural = 'Technical Support Requests'  # our model name in plural
        ordering = ['telegram_id', 'support_request']  # sorting


class Payment(models.Model):
    # id - PrimaryKey is added to DB by default
    telegram_id = models.CharField(max_length=2000, verbose_name="Telegram ID")
    payment_data = models.CharField(max_length=2000, verbose_name="Payment Data")

    # When displaying all records, for distinction, their title will be displayed
    def __str__(self):
        return self.telegram_id

    # Class for working with the model in Admin panel
    class Meta:
        verbose_name = 'Payment'  # our model name in singular
        verbose_name_plural = 'Payments'  # our model name in plural
        ordering = ['telegram_id', 'payment_data']  # sorting
