from django import forms
from allauth.socialaccount.forms import SignupForm
# from django.utils.translation import ugettext_lazy as _

from .models import User


#
# SubjectChoices(models.IntegerChoices):
#     NONE = None, 'Choose a Subject ...'
#     CHESS = 1, 'Chess'
#     RUBIK_CUBE = 2, 'Rubik\'s Cube'
#     VEDIC_MATH = 3, 'Vedic Maths'


class MyCustomSocialSignupForm(SignupForm):
    subject_form_field = forms.ChoiceField(choices=User.SUBJECT_CHOICES)
    phone_form_field = forms.RegexField(required=True, regex=r'^\+?1?\d{9,12}$',
                                        error_messages={"invalid": "Please enter a valid phone number"})

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone_form_field']
        user.subject = self.cleaned_data['subject_form_field']
        user.save()
        # Add your own processing here.
        # You must return the original result.
        return user

    class Meta:
        model = User
        fields = ('phone', 'subject', 'calender')


class UserEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a User object.

    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'subject', 'display_name')


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone', 'subject', 'display_name', 'is_staff', 'is_active',
            'date_joined')

    def is_valid(self):
        return super().is_valid()
