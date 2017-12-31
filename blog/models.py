from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):

	author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	class Meta:
		verbose_name='Post'
		verbose_name_plural='Posts'

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)

	def __str__(self):
		return self.title

class Comment(models.Model):
	# allows us to have access to comments from within the Post model.
	post = models.ForeignKey('blog.Post', related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	class Meta:
		verbose_name = "Comment"
		verbose_name_plural = "Comments"

	def __str__(self):
		return self.text
    