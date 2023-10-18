from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from chat.forms import linkform
from chat.models import Profile, Friend_Request, LINK
from users.models import User
from chat.utils import  https_link


@login_required
def my(request: HttpRequest, dark=False):
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
        link_form = linkform(request.POST)
        
        # deal with link adding
        if link_form.is_valid():
            link_url = link_form.cleaned_data["add_link"]
            link_url = https_link(link_url)  
            link_name = link_form.cleaned_data["add_name"]
            link = LINK.objects.filter(url=link_url, user=user)
            if link:
                link = link[0]
                link:LINK
                link.name = link_name
                link.save()
            else:
                link = LINK.objects.create(url=link_url, name = link_name, user=user)
            
        # deal with link removing
        if "delete_link_url" in request.POST:
            delete_link_url = request.POST["delete_link_url"]
            link = LINK.objects.get(url=delete_link_url, user=user)
            link.delete()
            
    return render(
        request=request, 
        template_name='chat/my.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            "links": LINK.objects.filter(user=request.user),
            "new_friends": Friend_Request.objects.filter(to_user=user),
            "wrong_message": wrong_message,
        }
    )

 