import datetime
from secrets import token_hex

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm, LoginUserForm, SecretTokenForm, PasswordReset, PasswordResetForUser, ChangeEmail
from .models import Olympiad, Subject, SecretToken, NotificationSubscription, UserTelegramConnection, SiteRegistration, \
    PasswordReset
from .service import translate_english_letters_into_russian
from .tasks import send_span_email
from .utils import menu, additional_menu, DataMixin


def pagination(search_olympiads, request):
    all_olympiads = search_olympiads
    paginator = Paginator(all_olympiads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, paginator


def main(request):
    return render(request, 'olympic/main.html',
                  {"menu": menu, "additional_menu": additional_menu, 'title': 'Home Page'})


def all_olympiads(request):
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user
            if UserTelegramConnection.objects.filter(username=request.user.username).exists():
                telegram_id = UserTelegramConnection.objects.get(username=request.user.username).telegram_id
                g = NotificationSubscription.objects.filter(user_identifier=telegram_id).all()
                h = NotificationSubscription.objects.filter(user_identifier=usr).all()
                gen = []
                for itm in h:
                    if not g.filter(title=itm.title, start_date=itm.start_date, subject_id=itm.subject).exists():
                        gen.append(itm)
                page_obj, paginator = pagination(gen + list(g), request)
                return render(request, 'olympic/information.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': 'Olympiads',
                               'categories': Subject.objects.all(),
                               'olympiads': gen + list(g),
                               'text': "Show all olympiads",
                               'page_obj': page_obj,
                               'paginator': paginator,
                               'flag': True,
                               })

            page_obj, paginator = pagination(NotificationSubscription.objects.filter(user_identifier=usr).all(), request)
            return render(request, 'olympic/information.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Olympiads',
                           'categories': Subject.objects.all(),
                           'text': "Show all olympiads",
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'flag': True,
                           })

    page_obj, paginator = pagination(Olympiad.objects.all(), request)
    return render(request, 'olympic/information.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Olympiads',
                   'categories': Subject.objects.all(),
                   'page_obj': page_obj,
                   'paginator': paginator,
                   'text': "Show only olympiads with connected notifications",
                   'flag': False,
                   })


def filter_olympiads(request, subject_slug):
    c = Subject.objects.get(slug=subject_slug)
    if request.method == "POST":
        if 'someone' in request.POST['select']:
            usr = request.user.username
            if UserTelegramConnection.objects.filter(username=request.user.username).exists():
                telegram_id = UserTelegramConnection.objects.get(username=request.user.username).telegram_id
                g = NotificationSubscription.objects.filter(user_identifier=telegram_id, subject__slug=subject_slug).all()
                h = NotificationSubscription.objects.filter(user_identifier=usr, subject__slug=subject_slug).all()
                gen = []
                for itm in h:
                    if not g.filter(title=itm.title, start_date=itm.start_date, subject_id=itm.subject).exists():
                        gen.append(itm)

                page_obj, paginator = pagination(gen + list(g), request)
                return render(request, 'olympic/information.html',
                              {"menu": menu,
                               "additional_menu": additional_menu,
                               'title': f'Category - {c.name}',
                               'categories': Subject.objects.all(),
                               'text': "Show all olympiads",
                               'page_obj': page_obj,
                               'paginator': paginator,
                               'flag': True,
                               })

            page_obj, paginator = pagination(NotificationSubscription.objects.filter(user_identifier=usr, subject__slug=subject_slug).all(),
                                             request)
            return render(request, 'olympic/information.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': f'Category - {c.name}',
                           'categories': Subject.objects.all(),
                           'text': "Show all olympiads",
                           'flag': True,
                           'paginator': paginator,
                           'page_obj': page_obj,
                           })
    page_obj, paginator = pagination(Olympiad.objects.filter(subject__slug=subject_slug), request)
    return render(request, 'olympic/information.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': f'Category - {c.name}',
                   'categories': Subject.objects.all(),
                   'text': "Show only olympiads with connected notifications",
                   'page_obj': page_obj,
                   'paginator': paginator,
                   'flag': False,
                   })


def notification_management(request):
    if not request.user.is_authenticated:
        return redirect('home')
    page_obj, paginator = pagination(Olympiad.objects.all(), request)
    if request.method == "POST":
        if 'find' in request.POST:
            search = str(request.POST['search'])
            translate_search = translate_english_letters_into_russian(search)
            search_olympiads = list(
                Olympiad.objects.filter(
                    Q(title__contains=search) |
                    Q(title__contains=search.capitalize()) |
                    Q(title__contains=search.lower()) |
                    Q(title__contains=translate_search) |
                    Q(title__contains=translate_search.capitalize()) |
                    Q(title__contains=translate_search.lower())
                )
            )
            for itm in Subject.objects.filter(
                    Q(name__contains=search.capitalize()) |
                    Q(name__contains=search) |
                    Q(name__contains=search.lower()) |
                    Q(name__contains=translate_search.capitalize()) |
                    Q(name__contains=translate_search) |
                    Q(name__contains=translate_search.lower())
            ).values():
                subject_slug = itm['slug']
                search_olympiads += list(Olympiad.objects.filter(Q(subject__slug__contains=subject_slug)))

            page_obj, paginator = pagination(search_olympiads, request)
            return render(request, 'olympic/notifications.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Connect/Remove Notifications',
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'categories': Subject.objects.all(),
                           'text_for_search': search,
                           })

        elif 'cancel' in request.POST:
            return render(request, 'olympic/notifications.html',
                          {"menu": menu,
                           "additional_menu": additional_menu,
                           'title': 'Connect/Remove Notifications',
                           'page_obj': page_obj,
                           'paginator': paginator,
                           'categories': Subject.objects.all(),
                           'text_for_search': '',
                           })

        elif 'add' in request.POST['select']:
            for itm in request.POST.getlist('choose'):
                title, subject_name = itm.split('это_!!!_бу-бу_разделитель')
                subject_id = Subject.objects.get(name=subject_name).id
                usr = request.user.username
                if not NotificationSubscription.objects.filter(title=title, user_identifier=usr, subject=subject_id).exists():
                    record = Olympiad.objects.get(title=title, subject_id=subject_id)
                    start_date, stage, schedule, website, subject, is_recognized = record.start_date, record.stage, record.schedule, \
                        record.website, record.subject, record.is_recognized
                    NotificationSubscription.objects.create(user_identifier=usr, title=title, start_date=start_date, website=website, stage=stage,
                                                     schedule=schedule, subject=subject, is_recognized=is_recognized)

        elif 'delete' in request.POST['select']:
            for itm in request.POST.getlist('choose'):
                title, subject_name = itm.split('это_!!!_бу-бу_разделитель')
                subject = Subject.objects.get(name=subject_name).id
                usr = request.user.username
                if UserTelegramConnection.objects.filter(username=usr).exists():
                    telegram_id = UserTelegramConnection.objects.get(username=usr).telegram_id
                    if NotificationSubscription.objects.filter(title=title, user_identifier=telegram_id, subject=subject).exists():
                        NotificationSubscription.objects.get(title=title, user_identifier=telegram_id, subject=subject).delete()
                if NotificationSubscription.objects.filter(title=title, user_identifier=usr, subject=subject).exists():
                    NotificationSubscription.objects.get(title=title, user_identifier=usr, subject=subject).delete()

    return render(request, 'olympic/notifications.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Connect/Remove Notifications',
                   'page_obj': page_obj,
                   'paginator': paginator,
                   'categories': Subject.objects.all(),
                   'text_for_search': '',
                   })


def account(request):
    return render(request, 'olympic/account_page.html',
                  {
                      "menu": menu,
                      "additional_menu": additional_menu,
                      'title': 'Personal Account',
                      'email': SiteRegistration.objects.get(username=request.user.username).email
                  })


def change_email(request):
    if request.method == "POST":
        new_email = request.POST['new_email']
        u = SiteRegistration.objects.get(username=request.user.username)
        u.email = new_email
        u.save()
        return render(request, 'olympic/account_page.html',
                      {
                          "menu": menu,
                          "additional_menu": additional_menu,
                          'title': 'Personal Account',
                          'email': SiteRegistration.objects.get(username=request.user.username).email
                      })
    return render(request, 'olympic/change_email.html', {
        "menu": menu,
        "additional_menu": additional_menu,
        'title': 'Change Email',
        'form': ChangeEmail(),
    })


def password_reset(request):
    if request.method == 'POST':
        usr_or_email, usr = request.POST['login_or_email'], ''
        if SiteRegistration.objects.filter(username=usr_or_email).exists():
            usr = SiteRegistration.objects.get(username=usr_or_email)
        elif SiteRegistration.objects.filter(email=usr_or_email).exists():
            usr = SiteRegistration.objects.get(email=usr_or_email)
        if usr != '':
            tkn = token_hex(32)
            reset_url = (request.build_absolute_uri() + tkn)
            data = {
                'username': usr.username,
                'url': reset_url,
            }
            html_body = render_to_string('olympic/email_templates/reset_password.html', data)
            now = datetime.datetime.now().strftime('%Y-%m-%d')
            PasswordReset.objects.create(username=usr.username, token=tkn, created_date=now)
            send_span_email.delay('Password-Reset-[olympic]', usr.email, html_body)
            return redirect('login')
    return render(request, 'olympic/password_reset.html', {
        "menu": menu,
        "additional_menu": additional_menu,
        'title': 'Password Reset',
        'form': PasswordReset(),
    })


def password_reset_for_user(request, token):
    if not PasswordReset.objects.filter(token=token).exists():
        return redirect('home')
    if request.method == 'POST':
        new_password = request.POST['new_password']
        username = PasswordReset.objects.get(token=token).username
        u = User.objects.get(username__exact=username)
        u.set_password(new_password)
        u.save()
        PasswordReset.objects.get(token=token).delete()
        return redirect('login')
    return render(request, 'olympic/password_reset_for_usr.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Password Reset',
                   'form': PasswordResetForUser(),
                   })


def telegram_token(request):
    if not request.user.is_authenticated:
        return redirect('home')
    alert_text = ''
    if request.method == 'POST':
        if 'password' in request.POST:
            token = request.POST['password']
            if SecretToken.objects.filter(secret_token=token).exists():
                tg_id = SecretToken.objects.get(secret_token=token).telegram_id
                if not UserTelegramConnection.objects.filter(telegram_id=tg_id).exists():
                    UserTelegramConnection.objects.create(telegram_id=tg_id, username=request.user)
            else:
                alert_text = 'No Telegram account with such Secret Token'
        else:
            UserTelegramConnection.objects.filter(username=request.user).delete()
    usr = request.user.username
    flag = UserTelegramConnection.objects.filter(username=usr).exists()
    return render(request, 'olympic/secret_token_pager.html',
                  {"menu": menu,
                   "additional_menu": additional_menu,
                   'title': 'Telegram Bot Synchronization',
                   'form': SecretTokenForm(),
                   'flag': flag,
                   'alert_text': alert_text,
                   })


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'olympic/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        SiteRegistration.objects.create(username=self.request.POST['username'], email=self.request.POST['email'],
                                        registration_date=datetime.datetime.now().strftime('%d-%m-%Y'),
                                        blocked=False)
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'olympic/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)  # logout from authorization
    return redirect('login')


def error_404(request, exception):
    context = {}
    context['page_title'] = '404'
    context['menu'] = menu
    response = render(request, 'olympic/404.html', context=context)
    response.status_code = 404
    return response
