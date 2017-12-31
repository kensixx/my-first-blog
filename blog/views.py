from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post

# import the PostForm from forms.py, same directory lang kaya may . sa unahan.
# tapos "forms" kasi forms.py, NOT! including .py extension.
from .forms import PostForm

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

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