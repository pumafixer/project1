from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk = user_id)
        return HttpResponse("Hello! %s님"%user)
    else:
         return HttpResponse("로그인 해주세요!")
   

def register(request):
    if request.method =='GET':
        return render(request,'register.html')
    elif request.method =='POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

    err_data={}
    if not(username and useremail and password and re_password):
        err_data['error']= '모든 값을 입력해주세요.'
    elif password != re_password:
        err_data['error']= '비밀번호가 다릅니다.'
    else:
        user = User(
            username=username,
            useremail=useremail,
            password=make_password(password),
        )
        user.save()
    return render(request,'register.html',err_data)

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method=='POST':
        useremail = request.POST.get('useremail',None)
        password= request.POST.get('password',None)

        err_data={}
        if not(useremail and password):
            err_data['error']= '모든 값을 입력해 주세요.'
        else:
            user = User.objects.get(useremail=useremail)
            if check_password(password, user.password):
                request.session['user']=user.id
                return redirect('/')
            else:
                err_data['error']='비밀번호가 일치하지 않습니다.'
    return render(request,'login.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
        return redirect('/') 
           
# Create your views here.
