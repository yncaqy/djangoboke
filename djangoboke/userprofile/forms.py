# -*- coding=utf-8 -*-
# @从此音尘各悄然，春山如黛草如烟
# @Project_Name:djangoboke
# @User:34409/月念尘
# @Date :2022/11/6 14:36
# @File : forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile


# 登录表单，继承forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
# def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
class UserRegisterFrom(forms.ModelForm):
    # 复写User的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码进行一致性校验
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
