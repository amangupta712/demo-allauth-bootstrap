from django import forms
from allauth.socialaccount.forms import SignupForm
from .models import User


class MyCustomSocialSignupForm(SignupForm):
    subject_form_field = forms.ChoiceField(choices=User.SUBJECT_CHOICES)
    phone_form_field = forms.RegexField(required=True, regex=r'^\+?1?\d{9,12}$',
                                        error_messages={"invalid": "Please enter a valid phone number"})

    start_time = forms.ChoiceField(choices=[(x, x) for x in range(0, 24)])
    end_time = forms.ChoiceField(choices=[(x, x) for x in range(0, 24)])

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone_form_field']
        user.subject = self.cleaned_data['subject_form_field']
        start_time_int = int(self.cleaned_data['start_time'])
        end_time_int = int(self.cleaned_data['end_time'])
        user.fill_calender(start_time_int, end_time_int)
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
