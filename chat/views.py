from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import Profile
from users.models import User

@login_required
def visit(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    # form = EditProfileForm(request.user.username, request.POST, request.FILES)
    print("profile:", profile.image_url)
    
    return render(
        request=request,
        template_name='chat/home.html', 
        context={
            'profile': profile
        }
    )
    


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user.username,request.POST, request.FILES)
        if form.is_valid():
            about_me = form.cleaned_data["about_me"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about_me = about_me
            if image:
                profile.image = image
            profile.save()
            return redirect("users:profile", username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, "users/edit_profile.html", {'form': form})