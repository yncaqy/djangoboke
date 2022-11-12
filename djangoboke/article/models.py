from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.
# 导入内建的User类型
from django.contrib.auth.models import User
# timezone用于处理时间相关事务
from django.utils import timezone


class ArticleColumn(models.Model):
    """
    栏目的Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    # 文章标签
    tags = TaggableManager(blank=True)
    # 文章栏目"一对多"外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 新增点赞数统计
    likes = models.PositiveIntegerField(default=0)

    # 保存时处理图片
    """
    save()是model内置的方法，
    它会在model实例每次保存时调用。
    这里改写它，将处理图片的逻辑“塞进去”。
    """
    """
    不太好理解的是if中的这个not kwargs.get('update_fields')。
    还记得article_detail()视图中为了统计浏览量而调用了save(update_fields=['total_views'])吗？没错，就是为了排除掉统计浏览量调用的save()，
    免得每次用户进入文章详情页面都要处理标题图，太影响性能了。
    """
    def save(self, *args, **kwargs):
        # 调用原有的save()功能
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y/x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        # 通过reverse()方法返回文章详情页面的url，实现了路由重定向。
        return reverse('article:article_detail', args=[self.id])

    def was_created_recently(self):
        # 若是最近发表的文章，返回True
        diff = timezone.now() - self.created
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and 0 <= diff.seconds < 60:
            return True
        else:
            return False
