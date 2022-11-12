# -*- coding=utf-8 -*-
# @从此音尘各悄然，春山如黛草如烟
# @Project_Name:djangoboke
# @User:34409/月念尘
# @Date :2022/11/7 19:17
# @File : forms.py
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
