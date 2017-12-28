from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):

	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	class Meta:
		verbose_name='Post'
		verbose_name_plural='Posts'

	def publish(self):
		post.published_date = timezone.now()
		post.save()

	def __str__(self):
		return self.title
    