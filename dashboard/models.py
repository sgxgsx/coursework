from django.db import models
from accounts.models import MyUser

# Create your models here.


def check_if_manager(user):
    if user:
        return user.id in (MyUser.objects.filter(status='Manager')).values_list('id', flat=True)
    return False


class WorkBoard(models.Model):
    userId = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    hoursamount = models.IntegerField(null=False, blank=False, default=0)


class Contract(models.Model):
    title = models.TextField(max_length=50, blank=False, null=False)
    content = models.TextField(max_length=1000, blank=False, null=False)
    needed = models.TextField(max_length=1000, blank=False, null=False)
    taken = models.BooleanField(null=False, blank=False, default=False)
    done = models.BooleanField(null=False, blank=False, default=False)
    budget = models.IntegerField(null=False, blank=False)
    userId = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)


class Payment(models.Model):
    date = models.DateField(null=False, blank=False)
    amount = models.IntegerField(blank=False, null=False)
    contractId = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Client(models.Model):
    name = models.TextField(max_length=50, blank=False, null=False)
    phone = models.TextField(max_length=10, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    contractss = models.ManyToManyField(Contract)


class Draft(models.Model):
    text = models.TextField(max_length=2000, blank=True, null=False)
    title = models.TextField(max_length=200, blank=True, null=False)
    done = models.BooleanField(default=False, null=False, blank=False)
    already_paid = models.BooleanField(default=False, null=False, blank=False)
    contractId = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Supplier(models.Model):
    name = models.TextField(max_length=50, blank=False, null=False)
    phone = models.TextField(max_length=10, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    company_name = models.TextField(max_length=50, blank=False, null=False)
    #type = models.TextField(max_length=50, blank=True, null=True)


class Item(models.Model):
    type = models.TextField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=200, blank=True, null=False)
    quantity = models.IntegerField(blank=False, default=0, null=False)


class ItemSupplier(models.Model):
    price = models.IntegerField(null=False, blank=False)
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=False, blank=False, on_delete=models.CASCADE)


class DraftItem(models.Model):
    amount_needed = models.IntegerField(blank=False, null=False)
    price = models.FloatField(null=True, default=None)
    satisfied = models.BooleanField(default=False, null=False)
    itemId = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    draftId = models.ForeignKey(Draft, on_delete=models.CASCADE, null=False)
    supplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, default=None)


class History(models.Model):
    time = models.FloatField(null=False)
    message = models.TextField(null=False)