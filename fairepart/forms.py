from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('email', 'text')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(InvitationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if Invitation.objects.filter(from_user=self.user, email=email).exists():
            raise forms.ValidationError(_('An invitation for %s already exist') % email)

        return email

    def save(self, *args, **kwargs):
        self.instance.from_user = self.user

        super(InvitationForm, self).save(*args, **kwargs)
