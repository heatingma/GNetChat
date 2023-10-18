from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from chat.forms import EditProfileForm, PasswordChangeForm
from chat.models import Profile, Friend_Request
from users.models import User



@login_required
def settings(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    
    # deal with POST method
    if request.method == "POST":
        profile_form = EditProfileForm(request.user.username, request.POST, request.FILES)
        psw_change_form = PasswordChangeForm(request.POST)
        
        # deal with profile changing
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
        
        # deal with password changing
        if psw_change_form.is_valid():
            user = request.user
            old_password = psw_change_form.cleaned_data['old_password']
            new_password = psw_change_form.cleaned_data['new_password']
            confirm_password = psw_change_form.cleaned_data['confirm_password']

            if not user.check_password(old_password):
                wrong_message = "Wrong Password!"
            elif new_password != confirm_password:
                wrong_message = "The two password inputs are inconsistent!"
            else:
                user.set_password(new_password)
                user.save()
                # Update user's login status and maintain session
                # It is necessary to update the session authentication hash
                # update_session_auth_hash(request, user)
                log_url = reverse('users:log')
                return redirect(log_url)        
            
    return render(
        request=request,
        template_name='chat/settings.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'wrong_message': wrong_message,
            "new_friends": Friend_Request.objects.filter(to_user=user),
        }
    )
    