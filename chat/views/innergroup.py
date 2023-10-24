import os
import shutil
import json
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from chat.forms import GroupForm, EditGroupForm
from chat.models import Profile, Friend_Request, Groups, GroupMessage
from chat.utils import is_chinese
from users.models import User


@login_required
def innergroup(request: HttpRequest, group_uid, dark=False):
    # judge the dark or light model
    if request.GET:
        dark = request.GET['dark']
        dark = False if dark == 'False' else True
        
    # user info
    username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # group info
    cur_group = get_object_or_404(Groups, uid=group_uid)
    group_messages = GroupMessage.objects.filter(belong_group=cur_group).order_by('timestamp')
    wrong_message = ""
    
    # deal with POST action
    if request.method == "POST":
        groupform = GroupForm(request.POST, request.FILES)
        editgroupform = EditGroupForm(request.POST, request.FILES)
        
        # deal with creating a new Groups
        if groupform.is_valid():
            group_name = groupform.cleaned_data["group_name"]
            about_group = groupform.cleaned_data["about_group"]
            image = groupform.cleaned_data["image"]
            selected_friends = request.POST.getlist('select_friends')
            if not is_chinese(group_name):
                group_name: str
                group_name.replace(' ', '_')
                if Groups.objects.filter(owner=user, name=group_name):
                    wrong_message = "You have already created a group chat with the same name"
                else:
                    if selected_friends:
                        new_group = Groups(name=group_name, about_group=about_group, owner=user)
                        if image:
                            new_group.image = image
                        new_group.save()
                        for friend in selected_friends:
                            friend = get_object_or_404(User, username=friend)
                            new_group.members.add(friend)
                        new_group.members.add(user)
                    else:
                        wrong_message = "Group chat requires at least 2 people"
            else:
                wrong_message = "Input of Chinese names is currently not supported"
        
        # deal with Group-editing   
        if editgroupform.is_valid():
            group_name = editgroupform.cleaned_data["change_group_name"]
            about_group = editgroupform.cleaned_data["change_about_group"]
            image = editgroupform.cleaned_data["change_image"]
            invite_person_email = editgroupform.cleaned_data["invite_person_email"]
            if invite_person_email != "" and invite_person_email is not None:
                to_user = User.objects.filter(email=invite_person_email)[0]
                all_members = cur_group.members.all()
                if not to_user in all_members:
                    Friend_Request.objects.create(
                        from_user=user,
                        to_user=to_user,
                        invite_message="Hello, I am {}. I am inviting you to join the Groups {}".format(user.username, cur_group.name),
                        groups_name=cur_group.name
                    )
            if group_name != "" and group_name is not None:
                cur_group.name = group_name
            if image:
                cur_group.image = image
            if about_group != "" and about_group is not None:
                cur_group.about_group = about_group
            selected_friends = request.POST.getlist('select_friends')
            cur_group_members = cur_group.members.all()
            import pdb
            pdb.set_trace()
            if selected_friends:
                for friend in selected_friends:
                    friend = get_object_or_404(User, username=friend)
                    if friend not in cur_group_members:
                        cur_group.members.add(friend)
            cur_group.save()
            
        
    all_groups = Groups.objects.all()
    own_groups = Groups.objects.filter(owner=user)
    in_groups = list()
    for group in all_groups:
        group: Groups
        if group.exist(user):
            in_groups.append(group)

    users_img_urls = dict()
    for rm in group_messages:
        user = rm.user
        user_profile = get_object_or_404(Profile, user=user)
        users_img_urls[user_profile.user.username] = user_profile.image_url

    # return the tpl
    return render(
        request=request, 
        template_name='chat/innergroup.html', 
        context={
            'profile': profile,
            'dark': dark,
            'light': not dark,
            'friends': user.friends.all(),
            "new_friends": Friend_Request.objects.filter(to_user=user),
            "wrong_message": wrong_message,
            'own_groups': own_groups,
            'in_groups': in_groups,
            'group_messages': group_messages,
            'cur_group': cur_group,
            'users_img_urls_json': json.dumps(users_img_urls),
            "cur_group_members": cur_group.members.all(),
        }
    )
    