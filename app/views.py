from django.shortcuts import render, get_object_or_404, redirect
from user.models import User
from .models.wallet_models import Wallet
from .models.order_models import Order
from django.contrib.auth import login, logout, authenticate
from decimal import Decimal
from .models.wallet_models import Wallet
from .models.transaction_models import Transaction
from libs.paystack_libs.payment import checkout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
from django.views.decorators.csrf import csrf_exempt
from libs.paystack_libs.verify import verify_paystack_transaction
from rest_framework.decorators import api_view
from libs.paystack_libs.base_service import verify_debit
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.backends import CustomBackend
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index_view(request):
    return render(request, 'index.html')

def pricing_view(request):
    return render(request, "pricing.html")

def callback_view(request):
    return render(request, 'callback.html')

def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'order': orders})

def login_view(request):
    error = None
    if request.method == "POST":
        identifier = request.POST.get('email') 
        password = request.POST.get('password')
        if identifier and password:
            user = authenticate(request, username=identifier, email=identifier, password=password)
            if user is not None:
                login(request, user)
                return redirect("Dashboard")
            error = "Invalid credentials. Please try again."
    return render(request, 'login.html', {'error': error})

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create(username=username, email=email, phone_number=phone_number)
            user.set_password(password1)
            user.save()
            Wallet.objects.create(user=user)
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect("login")

def wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'wallet.html', {'transactions': transactions, 'wallet': wallet})


def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'dashboard.html', {'orders': []})

    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:4]
    return render(request, 'dashboard.html', {'orders': orders})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    try:
        amount_str = request.data.get("amount")
        if not amount_str:
            return Response({"success": False, "message": "Amount is required"}, status=400)

        try:
            amount = Decimal(amount_str)
        except InvalidOperation:
            return Response({"success": False, "message": "Invalid amount format"}, status=400)

        email = request.user.email
        initiate = checkout(email=email, amount=amount)

        if "error" in initiate:
            return Response({"success": False, "message": initiate["message"]}, status=400)
        
        wallet = get_object_or_404(Wallet, user=request.user)

        Transaction.objects.create(
            wallet=wallet,
            user=request.user,
            amount=amount,
            reference=initiate["reference"],
            type="CREDIT",
            previous_balance=wallet.balance,
            new_balance=amount
        )

        return Response({
            "success": True,
            "authorization_url": initiate["authorization_url"]
        })

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)
    
def profile_view(request):
    return render(request, 'profile.html')

@api_view(["POST"])
def call_back(request):
    reference = request.data.get("reference") or request.data.get("trxref")
    if not reference:
        return Response({"success": False, "message": "Missing payment reference."}, status=400)

    result = verify_paystack_transaction(reference=reference)
    return Response(result)




@login_required
def profile(request):
    """Profile view (read-only display)"""
    return render(request, "profile.html", {"user": request.user})


@login_required
def profile_edit(request):
    """Profile edit view (manual form handling, no Django forms)"""
    user = request.user

    if request.method == "POST":
        # Collect submitted values
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        # Basic validation
        if not username:
            messages.error(request, "Username is required.")
            return redirect("profile_edit")
        if not email:
            messages.error(request, "Email is required.")
            return redirect("profile_edit")

        # Update user fields
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")  

    return render(request, "profile_edit.html", {"user": user})

