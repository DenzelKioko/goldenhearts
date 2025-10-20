import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DonationForm
from .models import Donation


# Context data mapping for dynamic title/icon rendering
CONTEXT_MAP = {
    'money': {'title': 'Financial Donation', 'icon': 'bi-currency-dollar'},
    'items': {'title': 'In-Kind Donation', 'icon': 'bi-box-seam'},
    'service': {'title': 'Service Donation', 'icon': 'bi-tools'},
}


def donation_form_view(request, donation_type):
    """Handles both GET (form display) and POST (form submission and saving)."""
    
    # 1. Validate the donation_type passed in the URL
    if donation_type not in CONTEXT_MAP:
        messages.error(request, "Invalid donation type specified.")
        return redirect('home')  # Redirect to a safe page

    context_data = CONTEXT_MAP[donation_type]
    is_authenticated = request.user.is_authenticated

    if request.method == 'POST':
        # Pass request.POST data to the form for processing
        form = DonationForm(request.POST)

        if form.is_valid():
            # Create the Donation instance but don't save to DB yet (commit=False)
            donation = form.save(commit=False)
            
            # --- Business Logic: Assigning Donor & Status ---
            if is_authenticated:
                # 1. Logged-in user: Assign ForeignKey, clear guest fields
                donation.donor = request.user
                donation.guest_name = None
                donation.guest_email = None
            
            # 2. Set Status and Transaction ID (Simulated for 'money')
            if donation_type == 'money':
                # NOTE: In a real app, this is where you'd call a payment gateway (Stripe/PayPal).
                # The payment gateway confirms success and returns a real transaction ID.
                donation.status = 'SUCCESS'
                donation.transaction_id = str(uuid.uuid4()) # Placeholder UUID
            else:
                donation.status = 'SUCCESS' # Items/Service are successful upon form submission

            # 3. Save the completed instance to the database
            donation.save()
            
            messages.success(request, f"Your {context_data['title']} was successfully submitted! We truly appreciate your generosity.")
            
            # PRG Pattern: Redirect to the static thank you page
            return redirect('donations:thank_you')
        
        else:
            # If the form is invalid (e.g., missing amount for 'money'), re-render with errors
            messages.error(request, "There was an issue with your submission. Please check the highlighted fields.")

    else: # GET request (initial load)
        # Populate the hidden 'donation_type' field based on the URL
        form = DonationForm(initial={'donation_type': donation_type})

    # Render the form template with all necessary context
    context = {
        'form': form,
        'donation_type': donation_type,
        'context_data': context_data,
        'is_authenticated': is_authenticated,
        'user': request.user,
    }
    return render(request, 'donations/donate_form.html', context)


def thank_you_view(request):
    """Simple view to render the final confirmation page."""
    return render(request, 'donations/thank_you.html')