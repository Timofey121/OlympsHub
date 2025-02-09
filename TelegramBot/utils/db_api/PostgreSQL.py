# -*- coding: utf8 -*-
import sqlite3

import psycopg2

from data.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT


def main():
    global con, cur
    con = psycopg2.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )
    cur = con.cursor()

async def add_user(telegram_id, full_name, blocked, data_registration):
    main()
    cur.execute(
        f"INSERT INTO RegistrationTelegram (telegram_id, full_name, blocked, data_registration) "
        f"VALUES('{telegram_id}', '{full_name}', '{blocked}', '{data_registration}')")
    con.commit()
    con.close()


async def select_all_users():
    main()
    cur.execute(f"SELECT * FROM RegistrationTelegram WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows


async def subscriber_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM RegistrationTelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def all_feedback():
    main()
    cur.execute(f"SELECT * FROM Feedback")
    rows = cur.fetchall()
    con.close()
    return rows


async def check_secret_token(secret_token):
    main()
    cur.execute(f"SELECT telegram_id, secret_token FROM SecretToken WHERE secret_token='{secret_token}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def secret_token_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM SecretToken WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_token(telegram_id, token):
    main()
    cur.execute(
        f"INSERT INTO SecretToken (telegram_id, secret_token) "
        f"VALUES('{telegram_id}', '{token}')")
    con.commit()
    con.close()


async def count_users():
    main()
    cur.execute(f"SELECT COUNT(*) FROM RegistrationTelegram WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows


async def count_olympiads():
    main()
    cur.execute(f"SELECT COUNT(*) FROM Olympiads")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_user_feedback(customer, Feedback):
    main()
    cur.execute(
        f"INSERT INTO Feedback (customer, Feedback) VALUES('{customer}', '{Feedback}')")
    con.commit()
    con.close()


async def add_user_tech(customer, help):
    main()
    cur.execute(f"INSERT INTO TechnicalSupport (customer, help) VALUES('{customer}', '{help}')")
    con.commit()
    con.close()


async def add_notification_dates(customer, title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(f"INSERT INTO NotificationDates (customer, title, start, stage, schedule, site, rsoch, sub_id) "
                f"VALUES('{customer}', '{title}', '{start}', '{stage}', '{schedule}', '{site}', '{rsoch}', '{sub}')")
    con.commit()
    con.close()


async def check_blocked(telegram_id):
    main()
    cur.execute(f"SELECT blocked FROM RegistrationTelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def update_blocked_users(telegram_id, blocked):
    main()
    cur.execute(
        f"UPDATE RegistrationTelegram SET blocked='{blocked}' WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def select_blocked_users():
    main()
    cur.execute(f"SELECT * FROM RegistrationTelegram WHERE blocked=True")
    rows = cur.fetchall()
    con.close()
    return rows


async def information_about_olympiads(sub_id):
    main()
    cur.execute(
        f"SELECT title, start, stage, schedule, site, rsoch, sub_id FROM Olympiads WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def data_olympiads(sub_id):
    main()
    cur.execute(
        f"SELECT title, start, stage, schedule, site, rsoch, sub_id FROM Olympiads WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT start FROM NotificationDates WHERE customer='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_yes_or_no_in_notifications(customer, title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"SELECT start FROM NotificationDates WHERE customer='{customer}' AND title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_info(sub_id):
    main()
    cur.execute(f"SELECT telegram_id FROM NotificationDates WHERE sub_id={sub_id}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_sub(sub_id):
    main()
    cur.execute(f"SELECT subject FROM Subjects WHERE id={sub_id}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_subjects_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT sub_id FROM NotificationDates WHERE customer='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_sub_info(telegram_id):
    main()
    cur.execute(
        f"SELECT customer, title, start, stage, schedule, site, rsoch, sub_id FROM NotificationDates "
        f"WHERE customer='{telegram_id}' ORDER BY sub_id")
    rows = cur.fetchall()
    con.close()
    return rows


async def select(telegram_id, sub_id):
    main()
    cur.execute(
        f"SELECT rsoch FROM NotificationDates WHERE customer='{telegram_id}' AND sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_user(telegram_id):
    main()
    cur.execute(
        f"SELECT * FROM UserNameAndTelegramID WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_subject(sub_id):
    main()
    cur.execute(f"SELECT start FROM NotificationDates WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def del_data_in_olimpic(customer, sub_id):
    main()
    cur.execute(
        f"DELETE FROM NotificationDates WHERE customer = '{customer}' AND sub_id = '{sub_id}'")
    con.commit()
    con.close()


async def del_olympic(title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"DELETE FROM NotificationDates WHERE title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_olympic_in_olympiads_parsing(title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"DELETE FROM Olympiads WHERE title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_feedback():
    main()
    cur.execute(
        f"DELETE FROM Feedback")
    con.commit()
    con.close()


async def del_notification():
    main()
    cur.execute(
        f"DELETE FROM NotificationDates")
    con.commit()
    con.close()


async def select_sub_id(sub):
    main()
    cur.execute(
        f"SELECT id FROM Subjects WHERE subject='{sub}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def del_notif_in_olimpic(telegram_id, title, start, stage, site, sub):
    main()
    cur.execute(
        f"DELETE FROM NotificationDates WHERE customer = '{telegram_id}' AND title='{title}' AND start='{start}'"
        f" AND stage='{stage}'  AND site='{site}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_tech(tag, help):
    main()
    cur.execute(
        f"DELETE FROM TechnicalSupport WHERE customer = '{tag}' AND help = '{help}'")
    con.commit()
    con.close()


async def all_tech_failed():
    main()
    cur.execute(f"SELECT customer, help FROM TechnicalSupport")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_infor_id():
    main()
    cur.execute(f"SELECT customer, title, start, stage, schedule, site, rsoch, sub_id FROM NotificationDates")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_tg_or_site(telegram_id):
    main()
    cur.execute(f"SELECT telegram_id,blocked FROM RegistrationTelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_site(customer):
    main()
    cur.execute(f"SELECT customer,email,blocked FROM RegistrationSite WHERE customer='{customer}'")
    rows = cur.fetchall()
    con.close()
    return rows
