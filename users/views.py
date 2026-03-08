"""
Views for users app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！欢迎加入灵感社区！')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """用户个人资料视图"""
    user_ideas = request.user.ideas.all()
    liked_ideas = request.user.liked_ideas.all()
    
    context = {
        'user_ideas': user_ideas,
        'liked_ideas': liked_ideas,
    }
    return render(request, 'users/profile.html', context)
