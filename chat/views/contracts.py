import os
import shutil
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from chat.forms import SendInvitationForm
from chat.models import Profile, Friend_Request, FMMessage, FriendRoom, Groups, GroupMessage
from users.models import User


@login_required
def contracts(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    
    if request.method == "POST":
        send_invitation_form = SendInvitationForm(request.POST)
        
        # deal with friend_request deleting
        if "fr_uid" in request.POST:
            del_fr_uid = request.POST["fr_uid"]
            del_fr = Friend_Request.objects.get(uid=del_fr_uid)
            del_fr.delete()
        
        # deal with friend adding   
        if "hidden_acc_fr_uid" in request.POST:
            acc_fr_uid = request.POST["hidden_acc_fr_uid"]
            fr = Friend_Request.objects.get(uid=acc_fr_uid)
            user_1 = fr.from_user
            user_2 = fr.to_user
            user_1.friends.add(user_2)
            user_2.friends.add(user_1)
            groups_name = fr.groups_name
            if groups_name != "NONE":
                group = get_object_or_404(Groups, owner=fr.from_user, name=groups_name)
                group.members.add(fr.to_user)
                GroupMessage.objects.create(
                    user=fr.from_user,
                    content="Welcome {} to join us!".format(fr.to_user.username),
                    belong_group=group,
                )
            fr.delete()
            fm = FriendRoom.objects.create(user_1=user_1, user_2=user_2)

            FMMessage.objects.create(
                user=user,
                belong_fm = fm,
                content = "Hi~ we are friends now!" 
            )

        # deal with friend deleting   
        if "delete_friend_name" in request.POST:
            del_friend_name = request.POST["delete_friend_name"]
            friend = User.objects.get(username=del_friend_name)
            if friend in user.friends.all():
                user.friends.remove(friend)
            if friend in user.top_friends.all():
                user.top_friends.remove(friend)
            if user in friend.friends.all():
                friend.friends.remove(user)
            if user in friend.top_friends.all():
                friend.top_friends.remove(user)
            try:
                fm = FriendRoom.objects.get(user_1=user, user_2=friend)
                flag = True
            except:
                try:
                    fm = FriendRoom.objects.get(user_1=friend, user_2=user) 
                    flag = True 
                except:
                    flag = False
            if flag:
                fm_uid = fm.uid
                media_path = 'media/chatfriends/{}'.format(fm_uid)
                if os.path.exists(media_path):
                    shutil.rmtree(media_path)
                FriendRoom.delete(fm)
                
                               
        # deal with send invitation
        if send_invitation_form.is_valid():
            invite_email = send_invitation_form.cleaned_data["invite_email"]
            invite_message = send_invitation_form.cleaned_data["invite_message"]
            try:
                target = User.objects.get(email=invite_email)
                Friend_Request.objects.get(from_user=user, to_user=target)
                wrong_message = "The invitation have sent!"
            except:
                try:
                    target = User.objects.get(email=invite_email)
                    Friend_Request.objects.create(from_user=user, to_user=target, invite_message=invite_message)
                except:
                    wrong_message = "The user doesn't exist!"            
    
    new_friends = Friend_Request.objects.filter(to_user=user)
    have_sent = Friend_Request.objects.filter(from_user=user)
    
    return render(
        request=request, 
        template_name='chat/contracts.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'wrong_message': wrong_message,
            "new_friends": new_friends,
            "have_sent": have_sent,
            "friends": user.friends.all(),
        }
    )
