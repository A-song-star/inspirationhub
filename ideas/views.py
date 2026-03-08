"""
Views for ideas app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Idea, Comment
from .forms import IdeaForm, CommentForm

def home(request):
    """首页视图，显示所有灵感和开场动画控制"""
    ideas = Idea.objects.all()
    form = IdeaForm() if request.user.is_authenticated else None
    
    # 如果数据库中没有灵感，创建示例数据
    if not ideas.exists():
        create_sample_ideas()
        ideas = Idea.objects.all()
    
    context = {
        'ideas': ideas,
        'form': form,
        'show_animation': not request.session.get('animation_shown', False)
    }
    
    # 标记动画已显示
    if context['show_animation']:
        request.session['animation_shown'] = True
    
    return render(request, 'ideas/home.html', context)

def idea_detail(request, pk):
    """灵感详情页视图"""
    idea = get_object_or_404(Idea, pk=pk)
    comments = idea.comments.all()
    comment_form = CommentForm() if request.user.is_authenticated else None
    user_has_liked = idea.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    context = {
        'idea': idea,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'ideas/detail.html', context)

@login_required
@require_POST
def like_idea(request, pk):
    """异步点赞视图"""
    idea = get_object_or_404(Idea, pk=pk)
    user = request.user
    
    if idea.likes.filter(id=user.id).exists():
        idea.likes.remove(user)
        liked = False
    else:
        idea.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': idea.total_likes()
    })

@login_required
@require_POST
def add_comment(request, pk):
    """添加评论视图"""
    idea = get_object_or_404(Idea, pk=pk)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.idea = idea
        comment.user = request.user
        comment.save()
        messages.success(request, '评论已发布！')
    
    return redirect('idea-detail', pk=pk)

@login_required
def create_idea(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ideas:home")  # 保存后跳回首页
    else:
        form = IdeaForm()

    return render(request, "ideas/create.html", {"form": form})

def create_sample_ideas():
    """创建示例灵感数据"""
    # 创建或获取测试用户
    test_user, created = User.objects.get_or_create(
        username='inspirer',
        defaults={'email': 'test@example.com'}
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
    
    # 示例灵感数据
    sample_ideas = [
        {
            'title': 'AI辅助创意写作工具',
            'description': '开发一个基于GPT的创意写作助手，能够根据用户输入的关键词生成故事大纲、人物设定和对话场景，帮助作家克服创作瓶颈。',
            'user': test_user
        },
        {
            'title': '可持续城市农场应用',
            'description': '创建一个社区共享的屋顶农场管理平台，居民可以认领种植区域，分享收成，学习有机种植技术，促进城市可持续生活。',
            'user': test_user
        },
        {
            'title': '冥想辅助智能灯光',
            'description': '设计一款能够根据用户呼吸节奏变化颜色和亮度的智能灯光设备，配合引导冥想应用，提供沉浸式放松体验。',
            'user': test_user
        },
        {
            'title': '语言学习社交平台',
            'description': '建立一个语言交换社区，用户可以通过视频聊天与母语者练习对话，系统自动匹配学习目标互补的伙伴，并提供实时翻译辅助。',
            'user': test_user
        },
        {
            'title': '二手书籍循环经济',
            'description': '开发一个智能书籍交换系统，用户上传闲置书籍，系统根据阅读兴趣推荐交换对象，通过物流网络实现全国范围的书籍循环。',
            'user': test_user
        },
        {
            'title': '远程团队协作虚拟空间',
            'description': '创建3D虚拟办公室环境，团队成员以虚拟形象进入，支持实时协作、白板讨论和非正式社交，增强远程团队的凝聚力。',
            'user': test_user
        }
    ]
    
    # 批量创建灵感
    for idea_data in sample_ideas:
        if not Idea.objects.filter(title=idea_data['title']).exists():
            Idea.objects.create(**idea_data)
