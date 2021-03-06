from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = Post.objects.get(pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

def post_new(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        post = form.save(commit=False)
        # post.author = User
        post.published_date =timezone.now()
        post.save()
        return redirect('post_detail',pk=post.pk)
    else:
        form  = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request,pk):
    post =  Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_edit.html',{'form':form})


def post_delete(request,pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

    