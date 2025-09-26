from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile, Message
from .forms import ProfileForm, SignUpForm
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            Profile.objects.create(user=user)  # auto profile
            login(request, user)
            return redirect("profile")  # go to profile
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('matches')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("matches")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})


@login_required
def matches(request):
    # Ensure the logged-in user always has a Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    all_matches = Profile.objects.exclude(user=request.user)

    suggested_matches = []
    for match in all_matches:
        # gender preference
        if profile.pref_gender and profile.pref_gender != "Anyone" and match.gender != profile.pref_gender:
            continue
        # hobbies intersection
        if set(profile.hobbies_list) & set(match.hobbies_list):
            suggested_matches.append(match)

    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

    return render(request, "matches.html", {
        "suggested_matches": suggested_matches,
        "all_matches": all_matches,
        "unread_count": unread_count,
    })


@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    for u in users:
        u.unread_count = Message.objects.filter(sender=u, receiver=request.user, is_read=False).count()
    return render(request, 'chat_list.html', {'users': users})


@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat', user_id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    return render(request, 'chat.html', {
        'roommate': other_user,
        'messages': messages
    })


@login_required
def delete_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        request.user.delete()
        return redirect("home")
    return render(request, "delete_profile.html", {"profile": profile})
