from django.forms import ModelForm
from apiauth.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("date_joined", "user")
