from django import forms


class FetchForm(forms.Form):
    select = forms.IntegerField()
    text = forms.CharField(max_length=50)


class BetweenForm(forms.Form):
    select2 = forms.IntegerField()
    datef = forms.CharField(max_length=10)
    datel = forms.CharField(max_length=10)

