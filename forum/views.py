from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Category, Thread, Post
from accounts.models import Profile


def is_approved(user):
    if user.is_staff or user.is_superuser:
        return True
    try:
        return user.profile.is_approved
    except Profile.DoesNotExist:
        return False


@login_required
def forum_home(request):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    categories = Category.objects.all()
    
    # Anzahl Threads und Posts pro Kategorie
    category_data = []
    for category in categories:
        thread_count = category.threads.count()
        post_count = sum(thread.posts.count() for thread in category.threads.all())
        category_data.append({
            'category': category,
            'thread_count': thread_count,
            'post_count': post_count,
        })  
      
    return render(request, 'forum/home.html', {'category_data': category_data})


@login_required
def thread_list(request, category_id):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    category = get_object_or_404(Category, id=category_id)
    threads = category.threads.order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'category': category, 'threads': threads})


@login_required
def thread_detail(request, thread_id):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(thread=thread, author=request.user, content=content)
            return redirect('forum:thread_detail', thread_id=thread.id)

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts})


@login_required
def thread_create(request, category_id):
    if not is_approved(request.user):
        return render(request, 'forum/not_approved.html')
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            thread = Thread.objects.create(category=category, title=title, author=request.user)
            Post.objects.create(thread=thread, author=request.user, content=content)
            return redirect('forum:thread_detail', thread_id=thread.id)

    return render(request, 'forum/thread_create.html', {'category': category})
