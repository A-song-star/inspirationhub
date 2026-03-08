from django.apps import AppConfig

class IdeasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ideas'
    verbose_name = '灵感管理'
    
    def ready(self):
        """应用就绪时执行"""
        # 可以在这里导入信号处理等
        pass

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = '用户管理'
