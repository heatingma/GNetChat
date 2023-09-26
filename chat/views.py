from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import Profile
from users.models import User

@login_required
def visit(request: HttpRequest):
    # deal with get method
    if request.method == "GET":
        username = request.user.username
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        profile_form = EditProfileForm(request.user.username)
    # deal with post method
    elif request.method == "POST":
        profile_form = EditProfileForm(request.user.username, request.POST, request.FILES)
        # check the profile form
        if profile_form.is_valid():
            about_me = profile_form.cleaned_data["about_me"]
            image = profile_form.cleaned_data["image"]
            location = profile_form.cleaned_data["location"]
            user = User.objects.get(username=request.user.username)
            profile = Profile.objects.get(user=user)
            if about_me != "":
                profile.about_me = about_me
            if image:
                profile.image = image
            if location != "":
                profile.location = location
            profile.save()
        else:
            username = request.user.username
            user = get_object_or_404(User, username=username)
            profile = get_object_or_404(Profile, user=user)
            profile_form = EditProfileForm(request.user.username)
            
    return render(
        request=request,
        template_name='chat/home.html', 
        context={
            'profile': profile,
            'profile_form': profile_form
        }
    )
