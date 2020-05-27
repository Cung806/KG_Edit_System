# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import User

##领域表
# Create your models here.
class DomainModel(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=50, verbose_name="领域名称")
    users = models.ManyToManyField(User)

    class Meta:
        verbose_name = '领域管理'
        verbose_name_plural = '领域管理'
    def __str__(self):
        return self.domain_name


##实体属性表
class entityModel(models.Model):
    entity_id = models.AutoField(primary_key=True)
    domain_name = models.ForeignKey(DomainModel, on_delete=models.CASCADE,verbose_name="所属领域")
    entity_label = models.CharField(max_length=50, verbose_name="实体属性名称")

    class Meta:
        verbose_name = '实体管理'
        verbose_name_plural = '实体管理'


## 关系属性表
class relationModel(models.Model):
    relation_id = models.AutoField(primary_key=True)
    domain_name = models.ForeignKey(DomainModel, on_delete=models.CASCADE,verbose_name="所属领域")
    relation_label = models.CharField(max_length=50, verbose_name="关系属性名称")

    class Meta:
        verbose_name = '关系管理'
        verbose_name_plural = '关系管理'
