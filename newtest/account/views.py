from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from postIssue.models import MyUser, Issue
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ForgotPassword, SetPassword, SignUpForm
from .models import create_otp, get_valid_otp_object
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader


# Create your views here.

def home(request):
    return render(request, 'startpage.html')


    

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('account:home', kwargs = {'id':request.user.id}))
    if request.method == 'GET':
        context = { 'f' : LoginForm()}
        return render(request, 'account/login.html', context)
    else:
        f = LoginForm(request.POST);
        if not f.is_valid():
            return render(request, 'account/login.html', {'f': f})
        else:
            user=f.authenticated_user;
            auth_login(request,user) 
            return redirect (reverse('account:home', kwargs = {'id':user.id}))

def logout(request):
    auth_logout(request);
    return redirect(reverse("account:login"))

# @csrf_exempt
# def all_users(request):
#     return render(request, 'account/index.html');

# @require_GET
# def add_user(request):
#     return render(request, 'account/createuser.html');

# @require_POST
# def save_user(request):
#     username = request.POST.get('username' , '')
#     if not username:
#         raise Http404
#     u = MyUser.objects.create(username = username);
#     return HttpResponse('ok');

@login_required
def after_login_home(request,id):
    i = get_object_or_404(MyUser, id=id);
    #queryset_list = Issue.objects.all().filter(raised_by=i)
    queryset_list = i.issues_raised.all();
    print("hello")
    print(queryset_list.count())
    context = {'object': i, 'q_list':queryset_list}
    return render(request, 'account/loggedin.html',context)

def forgot_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('account:home', kwargs = {'id':request.user.id}))
    if request.method == 'GET':
        context = { 'f' : ForgotPassword()}
        return render(request, 'account/forgot-password.html', context)
    else:
        f = ForgotPassword(request.POST);
        if not f.is_valid():
            return render(request, 'account/forgot-password.html', {'f': f})
        else:
            user = MyUser.objects.get(username=f.cleaned_data['username'])
            otp = create_otp(user=user, purpose='FP')
            #send email
            email_body_context = {'u':user, 'otp':otp}
            body = loader.render_to_string('account/email/forgot-password.txt', email_body_context)
            message = EmailMultiAlternatives('Reset-Password', body, settings.EMAIL_HOST_USER
                , [user.email])
            #message.attach_alternative(html_body, 'text/html')
            message.send()

            return render(request, 'account/forgot-email-sent.html', {'u':user})

def reset_password(request, id=None, otp=None):
    if request.user.is_authenticated():
        return redirect(reverse('account:home', kwargs = {'id':request.user.id}))
    user = get_object_or_404(MyUser, id=id);
    otp_object = get_valid_otp_object(user=user, purpose='FP', otp=otp)
    if not otp_object:
        raise Http404();
    if request.method == 'GET':
        f = SetPassword();
    else:
        f = SetPassword(request.POST);
        if f.is_valid():
            user.set_password(f.cleaned_data['new_password'])
            user.save();
            otp_object.delete();
            return render(request, 'account/password-successfully-reset.html', {'u':user})
    context = {'f':f, 'otp':otp_object.otp, 'uid':user.id}
    return render(request, 'account/reset-password.html', context)


def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse('account:home', kwargs = {'id':request.user.id}))
    if request.method == 'GET':
        context = { 'f' : SignUpForm()}
        return render(request, 'account/signup.html', context)
    else:
        f = SignUpForm(request.POST,request.FILES);
        if not f.is_valid():
            return render(request, 'account/signup.html', {'f': f})
        else:
            get_hostname = request.get_host()
            print(type(get_hostname))
            user = f.save(commit=False);
            user.set_password(f.cleaned_data['password']);
            user.is_active = False
            user.save();

            otp = create_otp(user=user, purpose='AA')
            #send email
            email_body_context = {'u':user, 'otp':otp}
            body = loader.render_to_string('account/email/activate-account.txt', email_body_context)
            message = EmailMultiAlternatives('Activate-Account', body, settings.EMAIL_HOST_USER
                , [user.email])
            #message.attach_alternative(html_body, 'text/html')
            message.send()

            return render(request, 'account/activate-account-sent.html', {'u':user, 'hostname': get_hostname})

@require_http_methods(['GET', 'POST'])  
@login_required
def edit_profile(request, id=None):
    user_obj = get_object_or_404(MyUser, id=id);
    print(user_obj.id)
    print(id)
    if user_obj.id!=id:
        raise Http404;
    if request.method == 'GET':
        f = SignUpForm(instance=user_obj)
    else:
        f=SignUpForm(request.POST, request.FILES, instance=user_obj);
        if f.is_valid():
            user =f.save();
            return HttpResponse('ok');
    context = {'i_id':user_obj.id, 'f':f}  
    return render(request, 'account/editprofile.html', context); 


@require_GET
def activate(request, id=None, otp=None):
    if request.user.is_authenticated():
        return redirect(reverse('account:home', kwargs = {'id':request.user.id}))
    user = get_object_or_404(MyUser, id=id);
    otp_object = get_valid_otp_object(user=user, purpose='AA', otp=otp)
    if not otp_object:
        raise Http404();
    user.is_active = 1;
    user.save();
    otp_object.delete();
    return render(request, 'account/account-successfully-activated.html', {'u':user})









    



