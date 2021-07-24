from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Content, Comment, Tag
from .forms import ContentForm, CommentForm, TagForm

# Create your views here.

def home(request):
    posts = Content.objects.order_by('-pub_date')
    """ search = request.GET.get('search')
    if search == 'true':
        author = request.GET.get('writer')
        posts = Content.objects.filter(writer=author)
        return render(request, 'home.html', {'posts_list':posts}) """
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'posts_list':posts})

def new(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = ContentForm()

    return render(request, 'new.html', {'form':form})

def detail(request, index):
    post = get_object_or_404(Content, pk=index)
    comment_list = Comment.objects.filter(post=post)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.published_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('detail', index=index)
    else:
        comment_form = CommentForm()
        tag_form = TagForm()
    return render(request, 'detail.html', {'post':post, 'comment_list':comment_list, 'comment_form':comment_form, 'tag_form':tag_form})

def edit(request, index):
    post = get_object_or_404(Content, pk=index)
    if request.method == "POST":
        form = ContentForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now
            post.save()
            return redirect('detail', index=post.pk)
    else:
        form = ContentForm(instance=post)
    return render(request, 'edit.html', {'form':form})

def delete(request, index):
    post = get_object_or_404(Content, pk=index)
    post.delete()
    return redirect('home')

def delete_comment(request, index, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('detail', index=index)

def tag_add(request, pk):
    post = get_object_or_404(Content, pk=pk)
    tag_form = TagForm(request.POST)
    if tag_form.is_valid():
        tag = tag_form.save(commit=False)
        tag, created = Tag.objects.get_or_create(name=tag.name)
        post.tags.add(tag)
        return redirect('detail', index=pk)

def tag_home(request):
    tags = Tag.objects.all()
    return render(request, 'tag.html', {'tags':tags})

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag_posts = tag.content_set.all()
    return render(request, 'tag_detail.html', {'tag':tag, 'tag_posts':tag_posts})

def tag_delete(request, pk, tag_pk):
    post = get_object_or_404(Content, pk=pk)
    tag = get_object_or_404(Tag, pk=tag_pk)
    post.tags.remove(tag)
    if tag.content_set.count() == 0:
        tag.delete()
    return redirect('detail', pk=pk)
