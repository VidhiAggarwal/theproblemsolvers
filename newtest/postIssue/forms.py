from django import forms


from .models import Issue, Solution

class PostAnIssue(forms.ModelForm):
	class Meta:
		model = Issue
		fields = ['title', 'text', 'image', 'category']

class PostSolution(forms.ModelForm):
	class Meta:
		model = Solution
		fields = ['text']

