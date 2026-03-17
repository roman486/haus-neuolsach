from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
    events = Event.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')
    past_events = Event.objects.filter(start_datetime__lt=timezone.now()).order_by('-start_datetime')[:5]
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
        start_datetime = request.POST.get('start_datetime')
        end_datetime = request.POST.get('end_datetime') or None

        if title and start_datetime:
            Event.objects.create(
                title=title,
                description=description,
                location=location,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                author=request.user,
            )
            return redirect('calendar_app:home')

    return render(request, 'calendar_app/event_create.html')
