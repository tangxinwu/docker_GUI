#! coding=utf-8
from django.db import models

# Create your models here.


class ImagePull(models.Model):
    PullStatus_dict = (
        (0, '下载进行中'),
        (1, '下载已经完成'),
        (2, '下载失败'),)
    ImageName = models.CharField('镜像名', max_length=50)
    PullStatus = models.SmallIntegerField('下载状态', choices=PullStatus_dict)
    pid = models.IntegerField('下载的pid', blank=True, default=None)


