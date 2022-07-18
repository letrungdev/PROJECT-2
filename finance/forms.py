from . models import Transaction
from django import forms


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'tran_time', 'category', 'note', 'tran_image')
