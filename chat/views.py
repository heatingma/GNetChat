from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, RoomForm
from .models import Profile, Room, RoomMessage
from users.models import User


@login_required
def chatroom(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    if request.method == "POST":
        roomform = RoomForm(request.POST)
        if roomform.is_valid():
            name = roomform.cleaned_data["name"]
            about_room = roomform.cleaned_data["about_room"]
            room = Room(name=name, owner_name=user.username, about_room=about_room)
            try:
                room.save()
            except:
                wrong_message = "The name of this chatroom already exists"
    return render(
        request=request, 
        template_name='chat/chatroom.html', 
        context={
            'profile': profile,
            'rooms': Room.objects.all(),
            'wrong_message': wrong_message
        }
    )
    
    
@login_required
def innerroom(request: HttpRequest, room_name):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    chat_room, created = Room.objects.get_or_create(name=room_name)
    room_messages = RoomMessage.objects.filter(room=chat_room).order_by('timestamp')
    cur_room = room_messages[0].room
    return render(
        request=request, 
        template_name='chat/innerroom.html', 
        context={
            'profile': profile,
            'cur_room': cur_room,
            'rooms': Room.objects.all(),
            'wrong_message': wrong_message,
            'room_messages': room_messages,
        }
    )
    

@login_required
def home(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/home.html', 
        context={
            'profile': profile,
        }
    )
    
       
@login_required
def groups(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/groups.html', 
        context={
            'profile': profile,
        }
    )

    
@login_required
def settings(request: HttpRequest):
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
        template_name='chat/settings.html', 
        context={
            'profile': profile,
            'profile_form': profile_form
        }
    )
    
    
@login_required
def my(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/my.html', 
        context={
            'profile': profile,
        }
    )
    
@login_required
def contracts(request: HttpRequest):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/contracts.html', 
        context={
        'rooms': Room.objects.all(),
        }
    )
    
    
