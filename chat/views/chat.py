from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from chat.models import Profile, Friend_Request
from chat.utils import is_chinese
from users.models import User


@login_required
def chat(request: HttpRequest, dark=False):
    # judge the dark or light model    
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
    
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == "POST":
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
        template_name='chat/chat.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'friends': user.friends.all(),
            "top_friends": user.top_friends.all(),
            "new_friends": Friend_Request.objects.filter(to_user=user),
        }
    )
    