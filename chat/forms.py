from django import forms
from users.models import User

###############################################
#                   Profile                   #
###############################################   

class EditProfileForm(forms.Form):
    about_me = forms.CharField(widget=forms.Textarea(), required=False)
    image = forms.ImageField(required=False)
    location = forms.CharField(max_length=50, required=False)
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
                
    def clean_username(self):
        """
        This function throws an exception if the username has already been
        taken by another user
        """
        username = self.cleaned_data['username']
        if username != self.original_username:
            # filter!
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'A user with that username already exists.')
        return username
    
    
class RoomForm(forms.Form):
    name = forms.CharField(required=True)
    about_room = forms.CharField(widget=forms.Textarea(), required=False)
    image = forms.ImageField(required=False)


class PostForm(forms.Form):
    title = forms.CharField(required=True)
    about_post = forms.CharField(widget=forms.Textarea(), required=False)
    image = forms.ImageField(required=False)
    new_tag = forms.CharField(required=False)


class AttachmentForm(forms.Form):
    attachment = forms.FileField(required=True)
    content = forms.CharField(required=False)
    

class ChangeRoomForm(forms.Form):
    chatroom_ori_name = forms.CharField(required=True)
    chatroom_owner = forms.CharField(required=True)
    chatroom_name = forms.CharField(required=False)
    chatroom_about = forms.CharField(widget=forms.Textarea(), required=False)
    chatroom_image = forms.ImageField(required=False)


class EditPostForm(forms.Form):
    change_about_post = forms.CharField(widget=forms.Textarea(), required=False)
    upload_image = forms.ImageField(required=False)
    delete_tag = forms.CharField(required=False)
    add_tag = forms.CharField(required=False)
    

class ConfirmDeletePostForm(forms.Form):
    hidden_post_name = forms.CharField(required=True)
    hidden_user_name = forms.CharField(required=True) 
    confirm_post_name = forms.CharField(required=True)
    confirm_user_name = forms.CharField(required=True)


class ConfirmDeleteChatroomForm(forms.Form):
    hidden_chatroom_name = forms.CharField(required=True)
    hidden_user_name = forms.CharField(required=True) 
    confirm_chatroom_name = forms.CharField(required=True)
    confirm_user_name = forms.CharField(required=True)
    
    
class SendInvitationForm(forms.Form):
    invite_email = forms.CharField(required=True)
    invite_message = forms.CharField(widget=forms.Textarea(), required=False) 