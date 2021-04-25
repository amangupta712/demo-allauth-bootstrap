from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.views import SignupView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView  # ,FormMixin

from .forms import UserEditForm
from .forms import MyCustomSocialSignupForm


class CustomSocialSignUpView(SignupView):
    """Allow view and update of basic user data.

    In practice this view edits a model, and that model is
    the User object itself, specifically the names that
    a user has.

    The key to updating an existing model, as compared to creating
    a model (i.e. adding a new row to a database) by using the
    Django generic view ``UpdateView``, specifically the
    ``get_object`` method.
    """
    form_class = MyCustomSocialSignupForm
    template_name = "allauth/socialaccount/signup.html"
    view_name = 'socialaccount_signup_view'
    success_url = reverse_lazy(view_name)


class UserEditView(UpdateView):
    """Allow view and update of basic user data.

    In practice this view edits a model, and that model is
    the User object itself, specifically the names that
    a user has.

    The key to updating an existing model, as compared to creating
    a model (i.e. adding a new row to a database) by using the
    Django generic view ``UpdateView``, specifically the
    ``get_object`` method.
    """
    form_class = UserEditForm
    template_name = "auth/profile.html"
    view_name = 'account_profile'
    success_url = reverse_lazy(view_name)

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, 'User profile updated')
        return super(UserEditView, self).form_valid(form)


account_profile = login_required(UserEditView.as_view())
