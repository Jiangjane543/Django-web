from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    '''帖子'''
    text=models.CharField(max_length=200)#记录字符或文本的数据
    date_added=models.DateTimeField(auto_now_add=True)#记录日期和时间的数据，每当创建新主题时可自动设置成当前日期和时间

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

class Entry(models.Model):
    '''具体的内容'''
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)  #外键是数据库术语，引用数据库的另一条记录。每个条目都关联到特定主题；每个主题创建时都分配一个键。
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True) #按创建顺序呈现条目
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:#存储管理模型的额外信息
        verbose_name_plural='entries'#在需要时使用Entries来表示多个条目

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text)>50:
            return self.text[:50]+"..."#呈现条目时应显示哪些信息，如果超过50，返回text前五十个字符，省略号指出显示并非整个条目
        else:return self.text