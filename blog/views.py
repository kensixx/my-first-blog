from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment

# import the PostForm from forms.py, same directory lang kaya may . sa unahan.
# tapos "forms" kasi forms.py, NOT! including .py extension.
from .forms import PostForm, CommentForm

# imports a decorator module shipped in Django, called "login_required"
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	# if cinlick na ni user yung "Save" button
	if request.method == "POST":
		# construct the PostForm with data from the form
		form = PostForm(request.POST)

		# check if all the forms are correct, walang invalid na inputs (ex. walang blanko sa required fields, walang letters na nilagay sa numbers-only na field)
		if form.is_valid():
			# don't save just yet, commit=False muna, kailangan pa yung author
			post = form.save(commit=False)
			post.author = request.user # kung sinuman nakalogin ang mapupunta sa post.author na model
			post.published_date = timezone.now()

			# save that shit kasama yung author and published_date
			post.save()

			# after clicking "Save", massave na lahat sa database yung inputs 

			# tapos magrredirect na sa post_detail na view.

			# na may argument na pk=post.pk kasi nga kailangan yun sa urls.py
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()

	# medyo di ko pa magets tong part na to. siguro dahil gutom na
	return render(request, 'blog/post_edit.html', {'form': form})

# function is the same as post_new
# kukuha lang tayo ng existing post sa database, with the pk para ma-"edit" nga siya.
@login_required
def post_edit(request, pk):

	# kunin sa database yung post, pag wala, display as 404 error.
	post = get_object_or_404(Post, pk=pk)

	# pag naclick na yung "SAVE" button
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)

		# same as post_new, check if form has no incorrect input fields
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)

	# display the form upon first click, na may laman na yung fields
	# as an instance of the get_object_or_404 sa taas
	else:
		form = PostForm(instance=post)

	# medyo di ko pa magets tong part na to. siguro dahil gutom na
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	# lalabas lang dito yung mga WALANG LAMAN yung published_date na field

	# order them by ascending order in created_date
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete() # Every Django model can be deleted by .delete(). It is as simple as that!

	return redirect('post_list')

def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()

	return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)