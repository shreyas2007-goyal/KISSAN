from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, FarmerRegisterForm, BuyerRegisterForm
from .models import User, AuditLog
from apps.farmers.models import FarmerProfile
from apps.buyers.models import BuyerProfile
from apps.accessibility.models import UserAccessibilityPreference

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dispatcher')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action="User Login",
                ip_address=request.META.get('REMOTE_ADDR'),
                details=f"Successful login for role {user.role}"
            )
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('dashboard:dispatcher')
        else:
            messages.error(request, "Invalid username/mobile or password. Please try again.")
    else:
        form = UserLoginForm()
    
    return render(request, 'public/login.html', {'form': form})

def register_farmer_view(request):
    if request.method == 'POST':
        form = FarmerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.FARMER
            user.set_password(form.cleaned_data['password'])
            user.save()

            FarmerProfile.objects.create(
                user=user,
                state=form.cleaned_data.get('state', 'Haryana'),
                district=form.cleaned_data.get('district', 'Karnal'),
                landholding_acres=form.cleaned_data.get('landholding_acres', 2.5),
            )
            UserAccessibilityPreference.objects.create(user=user)
            
            login(request, user)
            messages.success(request, "Farmer account registered successfully!")
            return redirect('dashboard:farmer_dashboard')
    else:
        form = FarmerRegisterForm()
    return render(request, 'public/register_farmer.html', {'form': form})

def register_buyer_view(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.BUYER
            user.set_password(form.cleaned_data['password'])
            user.save()

            BuyerProfile.objects.create(
                user=user,
                business_name=form.cleaned_data['business_name'],
                category=form.cleaned_data['category'],
                mandi_license_number=form.cleaned_data.get('mandi_license', ''),
                contact_phone=form.cleaned_data['phone_number'],
            )
            login(request, user)
            messages.success(request, "Buyer account registered successfully!")
            return redirect('dashboard:buyer_dashboard')
    else:
        form = BuyerRegisterForm()
    return render(request, 'public/register_buyer.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('public:home')

@login_required
def profile_view(request):
    return render(request, 'public/profile.html', {'user': request.user})
