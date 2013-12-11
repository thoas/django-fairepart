from django import forms

from .models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('email', 'text')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(InvitationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.from_user = self.user

        super(InvitationForm, self).save(*args, **kwargs)
