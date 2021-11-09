from django.shortcuts import redirect

from django.db.models import Q
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostFormList, PostFormCreate, PostFormUpdate, CommentFormCreate, CommentFormList


class SearchResultsListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'AdsBoard/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class SearchCommentsResultsListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'AdsBoard/search_comments_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Comment.objects.filter(
            Q(post__title__icontains=query) | Q(content__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class HomePageView(TemplateView):
    template_name = "flatpages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class AboutPageView(TemplateView):
    template_name = "flatpages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class ContactsPageView(TemplateView):
    template_name = "flatpages/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class PostList(ListView):
    model = Post
    template_name = 'AdsBoard/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_posted')
    form_class = PostFormList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        context['current_user'] = self.request.user
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'AdsBoard/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user

        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'AdsBoard/category_detail.html'
    context_object_name = 'category_detail'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(category=self.object)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'AdsBoard/post_create.html'
    context_object_name = 'post_detail'
    form_class = PostFormCreate

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(category=self.object)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'AdsBoard/post_update.html'
    context_object_name = 'post_detail'
    form_class = PostFormUpdate

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'AdsBoard/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'AdsBoard/comment_create.html'
    context_object_name = 'comment'
    form_class = CommentFormCreate
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):

        form.instance.author = self.request.user
        id_post = self.kwargs.get('pk')
        form.instance.post = Post.objects.get(pk=id_post)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        id_post = self.kwargs.get('pk')
        context['post'] = Post.objects.get(pk=id_post)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'AdsBoard/comments.html'
    context_object_name = 'comments'
    form_class = CommentFormList

    def get_queryset(self):
        queryset = Comment.objects.filter(post__author=self.request.user).order_by('post', '-date_posted')
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'AdsBoard/comment_delete.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('comment_list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        i = 0
        list_fh = []
        list_sh = []
        for cat in Category.objects.all():
            i += 1
            if i <= len(Category.objects.all()) / 2:
                list_fh.append(cat)
            else:
                list_sh.append(cat)

        context['categories'] = Category.objects.all()
        context['cat_fh'] = list_fh
        context['cat_sh'] = list_sh
        return context


@login_required
def comment_approved(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.approved = True
    comment.save()
    return redirect(request.META.get('HTTP_REFERER'))
