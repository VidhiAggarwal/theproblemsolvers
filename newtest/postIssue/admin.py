from django.contrib import admin
from .models import MyUser, Issue, Solution

admin.site.register(MyUser)
#admin.site.register(Issue)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
	list_display = ['title', 'image','text', 'category', 'raised_by']

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
	list_display = ['question', 'text', 'posted_by','created_on', 'last_checked']