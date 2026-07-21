from django import forms
from django.utils import timezone
from .models import Transaction


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].choices = [
            ('', 'Select Transaction Type')
        ] + list(Transaction.TYPE_CHOICES)

        self.fields['category'].choices = [
            ('', 'Select Category')
        ] + list(Transaction.CATEGORY_CHOICES)

    class Meta:
        model = Transaction

        fields = [
            'transaction_type',
            'category',
            'amount',
            'date',
            'description'
        ]

        widgets = {

            'transaction_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter amount'
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional description'
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError("Amount is required.")

        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

        return amount

    def clean_date(self):

        date = self.cleaned_data.get('date')

        if date and date > timezone.now().date():
            raise forms.ValidationError("Future dates are not allowed.")

        return date