from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserEditForm

# Registration View (Function-Based)
def register_view(request):
    """Handles user registration and immediately logs the user in."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


# Login View (Function-Based)
def login_view(request):
    """Handles user login."""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        # AuthenticationForm requires the request object as the first argument
        form = UserLoginForm(request, data=request.POST) 
        if form.is_valid():
            # User is authenticated by the form's clean method
            user = form.get_user() 
            login(request, user)
            
            # Handle the 'Remember Me' logic here if needed, 
            # though Django's session handling often covers this.
            
            messages.success(request, f"Welcome back, {user.first_name or user.email}!")
            return redirect('profile') # Send authenticated user to their profile
        else:
            # The form error messages handle invalid email/password
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserLoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


# Profile Display View (Function-Based, protected by decorator)
@login_required
def profile_view(request):
    """Displays the authenticated user's profile page."""
    # Note: request.user is automatically available in the template context, 
    # so passing it via the context dict is redundant but harmless.
    return render(request, 'accounts/profile.html')


# Profile Edit View (Function-Based, protected by decorator)
@login_required
def profile_edit_view(request):
    """
    Allows authenticated users to edit their profile details and upload a picture.
    """
    if request.method == 'POST':
        # Pass request.FILES for image upload, and the instance of the user
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        # Populate the form with current user data
        form = UserEditForm(instance=request.user)
        
    context = {
        'form': form
    }
    return render(request, 'accounts/profile_edit.html', context)


# Logout View (Function-Based)
def logout_view(request):
    """Logs the user out and redirects to home."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')
