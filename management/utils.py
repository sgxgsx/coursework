from django.views import generic
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from dashboard.views import get_show_all_form_data, get_needed_items, DetailDraft
from dashboard.utils import check_item, finish_draft
from dashboard.models import Draft, Contract, check_if_manager, Client
from dashboard.const import SQL_GET_DRAFTS_BY_USER, SQL_GET_CONTRACT_BY_USER, DRAFTS_MANAGEMENT_DETAIL_REDIRECT
from dashboard.const import SQL_1_GET_CLIENT_CONTACT
from django.db import connection
from fpdf import FPDF
from dashboard.const import SQL_3_GET_ACCOUNT_BETWEEN_DATE, SQL_3_GET_PAYMENTS_BETWEEN_DATE




def get_like(sql, text):
    with connection.cursor() as cur:
        cur.execute(sql.format(text))
        return cur.fetchall()



def do_between(s, d1, d2):
    print(d1)
    print(d2)
    if s == 1:
        with connection.cursor() as cur:
            cur.execute(SQL_3_GET_PAYMENTS_BETWEEN_DATE.format(d1,d2))
            return cur.fetchall()
    elif s == 0:
        with connection.cursor() as cur:
            cur.execute(SQL_3_GET_ACCOUNT_BETWEEN_DATE.format(d1, d2))
            return cur.fetchall()
    else:
        return None

