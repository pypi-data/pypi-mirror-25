from django.db import models
import shortuuid


def createuuid():
    return shortuuid.uuid()


class Base(models.Model):
    del_state_type = ((0, '已删除'), (1, '默认'))
    uuid = models.CharField(
        'ID',
        max_length=22,
        primary_key=True,
        default=createuuid,
        editable=False)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    del_state = models.IntegerField(
        '删除状态', choices=del_state_type, default=1, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-add_time']


class BaseMiddle(models.Model):
    uuid = models.CharField(
        'ID',
        max_length=22,
        primary_key=True,
        default=createuuid,
        editable=False)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-add_time']


class BaseSimple(models.Model):
    uuid = models.CharField(
        'ID',
        max_length=22,
        primary_key=True,
        default=createuuid,
        editable=False)

    class Meta:
        abstract = True
