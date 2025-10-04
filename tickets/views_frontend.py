from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
from comments.models import Comment
from accounts.models import User

@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("ticket-list")
    tickets = Ticket.objects.all().order_by("-created_at")
    agents = User.objects.filter(role="agent")
    return render(request, "admin/dashboard.html", {"tickets": tickets, "agents": agents})

@login_required
def assign_ticket(request, ticket_id):
    if request.user.role != "admin":
        return redirect("ticket-list")
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        agent_id = request.POST.get("agent")
        ticket.assigned_to_id = agent_id
        ticket.save()
        return redirect("admin_dashboard")
    agents = User.objects.filter(role="agent")
    return render(request, "admin/ticket_assign.html", {"ticket": ticket, "agents": agents})


@login_required
def agent_dashboard(request):
    if request.user.role != "agent":
        return redirect("ticket-list")
    tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, "agent/dashboard.html", {"tickets": tickets})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = Comment.objects.filter(ticket=ticket).order_by('created_at')

    if request.method == 'POST' and 'text' in request.POST:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(ticket=ticket, user=request.user, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect('ticket_detail', pk=ticket.pk)

    if request.method == 'POST' and 'status' in request.POST:
        if request.user.role == 'agent' and ticket.assigned_to == request.user:
            status_value = request.POST.get('status')
            if status_value in dict(Ticket.STATUS_CHOICES):
                ticket.status = status_value
                ticket.save()
                messages.success(request, 'Ticket status updated successfully!')
                return redirect('ticket_detail', pk=ticket.pk)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments
    })


@login_required
def ticket_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Ticket.objects.create(title=title, description=description, created_by=request.user)
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_list')

    return render(request, 'tickets/ticket_form.html')
