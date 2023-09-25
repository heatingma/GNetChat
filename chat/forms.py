from django import forms
from users.models import User

###############################################
#                   Profile                   #
###############################################   

class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.CharField(max_length=50)
    about_me = forms.CharField(widget=forms.Textarea())
    image_default = forms.BooleanField(initial=True, required=False)
    image = forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        if 'username' in self.initial:
            username = self.initial['username']
            if username:
                self.fields['image'].initial = username[0].upper()
                
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