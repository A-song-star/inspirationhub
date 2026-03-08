"""
Forms for ideas app.
"""

from django import forms
from .models import Idea, Comment

class IdeaForm(forms.ModelForm):
    """灵感表单"""
    class Meta:
        model = Idea
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '输入您的灵感标题',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent h-32',
                'placeholder': '详细描述您的灵感...',
                'rows': 5
            }),
        }
        labels = {
            'title': '标题',
            'description': '描述',
        }

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '发表您的评论...',
                'rows': 3
            }),
        }
        labels = {
            'content': '',
        }
