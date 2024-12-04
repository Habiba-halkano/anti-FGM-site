from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .admin import EventsAdmin
from .forms import PostForm, CommentForm, ReportForm, ContactForm
from .models import Post, Comments, Reports, Events, SupportGroups, Resources, BlogPost
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
#1. views for resources
def community_forum(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'web/forum.html', {'posts': posts})

def thank_you(request):
    return render(request, 'web/thank_you.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('community_forum')
    else:
        form = PostForm()
    return render(request, 'web/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    return render(request, 'web/post_detail.html', {'post': post, 'comments': comments})

#2. views for Comments
@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'web/add_comment.html', {'form': form, 'post': post})

# 3. views for ReportForm
@login_required
def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ReportForm()
    return render(request, 'web/submit_report.html', {'form': form})

#4. views for events
def events_view(request):
    events = Events.objects.all()
    return render(request, 'accounts/events.html', {'events': events})

#5. views for support_groups
def support_view(request):
    support_groups = SupportGroups.objects.all()
    return render(request, 'accounts/groups.html', {'support_groups': support_groups})

#6. views for Resources
def resources_view(request):
    resources = Resources.objects.all()
    return render(request, 'accounts/resources.html', {'resources': resources})

#4. VIEWS FOR EVENTS, SUPPORT GROUPS AND RESOURCES
def dashboard(request):
    events = Events.objects.all()
    support_groups = SupportGroups.objects.all()
    resources = Resources.objects.all()

    context = {'events': events, 'support_groups': support_groups, 'resources': resources}
    return render(request, 'accounts/dashboard.html', context)

#7. views for blogposts
def blog_view(request):
    blogs = BlogPost.objects.all()
    return render(request, 'accounts/blog/blogpost.html', {'blogs': blogs})

@staff_member_required()
def view_reports(request):
    reports = Reports.objects.all()
    return render(request, 'web/view_reports.html', {'reports': reports})

def home(request):
    return render(request, 'web/landing/index.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully')
            return redirect('contact')
        else:
            messages.error(request, 'please fill in the correct details')

    else:
        form = ContactForm()
    return render(request, 'accounts/contact.html', {'form': form})


