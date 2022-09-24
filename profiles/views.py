from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from profiles.models import Profile


#from chatterbox_project.profiles.models import Profile


# Create your views here.
@login_required
def profiles_list(request):
    profiles = Profile.objects.all()

    context = {'profiles': profiles}
    return render(request, 'profiles/users.html', context)


@login_required
def user_profile(request, pk):
    #user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=pk)

    context = {'profile': profile}  # 'user': user,
    return render(request, "profiles/user.html", context)


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about_me', 'photo')  # ToDo editable name...


class EditProfile(UpdateView):
    template_name = 'profiles/edituser.html'
    model = Profile
    form_class = EditProfileForm
    success_url = reverse_lazy('profiles')
