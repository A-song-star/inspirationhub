"""
Models for ideas app.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Idea(models.Model):
    """灵感模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(verbose_name='详细描述')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas', verbose_name='作者')
    likes = models.ManyToManyField(User, related_name='liked_ideas', blank=True, verbose_name='点赞用户')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('idea-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def description_short(self):
        """截断描述，用于卡片显示"""
        words = self.description.split()
        if len(words) > 20:
            return ' '.join(words[:20]) + '...'
        return self.description
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '灵感'
        verbose_name_plural = '灵感'

class Comment(models.Model):
    """评论模型"""
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments', verbose_name='灵感')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='评论时间')
    
    def __str__(self):
        return f'{self.user.username} 对 {self.idea.title} 的评论'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
