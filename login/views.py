from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import models
from . import forms


# Create your views here.

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect('/index')
    if request.method == 'POST':
        login_form = forms.UserForms(request.POST)
        message = '请检查填写的内容！'
        # 表单类自带的is_valid()方法一步完成数据验证工作
        if login_form.is_valid():
            # 需要完成验证的数据
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            captcha = login_form.cleaned_data.get('captcha')
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                #  locals()函数，它返回当前所有的本地变量字典
                return render(request, 'login/login.html', locals())

            if user.password == password:
                # 往session字典内写入用户状态和数据：
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    user_forms = forms.UserForms
    return render(request, 'login/login.html')


def register(request):
    # 首先判断用户是否登录
    if request.session.get('is_login', None):
        return redirect('/index/')
    # 进行请求方法的验证
    if request.method == 'POST':
        # 获取对应表单内容
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写内容'
        # 进行参数的验证
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            # 数据验证后进行判断
            if password1 != password1:
                message = '2次输入的密码不同'
                return render(request, '/login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '该用户名已存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已被注册'
                    return render(request, 'login/register.html', locals())
                # 没问题后将数据写入数据库
                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    # 判断是否登录被 未登录跳转登录页面
    if not request.session.get('is_login', None):
        redirect('/login/')
    # 退出登录则清空当前session
    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    # 但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除
    request.session.flush()
    # redirect 重定向
    # 记住redirect函数中直接是url路由地址,render才是request+对应的页面+字典
    return redirect('/login/')
