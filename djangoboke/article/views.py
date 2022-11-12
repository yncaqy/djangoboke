from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from comment.forms import CommentForm
from comment.models import Comment
from .models import ArticlePost, ArticleColumn
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


# 更新文章(缺少一个添加标签的功能--->已完成)
@login_required(login_url='userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title 、body 字段
    GET方法进入初始表单页面
    :param request:
    :param id: 文章id
    :return:
    """
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            # 获取tags需要使用官方接口（https://django-taggit.readthedocs.io/en/latest/api.html）
            """
            tags.set()和tags.names()就是库提供的接口了，
            分别用于更新数据和获取标签名。注意tags.set()是如何将序列分隔并解包的。
            渲染空表单时用到了列表生成器将数据转换为字符串。
            """
            article.tags.set(request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成修改后返回修改后文章，需传入id
            return redirect("article:article_detail", id=id)
        # 如果数据不合法
        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 如果用户GET请求获取数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()

        # 赋值上下文，将article文章对象传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns,
                   'tags': ','.join([x for x in article.tags.names()])}
        # 将响应返回到模板
        return render(request, 'article/update.html', context)


# 安全删除文章
@login_required(login_url='userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 删除文章
@login_required(login_url='userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    # 完成删除操作后返回文章列表
    return redirect("article:article_list")


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        """
       为什么需要search = ''语句？如果用户没有搜索操作，则search = request.GET.get('search')会使得search = None，
       而这个值传递到模板中会错误地转换成"None"字符串！等同于用户在搜索“None”关键字
       """
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        # 注意Django-taggit中标签过滤的写法：filter(tags__name__in=[tag])，
        # 意思是在tags字段中过滤name为tag的数据条目。赋值的字符串tag用方括号包起来。
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    # 每页显示3篇文章
    paginator = Paginator(article_list, 3)
    # 获取url中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给articles
    articles = paginator.get_page(page)
    # 传递给模板templates的对象
    context = {'articles': articles, 'order': order, 'search': search, 'column': column, 'tag': tag}
    # render函数，载入模板，返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    comments = Comment.objects.filter(article=id)
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html样式
    """
    markdown.markdown语法接收两个参数：第一个参数是需要渲染的文章正文article.body；第二个参数载入了常用的语法扩展，markdown.extensions.extra中包括了缩写、表格等扩展，
    markdown.extensions.codehilite则是后面要使用的代码高亮扩展。
    """
    md = markdown.Markdown(extensions=[
        # 包含缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body)
    # 引入表单评论
    comment_form = CommentForm()
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form}
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中id=1的用户为作者
            # 如果进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 保存到数据库
            new_article.save()

            # 新增代码，保存tags的多对多关系
            """
            需要注意的是，如果提交的表单使用了commit=False选项，
            则必须调用save_m2m()才能正确的保存标签，就像普通的多对多关系一样。
            """
            article_post_form.save_m2m()

            # 完成后返回文章列表
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
