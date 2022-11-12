"""djangoboke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from comment import views

"""
{% url '...' %}是Django规定的模板解耦语法，用它可以根据我们在urls.py中设置的名字，反向解析到对应的url中去。
"""
"""
两个path都使用了同一个视图函数，但是传入的参数却不一样多，
仔细看。第一个path没有parent_comment_id参数，
因此视图就使用了缺省值None，达到了区分评论层级的目的。
"""
app_name = 'comment'  # 前面定义了namespace，所以这个app_name必须写上
urlpatterns = [
    # 处理一级回复
    re_path('^post-comment/(?P<article_id>[0-9]+)/$', views.post_comment, name='post_comment'),
    # 处理二级回复
    re_path('^post-comment/(?P<article_id>[0-9]+)/(?P<parent_comment_id>[0-9]+)/$',
            views.post_comment, name='comment_reply'),
]
