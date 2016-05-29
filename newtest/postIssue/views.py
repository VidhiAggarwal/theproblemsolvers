#from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Issue, Solution, Upvote
from .forms import PostAnIssue, PostSolution
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.



@require_GET
@login_required
def all_issues(request): 
    #today = timezone.now().date()
    #queryset_list = Issue.objects.active()
    upvote_list = [] 
    # list containing all the upvote objects corresponding to a particular post
    upvote_query_list = []
    queryset_list = Issue.objects.all().filter(isChecked='True')

    for query in queryset_list:
        upvote_query = Upvote.objects.filter(issue=query)
        upvote_query_list.append(upvote_query)
        upvote_list.append(upvote_query.count())

    #if request.user.is_staff or request.user.is_superuser:
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Issue.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list,5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {'i_list':queryset, 'upvote_list': upvote_list, 'upvote_query_list': upvote_query_list}
    return render(request, 'postIssue/base.html', context)


@require_GET
@login_required
def solved_issues(request): 
    upvote_list = [] 
    # list containing all the upvote objects corresponding to a particular post
    upvote_query_list = []
    queryset_list = Issue.objects.all().filter(isSolved='True')

    for query in queryset_list:
        upvote_query = Upvote.objects.filter(issue=query)
        upvote_query_list.append(upvote_query)
        upvote_list.append(upvote_query.count())

    query = request.GET.get('q')
    if query:
        queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list,5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {'i_list':queryset, 'upvote_list': upvote_list, 'upvote_query_list': upvote_query_list}
    return render(request, 'postIssue/solved.html', context)



@require_GET
@login_required
def upvotes(request):
    user = request.user
    # TODO: check if the issue objects existed
    issue_id = request.GET.get('id')
    print(issue_id)
    print(type(issue_id))
    issue = Issue.objects.get(id=int(issue_id))
    if Upvote.objects.filter(user=user, issue=issue).exists():
        return HttpResponse('You have already upvoted the post')
    else:
        Upvote.objects.create(user=user, issue=issue, is_upvoted=True)
        return HttpResponse('Upvoted')

@require_GET
@login_required
def teams_cocurrics_issues(request):
    today = timezone.now().date() 
    team_issues_list = Issue.objects.all().filter(category='TNC', isChecked='True')
    query = request.GET.get('q')
    if query:
        team_issues_list=team_issues_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(team_issues_list,5)
    page = request.GET.get('page')
    try:
        team_issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        team_issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        team_issues = paginator.page(paginator.num_pages)
    context = {'i_list':team_issues, 'name' : "TEAM AND CO CURRICS ISSUES"}
    return render(request, 'postIssue/common_issues.html', context)


@require_GET
@login_required
def hostels_issues(request):
    today = timezone.now().date() 
    hostel_issues_list = Issue.objects.all().filter(category='HO', isChecked='True')
    query = request.GET.get('q')
    if query:
        hostel_issues_list=hostel_issues_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(hostel_issues_list,5)
    page = request.GET.get('page')
    try:
        hostel_issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hostel_issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hostel_issues = paginator.page(paginator.num_pages)
    context = {'i_list':hostel_issues, 'name' : "HOSTEL-ISSUES"}
    return render(request, 'postIssue/common_issues.html', context)

@require_GET
@login_required
def academic_issues(request):
    today = timezone.now().date() 
    acad_issues_list = Issue.objects.all().filter(category='AD', isChecked='True')
    query = request.GET.get('q')
    if query:
        acad_issues_list=acad_issues_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(acad_issues_list,5)
    page = request.GET.get('page')
    try:
        acad_issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        acad_issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        acad_issues = paginator.page(paginator.num_pages)
    context = {'i_list':acad_issues, 'name' : "ACADEMIC-ISSUES"}
    return render(request, 'postIssue/common_issues.html', context)


@require_GET
@login_required
def admin_dealing_issues(request):
    today = timezone.now().date() 
    admin_issues_list = Issue.objects.all().filter(category='AC', isChecked='True')
    query = request.GET.get('q')
    if query:
        admin_issues_list=admin_issues_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(admin_issues_list,5)
    page = request.GET.get('page')
    try:
        admin_issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        admin_issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        admin_issues = paginator.page(paginator.num_pages)
    context = {'i_list':admin_issues, 'name' : "ADMIN DEALING ISSUES"}
    return render(request, 'postIssue/common_issues.html', context)

@require_GET
@login_required
def miscellaneous_issues(request):
    today = timezone.now().date() 
    misc_issues_list = Issue.objects.all().filter(category='MS', isChecked='True')
    query = request.GET.get('q')
    if query:
        misc_issues_list=misc_issues_list.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(raised_by__username__icontains=query)
            ).distinct()

    paginator = Paginator(misc_issues_list,5)
    page = request.GET.get('page')
    try:
        misc_issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        misc_issues = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        misc_issues = paginator.page(paginator.num_pages)
    context = {'i_list':misc_issues, 'name' : "MISCELLANEOUS ISSUES"}
    return render(request, 'postIssue/common_issues.html', context)


@require_GET
@login_required
def get_issue(request, id=None):
    if not id:
        raise Http404;
    i = get_object_or_404(Issue, id=id);
    solutions_list = Solution.objects.all().filter(question=i)
    #if not request.user.is_staff or not request.user.is_superuser:
    #    raise Http404;
    
    context = {'object': i, 'title': i.title, 's_list':solutions_list}
    return render(request, 'postIssue/detailedIssue.html', context)

# @login_required   # myself
# def create_issue(request):
#     form = PostAnIssue(request.POST or None, request.FILES or None);
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, "Successfully Created")
#         return HttpResponseRedirect(instance.get_absolute_url())

#     context = {'form':form, }
#     return render(request, 'postIssue/postIssueForm.html', context);

# @login_required
# def update_issue(request, id=None):
#     instance = get_object_or_404(Issue, id=id);
#     form = PostAnIssue(request.POST or None, request.FILES or None, instance=instance);
#     if form.is_valid():
#         instance = form.save(commit=False)   
#         instance.save()
#         messages.success(request, "Successfully Updated")
#         #return HttpResponseRedirect(instance.get_absolute_url())
#         return redirect (reverse('postIssue:get', kwargs = {'id':instance.id}))
#     else:
#         messages.error(request, "Not Successfully Updated")
        
#     context = {'title':instance.title, 'instance':instance, 'form':form }
#     return render(request, 'postIssue/postIssueForm.html', context);
#     #success message


@login_required
def delete_issue(request, id=None):
    instance = get_object_or_404(Issue, id=id);
    instance.delete();
    messages.success(request, "Successfully Deleted")
    return redirect('postIssue:all')

@require_http_methods(['GET', 'POST'])   #anushray bhaiya
@login_required
def add_issue(request):
    if request.method == 'GET':
        f = PostAnIssue();
        return render(request, 'postIssue/addIssue.html', {'f':f});
    else:
        f=PostAnIssue(request.POST,request.FILES)
        if f.is_valid():
            issue_object=f.save(commit=False)
            issue_object.raised_by=request.user
            issue_object.save()
            return HttpResponse('ok')
        else:
            return render(request, 'postIssue/addIssue.html', {'f': f})
    return render(request, 'postIssue/issue_posted.html', {'u':request.user})
    #return redirect('postIssue:all');

@require_http_methods(['GET', 'POST'])   #anushray bhaiya
@login_required
def edit_issue(request, id=None):
    issue_obj = get_object_or_404(Issue, id=id);
    if issue_obj.raised_by!=request.user:
        raise Http404;
    if request.method == 'GET':
        f = PostAnIssue(instance=issue_obj)
    else:
        f=PostAnIssue(request.POST, request.FILES, instance=issue_obj);
        if f.is_valid():
            issue_object=f.save();
            return HttpResponse('ok');
    context = {'i_id':issue_obj.id, 'f':f}  
    return render(request, 'postIssue/editIssue.html', context); 


@login_required
def add_solution(request, i_id=None):
    ques_obj=get_object_or_404(Issue, id=i_id);
    if request.method == 'GET':
        f = PostSolution()
    else:
        f=PostSolution(request.POST,request.FILES);
        if f.is_valid():
            solution_object=f.save(commit=False);
            solution_object.posted_by=request.user;
            solution_object.question=ques_obj;
            solution_object.save();
    return render(request, 'postIssue/addSolution.html', {'f':f})
    #return redirect('postIssue:all');

@require_http_methods(['GET', 'POST'])  
@login_required
def edit_solution(request, id=None, i_id=None):
    solution_obj = get_object_or_404(Solution, id=id);
    ques_obj=get_object_or_404(Issue, id=i_id);
    if solution_obj.posted_by!=request.user:
        raise Http404;
    if request.method == 'GET':
        f = PostSolution(instance=solution_obj)
    else:
        f=PostSolution(request.POST, request.FILES or None, instance=solution_obj);
        if f.is_valid():
            solution_object=f.save();
            return HttpResponse('ok');
    context = {'i_id':solution_obj.id, 'f':f}  
    return render(request, 'postIssue/editSolution.html', context); 



    