from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "agent":
                return redirect("agent_dashboard")
            else:
                return redirect("ticket_list")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

@login_required
def create_agent(request):
    if request.user.role != "admin":
        messages.error(request, "Unauthorized access")
        return redirect("ticket_list")  # fallback

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            messages.error(request, "All fields are required")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password, role="agent")
            messages.success(request, f"Agent {username} created successfully!")
            return redirect("admin_dashboard")

    return render(request, "admin/create_agent.html")