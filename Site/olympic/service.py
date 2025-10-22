import time

import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from xvfbwrapper import Xvfb

from .models import Subject, Olympiad, NotificationSubscription
from .templates.dictionary import numbers, months, months2, subjects_rsosh


def send_email(name_email, user, body):
    send_mail(name_email, '', 'from@example.com', [user], html_message=body, fail_silently=False, )


def translate_english_letters_into_russian(text: str):
    layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                               'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'), "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                                                      'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
    return text.translate(layout)


def add_olympiads_to_bd():
    print('Run parsing')

    # subjects = 'Computer Science, Mathematics, Physics, Chemistry, Biology, Geography, History, Social Studies, Law, ' \
    #            'Economics, Russian Language, Literature, English Language, ' \
    #            'French Language, German Language, Astronomy, Robotics, ' \
    #            'Technology, Art, Drafting, Psychology'.split(', ')

    subjects = Subject.objects.all()

    vdisplay = Xvfb()
    vdisplay.start()
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")  # New headless mode (recommended for Chrome 112+)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")  # Solution for limited memory in containers
    chrome_options.add_argument("--disable-gpu")  # Disable GPU as it's not needed in headless mode
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size (important for some websites)

    service = ChromeService(ChromeDriverManager().install(), log_path="/home/app/web/chromedriver.log")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    time.sleep(1)
    for i in range(len(subjects)):
        try:
            sub_id = Subject.objects.get(name=subjects[i]).id
            subject = subjects[i].name
            print("Parse " + subject)

            URL = f'https://olimpiada.ru/activities?type=any&subject%5B{numbers[subject.strip().capitalize()]}' \
                  f'%5D=on&class=any&period_date=&period=week'
            driver.get(URL)

            while 'Проверка браузера перед переходом на сайт olimpiada.ru' in driver.page_source:
                time.sleep(1)

            for j in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.05)

            html = driver.page_source

            soup = BeautifulSoup(html, "lxml")

            a = soup.find_all('a', 'none_a black olimp_desc')
            Olympiad.objects.filter(subject=sub_id).all().delete()
            for item in a:
                try:
                    url = "https://olimpiada.ru" + item.get('href')
                    req = requests.get(url=url)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    title = soup.find_all('title')[0].text.strip().upper()

                    href_olimp = soup.find_all('div', 'contacts')[0].find('a', 'color').get('href')

                    fg = "https://olimpiada.ru" + soup.find_all('tr', 'notgreyclass')[0].find("a").get('href')

                    if fg != 'Расписание олимпиады в этом году пока не известно':
                        url = fg
                        req = requests.get(url=url)
                        src = req.text
                        soup = BeautifulSoup(src, "lxml")

                        step = soup.find('div', 'right').find('h1').text
                        data_start1 = (soup.find('span', 'main_date red').text.strip().replace('\n', '').replace('20',
                                                                                                                 ' 20').replace(
                            '!', '').replace('До', '')).strip().replace(' ', ' ').split('...')[0]

                        data_start = ''
                        for item2 in months2:
                            if item2 in data_start1:
                                data_start1 = data_start1.split(item2.strip())
                                if len(data_start1[0]) == 0:
                                    data_start1 = data_start1[1]

                                data_start = f"{data_start1[-1].strip()}-{months[item2.strip()]}-" \
                                             f"{('0' * (2 - len(data_start1[0].strip())))}{data_start1[0].split('-')[0].strip()}"
                        start = data_start.split('-')
                        try:
                            if len(start[-1]) < 2:
                                start[-1] = '0' + start[-1]
                        except Exception as ex:
                            pass
                        start.reverse()
                        start = '-'.join(start)
                        stage = step
                        schedule = fg
                        site = href_olimp
                        f = (title in subjects_rsosh[subject.lower().capitalize()])
                        Olympiad.objects.create(title=title, start_date=start, stage=stage, schedule=schedule, website=site,
                                                 is_recognized=f, subject_id=sub_id).save()

                        for tg in NotificationSubscription.objects.filter(subject_id=sub_id).all():
                            if NotificationSubscription.objects.filter(tg.user_identifier, title, start, stage, schedule, site, f,
                                                                subject_id).exists():
                                flag = bool(NotificationSubscription.objects.get(tg.user_identifier, subject_id).is_recognized)
                                if (flag is False) or (f is True and flag is True):
                                    NotificationSubscription.objects.create(tg.user_identifier, title, start, stage, schedule, site,
                                                                     f, subject_id).save()
                except Exception as ex:
                    pass
        except Exception as ex:
            pass

    driver.close()
    vdisplay.stop()
