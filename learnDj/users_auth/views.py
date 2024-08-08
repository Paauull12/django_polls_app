from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterFrom
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from polls.models import Comment


def register(request):
    if request.method == "POST":
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            print(request.POST['group'].title)

            form.save()

            user = CustomUser.objects.get(username=form.cleaned_data.get('username'))
            group = Group.objects.get(name=request.POST['group'].title())
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} contul a fost creat!")

            return redirect('login_users')
    else:
        form = UserRegisterFrom()
    return render(request, 'users_auth/register.html', context={'form': form})


@login_required
def profile(request):
    return render(request, 'users_auth/profile.html', {'comments': Comment.objects.filter(user=request.user)})



