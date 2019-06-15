from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def permission_denied(request, exception, template_name='403.html'):
    messages.warning(request, '權限不足')
    return redirect('root')


def register(request):
    if request.user.is_authenticated:
        return redirect('root')
        
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, '{} 您好，歡迎使用～'.format(user.username))
        return redirect('root')

    return render(request, 'user/register.html', {'form': form})