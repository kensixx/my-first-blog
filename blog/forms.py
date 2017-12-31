from django import forms
from .models import Post

class PostForm(forms.ModelForm):

	class Meta:
		# tell Django which model should be used to create this form
		model = Post 

		# which field(s) should end up in our form.
		fields = ('title', 'text',)
    