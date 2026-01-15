from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Department, StudentResult, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SimpleRegisterForm
from django.contrib.auth.models import User


def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'portal/home.html', {'posts': posts})

def about_view(request):
    depts = Department.objects.all()
    return render(request, 'portal/about.html', {'departments': depts})


def register_view(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('home')
    else:
        form = SimpleRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
    

def announcements_view(request):
    posts = Post.objects.filter(post_type='NEWS').order_by('-created_at')
    return render(request, 'portal/announcements.html', {'posts': posts})

def schedules_view(request):
    posts = Post.objects.filter(post_type='SCHEDULE').order_by('-created_at')
    return render(request, 'portal/schedules.html', {'posts': posts})


def results_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        # On cherche par matricule EXACT ou PARTIEL
        results = StudentResult.objects.filter(student_id__icontains=query)
                
    return render(request, 'portal/results.html', {
        'results': results,
        'query': query
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Si l'étudiant a déjà liké, on enlève le like (Toggle)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    # On reste sur la même page après le clic
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )
    return redirect(request.META.get('HTTP_REFERER', 'home'))