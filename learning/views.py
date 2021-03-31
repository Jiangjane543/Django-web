from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Topic,Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    '''快乐老家的主页'''
    return render(request,'learning/index.html')

def topics(request):
    '''显示所有的主题'''
    topics=Topic.objects.order_by('date_added')
    context={'topics':topics}
    return render(request,'learning/topics.html',context)

def topic(request, topic_id):
    '''单个主题及其所有的条目'''
    topic=Topic.objects.get(id=topic_id)
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning/topic.html',context)

@login_required
def new_entry(request,topic_id):
    '''在特定主题中添加新条目'''
    topic=Topic.objects.get(id=topic_id)
    if request.method!='POST':
        #未提交数据，创建一个空表单
        form=EntryForm()
    else:
        #POST提交的数据，对数据进行处理
        form=EntryForm(data=request.POST)
        if form.is_valid():#如果表单有效，就设置属性topic并保存到数据库中
            new_entry = form.save(commit=False)
            form.instance.owner=request.user
            new_entry.owner = request.user
            new_entry.owner_id = request.user.id
            new_entry.topic_id = topic_id
            new_entry.save()
            return HttpResponseRedirect(reverse('learning:topic',args=[topic_id]))
    context={'topic':topic,'form':form}
    return render(request,'learning/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    '''编辑已有条目'''
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if entry.owner!=request.user:
        raise Http404
    if request.method!='POST':
        #初次请求，使用当前条目填充表单
        form=EntryForm(instance=entry)
    else:
        #POST提交的数据，对数据进行处理
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning:topic',args=[topic.id]))
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning/edit_entry.html',context)
