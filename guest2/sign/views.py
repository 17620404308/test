from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import  login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from sign.models import Event,Guest


def index(request):
    return render(request,"index.html")
def login_action(requst):
    if requst.method == 'POST':
        username = requst.POST.get('username','')
        password = requst.POST.get('password','')
        user = auth.authenticate(username = username,password=password)
        if user is not None:
            auth.login(requst,user)
        if username =='admin' and password =='admin123':
            # return HttpResponse('login success!')
            # return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600)
            requst.session['user'] =username
            return response
        else:
            return render(requst,'index.html',{'error':'username or password error!'})
@login_required
def event_manage(request):
    event_list=Event.objects.all()
    # username = request.COOKIES.get('user','')
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'events':event_list})
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.Get.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    # search_name = request.Get.get('name','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})
