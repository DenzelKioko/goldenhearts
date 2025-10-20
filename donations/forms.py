from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    # Field to temporarily hold the payment token (optional, for future integration)
    payment_token = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Donation
        fields = [
            'program', 
            'donation_type', 
            'amount', 
            'description', 
            'guest_name', 
            'guest_email'
        ]
        widgets = {
            'donation_type': forms.HiddenInput(), # Set dynamically in the view/template
            'description': forms.Textarea(attrs={'rows': 4}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount (e.g., 50.00)'}),
        }

    def __init__(self, *args, **kwargs):
        # Remove fields that should not be displayed by default, as we handle conditional visibility
        super().__init__(*args, **kwargs)
        
        # Style all visible fields with Bootstrap classes
        for field_name in self.fields:
            if field_name not in ['donation_type', 'payment_token']:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
                self.fields[field_name].required = False # Start as optional, enforce in clean()

        # Set labels
        self.fields['guest_name'].label = "Your Name"
        self.fields['guest_email'].label = "Email for Receipt"

    def clean(self):
        cleaned_data = super().clean()
        donation_type = cleaned_data.get('donation_type')
        amount = cleaned_data.get('amount')
        description = cleaned_data.get('description')
        guest_email = cleaned_data.get('guest_email')

        # 1. Enforce data based on donation type
        if donation_type == 'money':
            if not amount:
                self.add_error('amount', "Please enter a donation amount.")
        elif donation_type in ['items', 'service']:
            if not description:
                self.add_error('description', f"Please describe the {donation_type} you wish to donate.")
        
        # 2. Require guest email if the donor is anonymous (instance is None or user is not set)
        if not self.instance or not self.instance.donor_id:
            if not guest_email:
                self.add_error('guest_email', "Please provide an email for us to send a receipt or confirmation.")
        
        return cleaned_data
