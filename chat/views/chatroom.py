import os
import shutil
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from chat.forms import RoomForm, ChangeRoomForm, ConfirmDeleteChatroomForm
from chat.models import Profile, Room, Post, Friend_Request
from chat.utils import is_chinese
from users.models import User


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
            if not is_chinese(name):
                name: str
                name = name.replace(' ', '_')
                about_room = roomform.cleaned_data["about_room"]
                image = roomform.cleaned_data["image"]
                room = Room(name=name, owner_name=user.username, about_room=about_room)
                if image:
                    room.image = image
                try:
                    room.save()
                except:
                    wrong_message = "The name of this chatroom already exists"
            else:
                wrong_message = "Input of Chinese names is currently not supported"
                
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
                    ori_media_path = 'media/chatrooms/{}'.format(ori_name)
                    new_media_path = 'media/chatrooms/{}'.format(new_name)
                    if os.path.exists(ori_media_path):
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
            hidden_chatroom_name = hidden_chatroom_name.replace(' ', '_')
            confirm_chatroom_name = confirm_chatroom_name.replace(' ', '_') 
            # check
            if hidden_chatroom_name != confirm_chatroom_name:
                wrong_message = "Incorrect confirmation information."
            elif hidden_user_name != confirm_user_name:
                wrong_message = "Incorrect confirmation information."
            else:
                chat_room = Room.objects.get(name=confirm_chatroom_name)
                if confirm_user_name == chat_room.owner_name:
                    chat_room.delete()
                    media_path = 'media/chatrooms/{}'.format(confirm_chatroom_name)
                    if os.path.exists(media_path):
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
            "new_friends": Friend_Request.objects.filter(to_user=user)
        }
    )
    
    