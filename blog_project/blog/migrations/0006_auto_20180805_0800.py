# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150616_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='callback_url',
            field=models.URLField(blank=True, verbose_name='回调url', null=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.CharField(max_length=200, verbose_name='广告描述'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='image_url',
            field=models.ImageField(verbose_name='图片路径', upload_to='ad/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='index',
            field=models.IntegerField(default=999, verbose_name='排列顺序(从小到大)'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.CharField(max_length=50, verbose_name='广告标题'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='分类', to='blog.Category', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='click_count',
            field=models.IntegerField(default=0, verbose_name='点击次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.CharField(max_length=50, verbose_name='文章描述'),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(verbose_name='是否推荐', default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(verbose_name='标签', to='blog.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=50, verbose_name='文章标题'),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='index',
            field=models.IntegerField(default=999, verbose_name='分类的排序'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, verbose_name='分类名称'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(verbose_name='文章', to='blog.Article', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=50, verbose_name='邮箱地址', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(verbose_name='父级评论', to='blog.Comment', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='url',
            field=models.URLField(blank=True, max_length=100, verbose_name='个人网页地址', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(blank=True, max_length=30, verbose_name='用户名', null=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='callback_url',
            field=models.URLField(verbose_name='url地址'),
        ),
        migrations.AlterField(
            model_name='links',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='description',
            field=models.CharField(max_length=200, verbose_name='友情链接描述'),
        ),
        migrations.AlterField(
            model_name='links',
            name='index',
            field=models.IntegerField(default=999, verbose_name='排列顺序(从小到大)'),
        ),
        migrations.AlterField(
            model_name='links',
            name='title',
            field=models.CharField(max_length=50, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30, verbose_name='标签名称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar/default.png', verbose_name='用户头像', null=True, blank=True, max_length=200, upload_to='avatar/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(unique=True, blank=True, max_length=11, verbose_name='手机号码', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='qq',
            field=models.CharField(blank=True, max_length=20, verbose_name='QQ号码', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.URLField(blank=True, max_length=100, verbose_name='个人网页地址', null=True),
        ),
    ]
