from django import forms


class ShowAllForm(forms.Form):
    showall = forms.IntegerField()


class OrderForm(forms.Form):
    price = forms.IntegerField()
    select = forms.IntegerField()

class TextForm(forms.Form):
    text = forms.CharField(max_length=3000)



