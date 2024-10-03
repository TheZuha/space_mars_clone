from django import forms
from .models import Shops

PAYMENT_CHOICES = [
    ('cash', 'Naqd'),
    ('card', 'Karta orqali'),
]

DELIVERY_CHOICES = [
    ('delivery', 'Yetkazib berish'),
    ('pickup', 'Borib olish'),
]

class OrderForm(forms.Form):
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    shops = forms.ModelChoiceField(queryset=Shops.objects.all(), required=False)

    # These fields will only be shown when payment method is 'card'
    card_number = forms.CharField(max_length=16, required=False)
    card_expiry_date = forms.CharField(max_length=5, required=False)  # Format: MM/YY

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')

        # If delivery method is 'pickup', 'shops' must be selected
        if delivery_method == 'pickup' and not cleaned_data.get('shops'):
            self.add_error('shops', 'Do\'kon tanlang.')

        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'card':
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Karta raqamini kiriting.')
            if not cleaned_data.get('card_expiry_date'):
                self.add_error('card_expiry_date', 'Karta amal qilish sanasini kiriting.')
        return cleaned_data
