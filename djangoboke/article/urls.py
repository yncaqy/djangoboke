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

import article
from article import views

"""
{% url '...' %}是Django规定的模板解耦语法，用它可以根据我们在urls.py中设置的名字，反向解析到对应的url中去。
"""

app_name = 'article'  # 前面定义了namespace，所以这个app_name必须写上
urlpatterns = [
    re_path('^article_list/$', views.article_list, name='article_list'),
    # 在list.html中，通过href="{% url 'article:article_detail' article.id %}"，将id传递给article/urls.py
    re_path(r'^article_detail/(?P<id>[0-9]+)/$', views.article_detail, name='article_detail'),
    re_path(r'^article_create/$', views.article_create, name='article_create'),
    re_path(r'^article_delete/(?P<id>[0-9]+)/$', views.article_delete, name='article_delete'),
    # 安全删除文章
    re_path(
        r'^article-safe-delete/(?P<id>[0-9]+)/$',
        views.article_safe_delete,
        name='article_safe_delete'
    ),
    # 更新文章
    re_path(r'^article-update/(?P<id>[0-9]+)/$', views.article_update, name='article_update'),
    # 点赞+1
    re_path('^increase-likes/(?P<id>[0-9]+)/$', views.IncreaseLikesView.as_view(), name='increase_likes')
]
