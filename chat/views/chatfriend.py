from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from chat.forms import AttachmentForm
from chat.models import Profile, Friend_Request, FMMessage, FriendRoom
from users.models import User


@login_required
def chatfriend(request: HttpRequest, friend_name, dark=False):
    # judge the dark or light model    
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    friend = get_object_or_404(User, username=friend_name)
    user = get_object_or_404(User, username=username)
    wrong_message = ""
    try:
        friend_room = FriendRoom.objects.get(user_1=user, user_2=friend)
    except:
        friend_room = get_object_or_404(FriendRoom, user_2=user, user_1=friend)
    profile = get_object_or_404(Profile, user=user)
    friend_messages = FMMessage.objects.filter(belong_fm=friend_room)
    
    
    # deal with POST action
    if request.method == "POST":
        attachmentform = AttachmentForm(request.POST, request.FILES)
        # deal with attachment
        if attachmentform.is_valid():
            attachment = attachmentform.cleaned_data["attachment"]
            content = attachmentform.cleaned_data["content"]
            rm = FMMessage.objects.create(
                user = user,
                belong_fm = friend_room,
                content = content,
                attachment = attachment
            )
            try:
                rm.save()
            except:
                wrong_message = "File size cannot exceed 5MB."
        # add top friends
        if "select_top_friends" in request.POST:
            select_top_friends = request.POST.getlist("select_top_friends")
            for friend_name in select_top_friends:
                friend = User.objects.get(username=friend_name)
                if friend not in user.top_friends.all():
                    user.top_friends.add(friend)
        # delete top friends           
        if "delete_top_friends" in request.POST:
            delete_top_friends = request.POST.getlist("delete_top_friends")
            for friend_name in delete_top_friends:
                friend = User.objects.get(username=friend_name)
                if friend in user.top_friends.all():
                    user.top_friends.remove(friend)
                
    return render(
        request=request, 
        template_name='chat/chatfriend.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'friends': user.friends.all(),
            "top_friends": user.top_friends.all(),
            "friend_room": friend_room,
            "friend":friend,
            "friend_profile": Profile.objects.get(user=friend),
            "friend_messages":friend_messages,
            "wrong_message": wrong_message,
            "new_friends": Friend_Request.objects.filter(to_user=user),
        }
    )
    
     