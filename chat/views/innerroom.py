import os
import shutil
import json
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from chat.forms import PostForm, AttachmentForm, ConfirmDeletePostForm, EditPostForm
from chat.models import Profile, Room, Post, Friend_Request, RoomMessage, Tag
from chat.utils import is_chinese,chinese_to_pinyin
from users.models import User


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
        editpostform = EditPostForm(request.POST, request.FILES)
        
        # deal with creating a new post
        if postform.is_valid():
            show_name = postform.cleaned_data["title"]
            title = show_name
            if is_chinese(title):
                title = chinese_to_pinyin(title)
            title: str
            title.replace(' ', '_')
            about_post = postform.cleaned_data["about_post"]
            image = postform.cleaned_data["image"]
            new_tag = postform.cleaned_data["new_tag"]
            selected_tag = request.POST.getlist('select_tags')
            all_tags = list()
            if selected_tag:
                for tag in selected_tag:
                    all_tags.append(tag)
            if new_tag:
                all_tags.append(new_tag) 
            post = Post(
                title=title, 
                show_name=show_name,
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
                if all_tags:
                    for tag in all_tags:
                        try:
                            cur_tag = Tag.objects.get(name=tag)
                        except:
                            cur_tag = Tag.objects.create(name=tag)
                        post.tags.add(cur_tag)
                
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
            hidden_post_name: str
            confirm_post_name: str  
            hidden_post_name = hidden_post_name.replace(' ', '_')
            confirm_post_name = confirm_post_name.replace(' ', '_')
            
            if is_chinese(hidden_post_name):
                hidden_post_name = chinese_to_pinyin(hidden_post_name)
            if is_chinese(confirm_post_name):
                confirm_post_name = chinese_to_pinyin(confirm_post_name)
            
            # check
            if hidden_post_name != confirm_post_name:
                wrong_message = "Incorrect confirmation information."
            elif hidden_user_name != confirm_user_name:
                wrong_message = "Incorrect confirmation information."
            elif confirm_post_name.startswith('chatting_'):
                wrong_message = "cannot delete the default chatting post."
            else:
                if confirm_user_name == cur_post.author.username or confirm_user_name == chat_room.owner_name:
                    dl_post = Post.objects.get(title=confirm_post_name, belong_room=chat_room)
                    dl_post.delete()
                    media_path = 'media/chatrooms/{}/posts/{}'.format(dl_post.belong_room.name, dl_post.title)
                    if os.path.exists(media_path):
                        shutil.rmtree(media_path)
                    post_name = "chatting_" + room_name
                    chatting_post = True
                    cur_post = get_object_or_404(Post, title=post_name, belong_room=chat_room)
                else:
                    wrong_message = "Incorrect confirmation information."
        
        # deal with post-editing
        if editpostform.is_valid():
            change_about_post = editpostform.cleaned_data["change_about_post"]
            upload_image = editpostform.cleaned_data["upload_image"]
            delete_tag = editpostform.cleaned_data["delete_tag"]
            add_tag = editpostform.cleaned_data["add_tag"]
            if change_about_post != "":
                cur_post.about_post = change_about_post
            if upload_image:
                cur_post.image = upload_image
            if delete_tag != "":
                try:
                    del_tag = Tag.objects.get(name=delete_tag)
                    cur_post.tags.delete(del_tag)
                except:
                    pass
            if add_tag != "":
                try:
                    addtag = Tag.objects.get(name=add_tag)
                except:
                    addtag = Tag.objects.create(name=add_tag)
                cur_post.tags.add(addtag)
            cur_post.save()

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
            'tags': Tag.objects.all(),
            "new_friends": Friend_Request.objects.filter(to_user=user),
        }
    )
    