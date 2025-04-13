from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from retail_store.models import CustomUser, CashierLoginID, Business
from retail_store.forms import CustomUserCreationForm, UserUpdateForm, BusinessRegistrationForm, UserUpdateForm
from django.contrib import messages


# register business
def register_business(request):
    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Business registered successfully. Please log in.")
            return redirect("staff:business_login")
        else:
            messages.error(request, "Registration failed. Please check your input.")
    else:
        form = BusinessRegistrationForm()
    
    return render(request, "main/register_business.html", {"form": form})


# login_business
def business_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Authenticate user
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            request.session["business_id"] = user.business.id  # Store business ID
            return redirect("staff:user_selector")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "main/business_login.html")


# User_selector
def user_selector(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        if user_type == "cashier":
            return redirect("cashier_login")
        elif user_type == "manager":
            return redirect("user_login")
    return render(request, "main/user_selector.html")


# user login
@login_required
def user_dashboard(request):
    return redirect_dashboard(request.user)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            
            return redirect_dashboard(user)
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, "main/login.html")

# @login_required
# def update_credentials(request):
#     if request.method == "POST":
#         form = UserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             request.user.username = form.cleaned_data['new_username']
#             request.user.set_password(form.cleaned_data['new_password'])
#             # request.user.is_first_login = False
#             request.user.save()
#             messages.success(request, "Credentials updated. Please log in again.")
#             return redirect('user_login')
#     else:
#         form = UserUpdateForm()
    
#     return render(request, "main/update_credentials.html", {"form": form})

def redirect_dashboard(user):
    if user.role == "manager":
        return redirect("manager_dashboard")
    elif user.role == "inventory_manager":
        return redirect("inventory_dashboard")
    elif user.role == "cashier":
        return redirect("cashier_dashboard")

@login_required
def generate_cashier_login(request):
    if request.user.role != "manager":
        messages.error(request, "Only the manager can generate cashier logins.")
        return redirect("manager_dashboard")

    cashier_id = get_random_string(6).upper()
    CashierLoginID.objects.create(id=cashier_id)
    messages.success(request, f"Generated cashier login ID: {cashier_id}")
    
    return redirect("manager_dashboard")

def cashier_login(request):
    if request.method == "POST":
        cashier_id = request.POST["cashier_id"]
        login_entry = CashierLoginID.objects.filter(id=cashier_id, is_used=False).first()

        if login_entry and not login_entry.is_expired():
            user, created = CustomUser.objects.get_or_create(username=cashier_id, role="cashier")
            auth_login(request, user)
            login_entry.is_used = True
            login_entry.user = user
            login_entry.save()
            return redirect("cashier_dashboard")
        else:
            messages.error(request, "Invalid or expired cashier login ID.")
    
    return render(request, "main/cashier_login.html")
