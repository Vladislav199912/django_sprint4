import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)


from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post


User = get_user_model()


class PostView(ListView):
    template_name = 'blog/index.html'
    queryset = (Post.objects.
                select_related('category',
                               'author').
                filter(is_published=True,
                       category__is_published=True,
                       pub_date__lte=dt.datetime.now()))
    paginate_by = 10


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    queryset = Post.objects.filter(is_published=True,
                                   category__is_published=True,
                                   pub_date__date__lte=dt.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related('author')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect('blog:post_detail', args=self.kwargs['pk'])
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect('blog:post_detail', post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=[self.object.id])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, id=self.object.id)
        form = PostForm(self.request.POST, instance=instance)
        context['form'] = form
        return context

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)


def profile_detail(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile,
               'page_obj': page_obj,
               }
    return render(request, template, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView,):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.username != request.user.username:
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = category.posts.filter(category__slug__exact=category_slug,
                                  is_published=True,
                                  pub_date__date__lte=dt.datetime.now()
                                  ).order_by('id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category,
               'page_obj': page_obj,
               }
    return render(request, template, context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, pk, pk1):
    instance = get_object_or_404(Comment, pk=pk1)
    if instance.author != request.user:
        return redirect('blog:index')
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, pk, pk1):
    comment = get_object_or_404(Comment, pk=pk1)
    if comment.author != request.user:
        return redirect('blog:index')
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=pk)
    return render(request, 'blog/comment.html', context)
