from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, FriendRequest

# 🏠 HOME VIEW
def home(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                Post.objects.create(
                    author=request.user,
                    content=content
                )
        return redirect('home')

    posts = Post.objects.all().order_by('-created_at')

    # 🔥 ADD THIS LINE (Step 6)
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(
            receiver=request.user,
            accepted=False
        )
    else:
        requests = []

    return render(request, 'home.html', {
        'posts': posts,
        'requests': requests   # 🔥 PASS TO HTML
    })

# 🔐 SIGNUP
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ❤️ LIKE POST
def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')


# 💬 ADD COMMENT
def add_comment(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        post = get_object_or_404(Post, id=post_id)

        if text:
            Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )

    return redirect('home')


# 👤 PROFILE VIEW
def profile(request, username):
    from django.contrib.auth.models import User
    from .models import Profile, Post

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts
    })
from .models import FriendRequest

def send_request(request, username):
    receiver = User.objects.get(username=username)
    
    if request.user != receiver:
        FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )
    return redirect('profile', username=username)


def accept_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    
    if friend_request.receiver == request.user:
        friend_request.accepted = True
        friend_request.save()

    return redirect('home')
from .models import Message, FriendRequest

def chat(request, username):
    other_user = User.objects.get(username=username)

    # 🔒 Check if they are friends
    is_friend = FriendRequest.objects.filter(
        sender=other_user,
        receiver=request.user,
        accepted=True
    ) | FriendRequest.objects.filter(
        sender=request.user,
        receiver=other_user,
        accepted=True
    )

    if not is_friend.exists():
        return redirect('home')

    # Send message
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )
        return redirect('chat', username=username)

    # Get messages
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages
    })