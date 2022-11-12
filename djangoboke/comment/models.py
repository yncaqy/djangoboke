from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


"""
模型不再继承内置的models.Model类，替换为MPTTModel，因此你的模型自动拥有了几个用于树形算法的新字段。（有兴趣的读者，可以在迁移好数据之后在SQLiteStudio中查看）
parent字段是必须定义的，用于存储数据之间的关系，不要去修改它。
reply_to外键用于存储被评论人。
将class Meta替换为class MPTTMeta，参数也有小的变化，这是模块的默认定义，实际功能是相同的。
"""
"""
举例说明：一级评论人为 a，二级评论人为 b（parent 为 a），
三级评论人为 c（parent 为 b）。因为我们不允许评论超过两级，因此将 c 的 parent 重置为 a，
reply_to 记录为 b，这样就能正确追溯真正的被评论者了。
"""
# 博文的评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    # 新增。mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 新增。记录二级评论回复给谁，str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
