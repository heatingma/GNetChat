from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, RoomForm, PostForm, AttachmentForm, \
    ChangeRoomForm, ConfirmDeletePostForm, ConfirmDeleteChatroomForm
from .models import Profile, Room, RoomMessage, Post
from users.models import User
import json
import os
import shutil


@login_required
def chatroom(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    if request.method == "POST":
        roomform = RoomForm(request.POST, request.FILES)
        changeroomform = ChangeRoomForm(request.POST, request.FILES)
        confirm_delete_chatroom_form = ConfirmDeleteChatroomForm(request.POST)
        
        # create a new chatroom
        if roomform.is_valid():
            name = roomform.cleaned_data["name"]
            about_room = roomform.cleaned_data["about_room"]
            image = roomform.cleaned_data["image"]
            room = Room(name=name, owner_name=user.username, about_room=about_room)
            if image:
                room.image = image
            try:
                room.save()
            except:
                wrong_message = "The name of this chatroom already exists"
                
        # edit an exited chatroom
        if changeroomform.is_valid():
            ori_name = changeroomform.cleaned_data["chatroom_ori_name"]
            owner = changeroomform.cleaned_data["chatroom_owner"]
            new_name = changeroomform.cleaned_data["chatroom_name"]
            new_about = changeroomform.cleaned_data["chatroom_about"]
            new_image = changeroomform.cleaned_data["chatroom_image"]
            if owner != user.username:
                wrong_message = "You are not authorized to perform this operation!"
            else:
                name_flag = False
                chat_room = Room.objects.get(name=ori_name)
                if new_name != "":
                    name_flag = True
                    chat_room.name = new_name
                if new_about != "":
                    chat_room.about_room = new_about
                if new_image:
                    chat_room.image = new_image
                chat_room.save()
                if name_flag:
                    # rename the media path 
                    ori_media_path = 'media/room_files/{}'.format(ori_name)
                    new_media_path = 'media/room_files/{}'.format(new_name)
                    os.rename(ori_media_path, new_media_path)
                    # update all the default chatting post name
                    target_post = Post.objects.get(title="chatting_"+ori_name, belong_room=chat_room)
                    target_post.title = "chatting_"+new_name
                    target_post.save()
                    
        # deal with the chatroom-deleting
        if confirm_delete_chatroom_form.is_valid():
            hidden_chatroom_name = confirm_delete_chatroom_form.cleaned_data["hidden_chatroom_name"]
            hidden_user_name = confirm_delete_chatroom_form.cleaned_data["hidden_user_name"]
            confirm_chatroom_name = confirm_delete_chatroom_form.cleaned_data["confirm_chatroom_name"]
            confirm_user_name = confirm_delete_chatroom_form.cleaned_data["confirm_user_name"] 
            # check
            if hidden_chatroom_name != confirm_chatroom_name:
                wrong_message = "Incorrect confirmation information."
            elif hidden_user_name != confirm_user_name:
                wrong_message = "Incorrect confirmation information."
            else:
                chat_room = Room.objects.get(name=confirm_chatroom_name)
                if confirm_user_name == chat_room.owner_name:
                    chat_room.delete()
                    media_path = 'media/room_files/{}'.format(confirm_chatroom_name)
                    shutil.rmtree(media_path)
                else:
                    wrong_message = "Incorrect confirmation information."
                    
                                  
    return render(
        request=request, 
        template_name='chat/chatroom.html', 
        context={
            'profile': profile,
            'rooms': Room.objects.all(),
            'wrong_message': wrong_message,
            'dark': dark,
            'light': not dark,
        }
    )
    
    
@login_required
def innerroom(request: HttpRequest, room_name, post_name, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
    # user info
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # get objects (current room and current post)
    chat_room = get_object_or_404(Room, name=room_name)
    if post_name == "chatting_" + room_name:
        chatting_post = True
    else:
        chatting_post = False
    cur_post = get_object_or_404(Post, title=post_name, belong_room=chat_room)
    room_messages = RoomMessage.objects.filter(room=chat_room, belong_post=cur_post).order_by('timestamp')
    posts = Post.objects.filter(belong_room=chat_room).order_by('created_on')
    wrong_message = ""
    
    # deal with POST action
    if request.method == "POST":
        postform = PostForm(request.POST, request.FILES)
        attachmentform = AttachmentForm(request.POST, request.FILES)
        confirm_delete_post_form = ConfirmDeletePostForm(request.POST)
        # deal with creating a new post
        if postform.is_valid():
            title = postform.cleaned_data["title"]
            about_post = postform.cleaned_data["about_post"]
            image = postform.cleaned_data["image"]
            post = Post(
                title=title, 
                author=user, 
                author_profile =profile,
                about_post=about_post, 
                belong_room=chat_room
            )
            if image:
                post.image = image
            if Post.objects.filter(title=post.title, belong_room=post.belong_room).exists():
                wrong_message = "A post with the same title already exists in this room."
            else:
                post.save()     
        # deal with attachment
        if attachmentform.is_valid():
            attachment = attachmentform.cleaned_data["attachment"]
            content = attachmentform.cleaned_data["content"]
            rm = RoomMessage(
                user = user,
                room = chat_room,
                belong_post = cur_post,
                content = content,
                attachment = attachment
            )
            try:
                rm.save()
            except:
                wrong_message = "File size cannot exceed 5MB."
        # deal with post-deleting
        if confirm_delete_post_form.is_valid():
            hidden_post_name = confirm_delete_post_form.cleaned_data["hidden_post_name"]
            hidden_user_name = confirm_delete_post_form.cleaned_data["hidden_user_name"]
            confirm_post_name = confirm_delete_post_form.cleaned_data["confirm_post_name"]
            confirm_user_name = confirm_delete_post_form.cleaned_data["confirm_user_name"] 
            # check
            if hidden_post_name != confirm_post_name:
                wrong_message = "Incorrect confirmation information."
            elif hidden_user_name != confirm_user_name:
                wrong_message = "Incorrect confirmation information."
            else:
                if confirm_user_name == cur_post.author.username or confirm_user_name == chat_room.owner_name:
                    dl_post = Post.objects.get(title=confirm_post_name, belong_room=chat_room)
                    dl_post.delete()
                    post_name = "chatting_" + room_name
                    chatting_post = True
                    cur_post = get_object_or_404(Post, title=post_name, belong_room=chat_room)
                else:
                    wrong_message = "Incorrect confirmation information."
            
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
            'cur_room': chat_room,
            'wrong_message': wrong_message,
            'room_messages': room_messages,
            'posts': posts,
            'cur_post': cur_post,
            'chatting_post': chatting_post,
            'users_img_urls_json': json.dumps(users_img_urls),
            'dark': dark,
            'light': not dark,
        }
    )
    

@login_required
def chat(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/chat.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
        }
    )
    
       
@login_required
def groups(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/groups.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
        }
    )

    
@login_required
def settings(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
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
            'profile_form': profile_form,
            'dark': dark,
            'light': not dark,
        }
    )
    
    
@login_required
def my(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True

    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/my.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
        }
    )
    
@login_required
def contracts(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request=request, 
        template_name='chat/contracts.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
        }
    )
    
    
