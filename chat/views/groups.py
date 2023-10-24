import os
import shutil
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from chat.models import Profile, Friend_Request, Groups
from users.models import User
from chat.forms import GroupForm, ConfirmDeleteGroupForm
from chat.utils import is_chinese,chinese_to_pinyin


@login_required
def groups(request: HttpRequest, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    wrong_message = ""
    
    if request.method == "POST":
        print(request.POST)
        groupform = GroupForm(request.POST, request.FILES)
        confirm_delete_group_form = ConfirmDeleteGroupForm(request.POST)
        # deal with creating a new Groups
        if groupform.is_valid():
            show_name = groupform.cleaned_data["group_name"]
            group_name = show_name
            about_group = groupform.cleaned_data["about_group"]
            image = groupform.cleaned_data["image"]
            selected_friends = request.POST.getlist('select_friends')
            if is_chinese(group_name):
                group_name=chinese_to_pinyin(group_name)
            group_name: str
            group_name.replace(' ', '_')
            if Groups.objects.filter(owner=user, name=group_name):
                wrong_message = "You have already created a group chat with the same name"
            else:
                if selected_friends:
                    new_group = Groups(name=group_name, show_name=show_name, about_group=about_group, owner=user)
                    if image:
                        new_group.image = image
                    new_group.save()
                    for friend in selected_friends:
                        friend = get_object_or_404(User, username=friend)
                        new_group.members.add(friend)
                    new_group.members.add(user)
                else:
                    wrong_message = "Group chat requires at least 2 people"
        
        if "exit_group_uid" in request.POST:
            exit_group_uid = request.POST["exit_group_uid"]
            group = get_object_or_404(Groups, uid=exit_group_uid)
            group.members.remove(user)
            
        # deal with the group-deleting
        if confirm_delete_group_form.is_valid():
            hidden_group_name = confirm_delete_group_form.cleaned_data["hidden_group_name"]
            hidden_user_name = confirm_delete_group_form.cleaned_data["hidden_user_name"]
            confirm_group_name = confirm_delete_group_form.cleaned_data["confirm_group_name"]
            confirm_user_name = confirm_delete_group_form.cleaned_data["confirm_user_name"]
            hidden_group_name = hidden_group_name.replace(' ', '_')
            confirm_group_name = confirm_group_name.replace(' ', '_')
            owner = User.objects.filter(username=confirm_user_name)[0] 
            # check
            if hidden_group_name != confirm_group_name:
                wrong_message = "Incorrect confirmation information."
            elif hidden_user_name != confirm_user_name:
                wrong_message = "Incorrect confirmation information."
            elif owner != user:
                wrong_message = "Incorrect confirmation information."
            else:
                del_group = Groups.objects.get(owner=user, name=confirm_group_name)
                media_path = 'media/groups/{}'.format(del_group.uid)
                if os.path.exists(media_path):
                    shutil.rmtree(media_path)
                del_group.delete()
   
    all_groups = Groups.objects.all()
    own_groups = Groups.objects.filter(owner=user)
    in_groups = list()
    for group in all_groups:
        group: Groups
        if group.exist(user):
            in_groups.append(group)
            
    return render(
        request=request, 
        template_name='chat/groups.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'friends': user.friends.all(),
            "new_friends": Friend_Request.objects.filter(to_user=user),
            "wrong_message": wrong_message,
            'own_groups': own_groups,
            'in_groups': in_groups,
        }
    )

    