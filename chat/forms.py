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

    