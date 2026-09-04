from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Complaint


def dashboard(request):
    """Bina login ke direct website dashboard open hoga"""
    complaints = Complaint.objects.all().order_by('-id')

    # Status-wise count calculation (agar fields match karte hain)
    total_complaints = complaints.count()
    pending_complaints = complaints.filter(status__iexact='Pending').count() if hasattr(Complaint, 'status') else 0
    resolved_complaints = complaints.filter(status__iexact='Resolved').count() if hasattr(Complaint, 'status') else 0

    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
    }
    return render(request, 'dashboard.html', context)


def raise_complaint(request):
    """Nayi complaint submit karne ka view"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category', 'General')

        if title and description:
            Complaint.objects.create(
                title=title,
                description=description,
                category=category
            )
            messages.success(request, 'Complaint successfully submit ho gayi hai!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Kripya sabhi zaroori fields bharein.')

    return render(request, 'raise_complaint.html')


def complaint_detail(request, pk):
    """Specific complaint ka detail view"""
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaint_detail.html', {'complaint': complaint})


def login_view(request):
    """Agar kisi user ya admin ko manually login karna ho"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username ya password.')

    return render(request, 'login.html')


def logout_view(request):
    """Logout karke wapas open dashboard par redirect karega"""
    logout(request)
    return redirect('dashboard')