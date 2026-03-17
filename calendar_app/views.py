from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Event, RSVP
from accounts.models import Profile


def is_approved(user):
    if user.is_staff or user.is_superuser:
        return True
    try:
        return user.profile.is_approved
    except Profile.DoesNotExist:
        return False


@login_required
def calendar_home(request):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    events = Event.objects.filter(start_date__gte=date.today()).order_by('start_date')
    past_events = Event.objects.filter(start_date__lt=date.today()).order_by('-start_date')[:5]
    return render(request, 'calendar_app/home.html', {
        'events': events,
        'past_events': past_events,
    })


@login_required
def event_detail(request, event_id):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    event = get_object_or_404(Event, id=event_id)
    rsvps = event.rsvps.select_related('user')
    user_rsvp = rsvps.filter(user=request.user).first()

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['yes', 'no', 'maybe']:
            RSVP.objects.update_or_create(
                event=event,
                user=request.user,
                defaults={'status': status}
            )
            return redirect('calendar_app:event_detail', event_id=event.id)

    return render(request, 'calendar_app/event_detail.html', {
        'event': event,
        'rsvps': rsvps,
        'user_rsvp': user_rsvp,
    })


@login_required
def event_create(request):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') or None

        if title and start_date:
            Event.objects.create(
                title=title,
                description=description,
                location=location,
                start_date=start_date,
                end_date=end_date,
                author=request.user,
            )
            return redirect('calendar_app:home')

    return render(request, 'calendar_app/event_create.html')
