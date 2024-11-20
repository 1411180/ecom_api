from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'cardholder_name', 'expiry_date', 'cvv', 'amount']
        widgets = {
            'expiry_date': forms.TextInput(attrs={'type': 'date'}),
            'cvv': forms.PasswordInput(render_value=False, attrs={'maxlength': 3}),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError("Enter a valid 16-digit card number.")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit() or len(cvv) != 3:
            raise forms.ValidationError("Enter a valid 3-digit CVV.")
        return cvv
