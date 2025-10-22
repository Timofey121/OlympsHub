from django.contrib import admin

from olympic.models import SiteRegistration, TelegramRegistration, Olympiad, NotificationSubscription, Feedback, \
    TechnicalSupport, Payment, \
    Subject, SecretToken, UserTelegramConnection, PasswordReset


class SiteRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'blocked', 'registration_date')  # display these fields
    list_display_links = (
        'username', 'email', 'registration_date')  # clickable fields in admin panel for navigating to database record
    search_fields = ('email', 'username')  # fields to search records by
    list_editable = ('blocked',)  # fields that can be edited directly in the record list

    # fields displayed in the edit form, some are non-editable
    fields = ('username', 'email', 'registration_date', 'blocked')


class TelegramRegistrationAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'blocked', 'registration_date')  # display these fields
    list_display_links = (
        'telegram_id', 'full_name', 'registration_date')  # clickable fields in admin panel for navigating to database record
    search_fields = ('full_name', 'telegram_id')  # fields to search records by
    list_editable = ('blocked',)  # fields that can be edited directly in the record list

    # fields displayed in the edit form, some are non-editable
    fields = ('telegram_id', 'full_name', 'registration_date', 'blocked')


class OlympiadAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'subject', 'title', 'start_date', 'stage', 'is_recognized')  # display these fields
    list_display_links = ('id', 'title')  # clickable fields in admin panel for navigating to database record
    list_editable = ('is_recognized',)  # fields that can be edited directly in the record list
    search_fields = ('subject', 'title')  # fields to search records by

    # fields displayed in the edit form, some are non-editable
    fields = ('subject', 'title', 'start_date', 'stage', 'schedule', 'website', 'is_recognized')


class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'subject', 'user_identifier', 'title', 'start_date', 'stage', 'is_recognized')  # display these fields
    list_display_links = ('user_identifier', 'title')  # clickable fields in admin panel for navigating to database record
    search_fields = ('user_identifier', 'subject', 'title')  # fields to search records by
    list_editable = ('is_recognized',)  # fields that can be edited directly in the record list

    # fields displayed in the edit form, some are non-editable
    fields = ('subject', 'user_identifier', 'title', 'start_date', 'stage', 'schedule', 'website', 'is_recognized')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'feedback_text',)  # display these fields
    search_fields = ('username',)  # fields to search records by


class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'support_request',)  # display these fields
    search_fields = ('telegram_id',)  # fields to search records by


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'payment_data',)  # display these fields
    search_fields = ('telegram_id',)  # fields to search records by


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'photo')  # display these fields
    search_fields = ('name',)  # fields to search records by
    prepopulated_fields = {'slug': ("name",)}  # automatically populate slug field based on name field


class SecretTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'secret_token',)  # display these fields
    list_display_links = ('telegram_id',)  # clickable fields in admin panel for navigating to database record
    search_fields = ('telegram_id',)  # fields to search records by


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'token', 'created_date')  # display these fields
    list_display_links = ('username',)  # clickable fields in admin panel for navigating to database record
    search_fields = ('username',)  # fields to search records by
    fields = ('username', 'token', 'created_date')


class UserTelegramConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'username',)  # display these fields
    list_display_links = ('telegram_id',)  # clickable fields in admin panel for navigating to database record
    search_fields = ('telegram_id', 'username')  # fields to search records by


admin.site.register(SiteRegistration, SiteRegistrationAdmin)
admin.site.register(TelegramRegistration, TelegramRegistrationAdmin)
admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(NotificationSubscription, NotificationSubscriptionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(TechnicalSupport, TechnicalSupportAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SecretToken, SecretTokenAdmin)
admin.site.register(UserTelegramConnection, UserTelegramConnectionAdmin)