from django import template
from ..models import Contract, Draft, Supplier


register = template.Library()


@register.inclusion_tag('gen_contracts.html')
def get_contracts():
    contracts = Contract.objects.all()
    return {'contracts': contracts[:10]}


@register.inclusion_tag('gen_drafts.html')
def get_drafts():
    drafts = Draft.objects.all()
    return {'drafts': drafts}


@register.inclusion_tag('gen_suppliers.html')
def get_suppliers():
    supplier = Supplier.objects.all()
    return {'suppliers': supplier}



