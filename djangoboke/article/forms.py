# -*- coding=utf-8 -*-
# @从此音尘各悄然，春山如黛草如烟
# @Project_Name:djangoboke
# @User:34409/月念尘
# @Date :2022/11/6 12:17
# @File : forms.py
"""
在HTML中，表单是在 <form>...</form> 中的一些元素，它允许访客做类似输入文本、选择选项、操作对象或空间等动作，然后发送这些信息到服务端。一些表单界面元素（文本框或复选框）非常简单并内置在HTML中，而其他会复杂些：像弹出日期选择等操作控件。
处理表单是一件挺复杂的事情。想想看Django的admin，许多不同类型的数据可能需要在一张表单中准备显示，渲染成HTML，使用方便的界面进行编辑，传到服务器，验证和清理数据，然后保存或跳过进行下一步处理。
Django的表单功能可以简化上述工作的大部分内容，并且也能比大多数程序员自己编写代码去实现来的更安全。
Django表单系统的核心组件是 Form类，它能够描述一张表单并决定它如何工作及呈现。
要使用Form类也很简单，需要在article/中创建forms.py文件，
"""
from django import forms
from .models import ArticlePost


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含字段
        fields = ('title', 'body', 'tags', 'avatar')
