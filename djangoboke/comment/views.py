from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User

# Create your views here.
"""
get_object_or_404()：它和Model.objects.get()的功能基本是相同的。区别是在生产环境下，如果用户请求一个不存在的对象时，Model.objects.get()会返回Error 500（服务器内部错误），
而get_object_or_404()会返回Error 404。相比之下，返回404错误更加的准确

redirect()：返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。
当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法。
因此接下来马上修改article的模型。
"""


# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理POST请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # 新增代码，给其他用户发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                return JsonResponse({'code': "200 OK", "new_comment_id": new_comment.id})
                # return HttpResponse("200 OK")

            new_comment.save()

            # 新增代码,给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )

            # 添加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)

            return redirect(redirect_url)

        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 处理GET请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接收get/post请求。")
