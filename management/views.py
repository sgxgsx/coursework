from django.views import generic
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, FileResponse
from django.db import connection
from dashboard.views import get_show_all_form_data, get_needed_items, DetailDraft
from dashboard.utils import check_item, finish_draft, cursor_exec_get, insert_history
from dashboard.models import Draft, Contract, check_if_manager, Client, MyUser, History
from dashboard.const import SQL_GET_DRAFTS_BY_USER, SQL_GET_CONTRACT_BY_USER, DRAFTS_MANAGEMENT_DETAIL_REDIRECT, MANAGEMENT_REDIRECT, HISTORY_STRING
from dashboard.const import SQL_1_GET_CLIENT_CONTACT, SQL_2_GET_NAME_LIKE_EMAIL, SQL_2_GET_TITLE_LIKE_PART, SQL_4_SUM_DRAFT_PRICE, SQL_4_AVG_USER_HOUR_AMOUNT, SQL_5_SUM_GROUP_PAYED_CONTRACT, SQL_5_AVG_GROUP_USER_HOUR_AMOUNT
from fpdf import FPDF
from .forms import FetchForm, BetweenForm
from .utils import get_like, do_between
import datetime
# Create your views here.


def get_data(sql):
    with connection.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

def normalize(p):
    p = [list(i) for i in p]
    g = list()
    for i in p:
        d = list()
        for u in i:
            if u is None:
                d.append('0')
            else:
                d.append(str(u))
        g.append(d)
    return g

@login_required(login_url='/accounts/logout/')
@user_passes_test(check_if_manager, login_url='/accounts/logout')
def report_draft(request, pk):
    insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
    draft = Draft.objects.get(pk=pk)
    contract = Contract.objects.get(pk=draft.contractId_id)
    user = MyUser.objects.get(pk=contract.userId_id)
    items = get_needed_items(pk=pk)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=25)
    pdf.cell(200, 10, txt=user.name, ln=1, align="C")
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="Report " + contract.title, ln=1, align="C")
    pdf.set_font("Arial", size=12)
    for i in draft.text.split("\n"):
        pdf.cell(200, 10, txt=i, ln=1, align="L")
    for item in items:
        if item.satisfied:
            pdf.cell(200, 10, txt=item.type + " Satisfied", ln=1, align="L")
        else:
            pdf.cell(200, 10, txt=item.type + " not satisfied", ln=1, align="L")

    pdf.output("some.pdf")
    response = FileResponse(open('some.pdf', 'rb'))
    return response

@login_required(login_url='/accounts/logout/')
@user_passes_test(check_if_manager, login_url='/accounts/logout')
def report_all(request):
    insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with connection.cursor() as cur:
        cur.execute(SQL_5_SUM_GROUP_PAYED_CONTRACT)
        p = cur.fetchall()
        cur.execute(SQL_5_AVG_GROUP_USER_HOUR_AMOUNT)
        c = cur.fetchall()
        p.insert(0, ['Client', 'Contract', 'Price'])
        p = normalize(p)
        c.insert(0, ['Employee', 'Average hours'])
        c = normalize(c)
        ooo = get_data(SQL_1_GET_CLIENT_CONTACT)
        ooo.insert(0, ['Client', 'Contract'])
        ooo = normalize(ooo)
    col_height = col_width = pdf.w / 4.5
    row_height = pdf.font_size
    print(p)
    pdf.cell(200, 10, txt='Table # 1\n', ln=1, align="C")
    for row in p:
        for item in row:
            pdf.cell(col_width, row_height*1, txt=item, border=1)
        pdf.ln(row_height*1)
    pdf.cell(200, 10, txt='Table # 2\n', ln=1, align="C")
    for row in c:
        for item in row:
            pdf.cell(col_width, row_height * 1, txt=item, border=1)
        pdf.ln(row_height * 1)
    pdf.cell(200, 10, txt='Table # 3\n', ln=1, align="C")
    for row in ooo:
        for item in row:
            pdf.cell(col_width, row_height * 1, txt=item, border=1)
        pdf.ln(row_height * 1)
    pdf.output("some.pdf")
    response = FileResponse(open('some.pdf', 'rb'))
    return response


@login_required(login_url='/accounts/logout/')
@user_passes_test(check_if_manager, login_url='/accounts/logout')
def report(request, pk):
    insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
    draft = Draft.objects.get(pk=pk)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i in draft.text.split("\n"):
        pdf.cell(200, 10, txt=i, ln=1, align="C")
    pdf.output("some.pdf")
    return redirect(DRAFTS_MANAGEMENT_DETAIL_REDIRECT.format(pk))


@login_required(login_url='/accounts/logout/')
@user_passes_test(check_if_manager, login_url='/accounts/logout')
def finish(request, pk):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        d = finish_draft(pk)
        return redirect(DRAFTS_MANAGEMENT_DETAIL_REDIRECT.format(pk))
    except Exception as e:
        print(e)
    return HttpResponse(status=400)


@method_decorator(login_required, name='dispatch')
class DetailManagementDraft(generic.TemplateView):
    template_name = 'managementdrafts.html'

    def get_context_data(self, **kwargs):
        context = super(DetailManagementDraft, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        return context

    def get_draft_data(self, context, **kwargs):
        context['drafts'] = Draft.objects.all()
        if 'pk' in kwargs:
            try:
                pk = kwargs['pk']
                context['draft'] = Draft.objects.get(pk=pk)
                context['items'] = get_needed_items(pk=pk)
            except Exception as e:
                print(e)
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if not check_if_manager(request.user):
            return redirect('/accounts/logout/')
        if request.method == 'POST':
            return self.post()
        return super(DetailManagementDraft, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        context = super(DetailManagementDraft, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        return render(self.request, 'managementdrafts.html', context)


@method_decorator(login_required, name='dispatch')
class DetailManagementContract(generic.TemplateView):
    template_name = 'managementcontracts.html'

    def get_context_data(self, **kwargs):
        context = super(DetailManagementContract, self).get_context_data(**kwargs)
        context = self.get_contract_data(context, **kwargs)
        return context

    def get_contract_data(self, context, **kwargs):
        context['contracts'] = Contract.objects.all()
        if 'pk' in kwargs:
            try:
                contract = Contract.objects.get(pk=kwargs['pk'])
                context['contract'] = contract
                if contract.taken == 1:
                    with connection.cursor() as cur:
                        cur.execute(SQL_4_AVG_USER_HOUR_AMOUNT.format(contract.userId_id))
                        sss = cur.fetchall()[0]
                        context['average'] = sss
                with connection.cursor() as cur:
                    cur.execute(SQL_4_SUM_DRAFT_PRICE.format(contract.id))
                    ddd = cur.fetchall()[0]
                    context['sum_draft'] = ddd
                print('kkk')
            except Exception as e:
                print(e)
                print('hui')
        print(context)
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if not check_if_manager(request.user):
            return redirect('/accounts/logout/')
        if request.method == 'POST':
            return self.post()
        return super(DetailManagementContract, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        context = super(DetailManagementContract, self).get_context_data(**kwargs)
        context.update(self.get_contract_data(context, **kwargs))
        return render(self.request, 'managementcontracts.html', context)


@method_decorator(login_required, name='dispatch')
class DetailStats(generic.TemplateView):
    template_name = 'management_stat.html'

    def get_context_data(self, **kwargs):
        context = super(DetailStats, self).get_context_data(**kwargs)
        context = self.get_contract_data(context, **kwargs)
        return context

    def get_contract_data(self, context, **kwargs):
        get_data(SQL_1_GET_CLIENT_CONTACT)
        context['data'] = get_data(SQL_1_GET_CLIENT_CONTACT)
        with connection.cursor() as cur:
            cur.execute(SQL_5_SUM_GROUP_PAYED_CONTRACT)
            p = cur.fetchall()
            print(p)
            context['avg_group_contract'] = p
            cur.execute(SQL_5_AVG_GROUP_USER_HOUR_AMOUNT)
            c = cur.fetchall()
            context['avg_group_user'] = c
        if 'pk' in kwargs:
            try:
                contract = Contract.objects.get(pk=kwargs['pk'])
            except Exception as e:
                print(e)
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if not check_if_manager(request.user):
            return redirect('/accounts/logout/')
        if request.method == 'POST':
            return self.post()
        return super(DetailStats, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        context = super(DetailStats, self).get_context_data(**kwargs)
        context.update(self.get_contract_data(context, **kwargs))
        form = FetchForm(self.request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            select = form.cleaned_data['select']
            try:
                if select == 1:
                    u = get_like(SQL_2_GET_TITLE_LIKE_PART, text)
                    print(u)
                    context['numbertwo'] = u
                    print(context)
                elif select == 0:
                    u = get_like(SQL_2_GET_NAME_LIKE_EMAIL, text)
                    print(u)
                    context['numbertwo'] = u
                    print(context)
            except Exception as e:
                print(e)
                return redirect(MANAGEMENT_REDIRECT, context)
        fr = BetweenForm(self.request.POST)
        print('ss')
        print(self.request.POST)
        if fr.is_valid():
            print('no')
            print(form.cleaned_data)
            date1 = self.request.POST['datef']
            date2 = self.request.POST['datel']
            select = self.request.POST['select2'][0]
            try:
                v = do_between(int(select), date1, date2)
                context['between'] = v


            except Exception as e:
                print(e)
                return render(self.request, 'management_stat.html', context)

        return render(self.request, 'management_stat.html', context)


@method_decorator(login_required, name='dispatch')
class DetailHistory(generic.TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        insert_history(HISTORY_STRING.format(self.request.user.name, self.request.method, self.request.build_absolute_uri()))
        context = super(DetailHistory, self).get_context_data(**kwargs)
        obj = History.objects.all()
        lis = list()
        for i in obj:
            c = int(i.time) + 3600*2
            u = datetime.datetime.utcfromtimestamp(c).strftime('%Y-%m-%d %H:%M:%S')
            print(u)
            i.time = u
        context['data'] = obj
        print(context)
        print(kwargs)
        return context
