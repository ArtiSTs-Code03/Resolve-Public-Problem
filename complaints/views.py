from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Complaint, Category

# User Dashboard (Protected)
def dashboard(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    category_filter = request.GET.get('category', '').strip()

    complaints = Complaint.objects.filter(user=request.user)

    if search_query:
        complaints = complaints.filter(
            Q(ticket_id__icontains=search_query) | 
            Q(title__icontains=search_query) |
            Q(complainant_name__icontains=search_query)
        )

    if status_filter:
        complaints = complaints.filter(status=status_filter)

    if category_filter:
        complaints = complaints.filter(category_id=category_filter)

    complaints = complaints.order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'complaints': complaints,
        'categories': categories,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
    }
    return render(request, 'complaints/dashboard.html', context)

# Raise Complaint Form (Protected)
def raise_complaint(request):
    if request.method == 'POST':
        name = request.POST.get('complainant_name')
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        category = get_object_or_404(Category, id=category_id)
        Complaint.objects.create(
            user=request.user,
            complainant_name=name,
            category=category,
            title=title,
            description=description,
            image=image
        )
        messages.success(request, "Your issue has been reported successfully!")
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'complaints/raise_complaint.html', {'categories': categories})

# User Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'complaints/login.html', {'form': form})

# User Registration View
def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'complaints/register.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')