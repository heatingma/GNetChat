from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, RoomForm, PostForm
from .models import Profile, Room, RoomMessage, Post
from users.models import User
import json

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
            'wrong_message': wrong_message,
        }
    )
    
    
@login_required
def innerroom(request: HttpRequest, room_name, post_name):
    # user info
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # get objects 
    chat_room = get_object_or_404(Room, name=room_name)
    room_messages = RoomMessage.objects.filter(room=chat_room).order_by('timestamp')
    wrong_message = ""
    
    # deal with post action
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            title = postform.cleaned_data["title"]
            about_post = postform.cleaned_data["about_post"]
            image = postform.cleaned_data["image"]
            post = Post(title=title, author=user, about_post=about_post, image=image, belong_room=chat_room)
            try:
                post.save()
            except:
                wrong_message = "A post with the same title already exists in this room."

    # get current room and current post
    cur_room = room_messages[0].room
    if post_name == "chatting_" + room_name:
        chatting_post = True
    else:
        chatting_post = False
    cur_post = get_object_or_404(Post, title=post_name, belong_room=cur_room)
    
    # get users' img_urls
    users_img_urls = dict()
    for rm in room_messages:
        user = rm.user
        user_profile = get_object_or_404(Profile, user=user)
        users_img_urls[user_profile.user.username] = user_profile.image_url
    
    # return the tpl
    return render(
        request=request, 
        template_name='chat/innerroom.html', 
        context={
            'profile': profile,
            'rooms': Room.objects.all(),
            'cur_room': cur_room,
            'wrong_message': wrong_message,
            'room_messages': room_messages,
            'cur_post': cur_post,
            'chatting_post': chatting_post,
            'users_img_urls_json': json.dumps(users_img_urls)
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
    
    
