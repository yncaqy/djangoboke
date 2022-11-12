# -*- coding=utf-8 -*-
# @从此音尘各悄然，春山如黛草如烟
# @Project_Name:djangoboke
# @User:34409/月念尘
# @Date :2022/11/9 22:21
# @File : my_filters_and_tags.py
"""
# 任意模板文件中
{% load my_filters_and_tags %}
{{ 'ABC'|transfer:'cool' }}  # 输出：'cool'
{{ 'ABC'|lower }}  # 输出： 'abc'
"""
from django import template

register = template.Library()


@register.filter(name='transfer')
def transfer(value, arg):
    """将输出强制转换为字符串 arg """
    return arg


@register.filter()
def lower(value):
    """将字符串转换为小写字符"""
    return value.lower()


from django.utils import timezone
import math


# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and 0 <= diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if 1 <= diff.days < 30:
        return str(diff.days) + "天前"

    if 30 <= diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"


@register.inclusion_tag('article/tag_list.html')
def show_comments_pub_time(article):
    """显示文章评论的发布时间"""
    comments = article.comments.all()
    return {'comments': comments}
