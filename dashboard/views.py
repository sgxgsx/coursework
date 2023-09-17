from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from dashboard.utils import populate_db, analyse, generate_requirements, add_needed_items_to_draft, get_needed_items, check_item, satisfy_item, finish_draft, order_write, satisfy_all_possible_items, get_item_id, update_text, insert_history
from .models import Supplier, Contract, Draft, Item, ItemSupplier, DraftItem, check_if_manager, MyUser
from .const import DRAFTS_DETAIL_REDIRECT, SQL_SELECT_SUPPLIERS_BY_ITEM, SQL_GET_DRAFTS_BY_USER, SQL_GET_SUPPLIER_ITEM, SQL_GET_CONTRACT_BY_USER, HISTORY_STRING
from .forms import ShowAllForm, OrderForm, TextForm
from fpdf import FPDF
from random import randint, random

#                              CAN BE MOVED


@login_required(login_url='/accounts/logout/')
def update_for(request, pk):
    insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
    print("ssfsf")
    if request.method == 'POST':
        form = TextForm(request.POST)
        print("form")
        if form.is_valid():
            text = form.cleaned_data['text']
            print(text)
            update_text(pk, text)
            print("success")
    return redirect(DRAFTS_DETAIL_REDIRECT.format(pk))


@login_required(login_url='/accounts/logout/')
def report(request, pk):
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


def get_show_all_form_data(post_data, context, **kwargs):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        form = ShowAllForm(post_data)
        if form.is_valid():
            show_all = form.cleaned_data['showall']
            if show_all == 0:
                context['showall'] = 1
            else:
                context['showall'] = 0
            print(show_all)
        else:
            context['showall'] = 0
    except Exception as e:
        print(e)
    return context


@login_required(login_url='/accounts/logout/')
def satisfy(request, pk, ipk):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        d = satisfy_item(pk, ipk)
        if not d:
            print("errr")
        response = redirect(DRAFTS_DETAIL_REDIRECT.format(pk))
        return response
    except Exception as e:
        print(e)
    return HttpResponse(status=400)


@login_required(login_url='/accounts/logout/')
def satisfy_all_possible(request, pk):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        satisfy_all_possible_items(pk)
        return redirect(DRAFTS_DETAIL_REDIRECT.format(pk))
    except Exception as e:
        print(e)
    return HttpResponse(status=400)

@login_required(login_url='/accounts/logout/')
def finish(request, pk):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        print(pk)
        print('chees')
        d = finish_draft(pk)
        if not d:
            print("err")
        response = redirect(DRAFTS_DETAIL_REDIRECT.format(pk))
        return response
    except Exception as e:
        print(e)
    return HttpResponse(status=400)


def some_test_view(request):
    populate_db()
    return HttpResponse(str("ssar qw"))



#       VIEWS

@login_required(login_url='/accounts/logout/')
def create_draft(request, pk):
    #try:
    insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
    contract = Contract.objects.get(pk=pk)
    if contract.userId is None and request.method == 'POST':
        title = "Draft of : \"" + contract.title + "\""
        draft = Draft.objects.create(title=title, text=contract.content, contractId=contract)
        Contract.objects.filter(pk=contract.id).update(userId=request.user, taken=True)
        print("saf")
        add_needed_items_to_draft(contract.needed, draft)                                          # adds DraftItem
        response = redirect(DRAFTS_DETAIL_REDIRECT.format(draft.id))
        return response
    #except Exception as e:
    #    print(e)
    return HttpResponse(status=400)


@login_required(login_url='/accounts/logout/')
def delete_draft(request, pk):
    try:
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        draft = Draft.objects.get(pk=pk)
        contract = Contract.objects.get(pk=draft.contractId.id)
        if request.user.id == contract.userId.id and request.method == 'POST':
            draft.delete()
            Contract.objects.filter(pk=contract.id).update(taken=False, userId=None)
            redirect_path = "/dashboard/drafts"
            response = redirect(redirect_path)
            return response
    except Exception as e:
        print(e)
        pass
    return HttpResponse(status=400)


@method_decorator(login_required, name='dispatch')
class DetailSupplier(generic.TemplateView):
    template_name = 'suppliers.html'

    def get_context_data(self, **kwargs):
        insert_history(HISTORY_STRING.format(self.request.user.name, self.request.method, self.request.build_absolute_uri()))
        context = super(DetailSupplier, self).get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        if 'pk' in kwargs:
            supplier = Supplier.objects.get(pk=kwargs['pk'])
            sql = "SELECT * FROM dashboard_item WHERE id in (select item_id FROM dashboard_itemsupplier WHERE supplier_id=%s)"
            context['supplier'] = supplier
            context['supplier_items'] = Supplier.objects.raw(sql, [supplier.id])
        print("sss")
        if 'showall' in kwargs and self.request.method == 'POST':
            show_all = kwargs['showall']
            try:
                if show_all == 0:
                    context['showall'] = 1
                else:
                    context['showall'] = 0
            except Exception as e:
                print(e)

        print(kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class DetailDraft(generic.TemplateView):
    template_name = 'drafts.html'

    def get_context_data(self, **kwargs):
        context = super(DetailDraft, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        return context

    def get_draft_data(self, context, **kwargs):
        context['drafts'] = Draft.objects.raw(SQL_GET_DRAFTS_BY_USER, [self.request.user.id])
        if 'pk' in kwargs:
            try:
                pk = kwargs['pk']
                context['draft'] = Draft.objects.get(pk=pk)
                context['items'] = get_needed_items(pk=pk)
                if 'update' in kwargs:
                    context['update_form'] = True
                if 'ipk' in kwargs:
                    context['item_check'] = check_item(pk, kwargs['ipk'])[0]                      # TODO redirect to url#ITEMTYPE
                print(context['items'])
            except Exception as e:
                print(e)
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if request.method == 'POST':
            return self.post()
        return super(DetailDraft, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        context = super(DetailDraft, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        context.update(get_show_all_form_data(self.request.POST, context, **kwargs))
        return render(self.request, 'drafts.html', context)


@method_decorator(login_required, name='dispatch')
class DetailContract(generic.TemplateView):
    template_name = 'contracts.html'

    def get_context_data(self, **kwargs):
        context = super(DetailContract, self).get_context_data(**kwargs)
        context = self.get_contract_data(context, **kwargs)
        return context

    def get_contract_data(self, context, **kwargs):
        context['contracts'] = Contract.objects.raw(SQL_GET_CONTRACT_BY_USER, [self.request.user.id])
        if 'pk' in kwargs:
            try:
                context['contract'] = Contract.objects.get(pk=kwargs['pk'])
            except Exception:
                pass
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if request.method == 'POST':
            return self.post()
        return super(DetailContract, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        context = super(DetailContract, self).get_context_data(**kwargs)
        context.update(self.get_contract_data(context, **kwargs))
        context.update(get_show_all_form_data(self.request.POST, context, **kwargs))
        return render(self.request, 'contracts.html', context)


@method_decorator(login_required, name='dispatch')
class DetailItemSupplier(generic.TemplateView):
    template_name = 'supplieritems.html'

    def get_context_data(self, **kwargs):
        context = super(DetailItemSupplier, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        return context

    def get_draft_data(self, context, **kwargs):
        if 'pk' and 'ipk' in kwargs:
            #try:
            context['drafts'] = Draft.objects.raw(SQL_GET_DRAFTS_BY_USER, [self.request.user.id])
            context['suppliers'] = Supplier.objects.raw(SQL_GET_SUPPLIER_ITEM, [get_item_id(kwargs['ipk'])])
            context['item'] = kwargs['ipk']
            context['draft'] = Draft.objects.get(pk=kwargs['pk'])

            #except Exception as e:
            #    print(e)
        return context

    def dispatch(self, request, *args, **kwargs):
        insert_history(HISTORY_STRING.format(request.user.name, request.method, request.build_absolute_uri()))
        if request.method == 'POST':
            return self.post(**self.kwargs)
        return super(DetailItemSupplier, self).dispatch(request, *args, **kwargs)

    def post(self, **kwargs):
        print(kwargs)
        context = super(DetailItemSupplier, self).get_context_data(**kwargs)
        context.update(self.get_draft_data(context, **kwargs))
        context.update(get_show_all_form_data(self.request.POST, context, **kwargs))
        form = OrderForm(self.request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            select = form.cleaned_data['select']
            #try:
            if select != -400 and select > 0 and 'sid' in kwargs and 'ipk' in kwargs and 'pk' in kwargs:
                print('doing')
                print(kwargs['ipk'])
                print(get_item_id(kwargs['ipk']))
                order_write(price, kwargs['pk'], kwargs['sid'], kwargs['ipk'])
                print("redirect")
                return redirect(DRAFTS_DETAIL_REDIRECT.format(kwargs['pk']))
            #except Exception as e:
            #    print(e)
        print("end")
        return render(self.request, 'drafts.html', context)


