from django.conf.urls import url
from .views import all_issues, get_issue, delete_issue, add_issue, edit_issue, add_solution, edit_solution, teams_cocurrics_issues,academic_issues, admin_dealing_issues, miscellaneous_issues, hostels_issues, upvotes

urlpatterns = [
    url(r'^all/$', all_issues, name = "all"),
    url(r'^teams_co_currics/$', teams_cocurrics_issues, name = "tncc"),
    url(r'^hostels/$', hostels_issues, name = "hostels"),
    url(r'^academics/$', academic_issues, name = "academics"),
    url(r'^admin_dealings/$', admin_dealing_issues, name = "admin-dealings"),
    url(r'^miscellaneous/$', miscellaneous_issues, name = "miscellaneous"),
    url(r'^(?P<id>[0-9]+)/$', get_issue , name = "get"),
    #url(r'^(?P<id>[0-9]+)/update/$', update_issue , name = "update"),
    #url(r'^createissue/$', create_issue, name = "create"),
    url(r'^(?P<id>[0-9]+)/delete/$', delete_issue , name = "delete"),
    url(r'^add/$', add_issue, name = "add-issue"),
    url(r'^(?P<id>[0-9]+)/edit/$', edit_issue , name = "edit"),
    url(r'^(?P<i_id>[0-9]+)/add-solution/$', add_solution, name = "add-solution"),
    url(r'^(?P<id>[0-9]+)/(?P<i_id>[0-9]+)/edit-solution/$', edit_solution, name = "edit-solution"),
    url(r'^upvote/$', upvotes, name = "upvote"),
]