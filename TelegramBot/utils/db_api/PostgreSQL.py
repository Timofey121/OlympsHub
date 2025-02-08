# -*- coding: utf8 -*-
import sqlite3

import psycopg2

from TelegramBot.data.config import POSTGRES_USER, POSTGRES_PASSWORD, HOST, POSTGRES_DB


def main():
    global con, cur

    con = psycopg2.connect(user=POSTGRES_USER,
                           # пароль, который указали при установке PostgreSQL
                           password=POSTGRES_PASSWORD,
                           host=HOST,
                           port="5432")

async def add_user(telegram_id, full_name, blocked, data_registration):
    main()
    cur.execute(
        f"INSERT INTO olympic_registrationtelegram (telegram_id, full_name, blocked, data_registration) "
        f"VALUES('{telegram_id}', '{full_name}', '{blocked}', '{data_registration}')")
    con.commit()
    con.close()


async def select_all_users():
    main()
    cur.execute(f"SELECT * FROM olympic_registrationtelegram WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows


async def subscriber_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM olympic_registrationtelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def all_feedback():
    main()
    cur.execute(f"SELECT * FROM olympic_feedback")
    rows = cur.fetchall()
    con.close()
    return rows


async def check_secret_token(secret_token):
    main()
    cur.execute(f"SELECT telegram_id, secret_token FROM olympic_secrettoken WHERE secret_token='{secret_token}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def secret_token_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM olympic_secrettoken WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_token(telegram_id, token):
    main()
    cur.execute(
        f"INSERT INTO olympic_secrettoken (telegram_id, secret_token) "
        f"VALUES('{telegram_id}', '{token}')")
    con.commit()
    con.close()


async def count_users():
    main()
    cur.execute(f"SELECT COUNT(*) FROM olympic_registrationtelegram WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows


async def count_olympiads():
    main()
    cur.execute(f"SELECT COUNT(*) FROM olympic_olympiads")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_user_feedback(customer, feedback):
    main()
    cur.execute(
        f"INSERT INTO olympic_feedback (customer, feedback) VALUES('{customer}', '{feedback}')")
    con.commit()
    con.close()


async def add_user_tech(customer, help):
    main()
    cur.execute(f"INSERT INTO olympic_technicalsupport (customer, help) VALUES('{customer}', '{help}')")
    con.commit()
    con.close()


async def add_notification_dates(customer, title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(f"INSERT INTO olympic_notificationdates (customer, title, start, stage, schedule, site, rsoch, sub_id) "
                f"VALUES('{customer}', '{title}', '{start}', '{stage}', '{schedule}', '{site}', '{rsoch}', '{sub}')")
    con.commit()
    con.close()


async def check_blocked(telegram_id):
    main()
    cur.execute(f"SELECT blocked FROM olympic_registrationtelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def update_blocked_users(telegram_id, blocked):
    main()
    cur.execute(
        f"UPDATE olympic_registrationtelegram SET blocked='{blocked}' WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def select_blocked_users():
    main()
    cur.execute(f"SELECT * FROM olympic_registrationtelegram WHERE blocked=True")
    rows = cur.fetchall()
    con.close()
    return rows


async def information_about_olympiads(sub_id):
    main()
    cur.execute(
        f"SELECT title, start, stage, schedule, site, rsoch, sub_id FROM olympic_olympiads WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def data_olympiads(sub_id):
    main()
    cur.execute(
        f"SELECT title, start, stage, schedule, site, rsoch, sub_id FROM olympic_olympiads WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT start FROM olympic_notificationdates WHERE customer='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_yes_or_no_in_notifications(customer, title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"SELECT start FROM olympic_notificationdates WHERE customer='{customer}' AND title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_info(sub_id):
    main()
    cur.execute(f"SELECT telegram_id FROM olympic_notificationdates WHERE sub_id={sub_id}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_sub(sub_id):
    main()
    cur.execute(f"SELECT subject FROM olympic_subjects WHERE id={sub_id}")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_subjects_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT sub_id FROM olympic_notificationdates WHERE customer='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_sub_info(telegram_id):
    main()
    cur.execute(
        f"SELECT customer, title, start, stage, schedule, site, rsoch, sub_id FROM olympic_notificationdates "
        f"WHERE customer='{telegram_id}' ORDER BY sub_id")
    rows = cur.fetchall()
    con.close()
    return rows


async def select(telegram_id, sub_id):
    main()
    cur.execute(
        f"SELECT rsoch FROM olympic_notificationdates WHERE customer='{telegram_id}' AND sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_user(telegram_id):
    main()
    cur.execute(
        f"SELECT * FROM olympic_usernameandtelegramid WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_subject(sub_id):
    main()
    cur.execute(f"SELECT start FROM olympic_notificationdates WHERE sub_id='{sub_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def del_data_in_olimpic(customer, sub_id):
    main()
    cur.execute(
        f"DELETE FROM olympic_notificationdates WHERE customer = '{customer}' AND sub_id = '{sub_id}'")
    con.commit()
    con.close()


async def del_olympic(title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"DELETE FROM olympic_notificationdates WHERE title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_olympic_in_olympiads_parsing(title, start, stage, schedule, site, rsoch, sub):
    main()
    cur.execute(
        f"DELETE FROM olympic_olympiads WHERE title='{title}' AND start='{start}'"
        f" AND stage='{stage}' AND schedule='{schedule}' AND site='{site}' AND rsoch='{rsoch}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_feedback():
    main()
    cur.execute(
        f"DELETE FROM olympic_feedback")
    con.commit()
    con.close()


async def del_notification():
    main()
    cur.execute(
        f"DELETE FROM olympic_notificationdates")
    con.commit()
    con.close()


async def select_sub_id(sub):
    main()
    cur.execute(
        f"SELECT id FROM olympic_subjects WHERE subject='{sub}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def del_notif_in_olimpic(telegram_id, title, start, stage, site, sub):
    main()
    cur.execute(
        f"DELETE FROM olympic_notificationdates WHERE customer = '{telegram_id}' AND title='{title}' AND start='{start}'"
        f" AND stage='{stage}'  AND site='{site}' AND sub_id={sub}")
    con.commit()
    con.close()


async def del_tech(tag, help):
    main()
    cur.execute(
        f"DELETE FROM olympic_technicalsupport WHERE customer = '{tag}' AND help = '{help}'")
    con.commit()
    con.close()


async def all_tech_failed():
    main()
    cur.execute(f"SELECT customer, help FROM olympic_technicalsupport")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_infor_id():
    main()
    cur.execute(f"SELECT customer, title, start, stage, schedule, site, rsoch, sub_id FROM olympic_notificationdates")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_tg_or_site(telegram_id):
    main()
    cur.execute(f"SELECT telegram_id,blocked FROM olympic_registrationtelegram WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_site(customer):
    main()
    cur.execute(f"SELECT customer,email,blocked FROM olympic_registrationsite WHERE customer='{customer}'")
    rows = cur.fetchall()
    con.close()
    return rows
