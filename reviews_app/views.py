
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from unidecode import unidecode
from reviews_app.forms import AddReviewForm, UploadFileForm
from reviews_app.models import GameReview, Category, TagReview, UploadFiles
from reviews_app.utils import DataMixin


def custom_slugify(value):
    return slugify(unidecode(value))


class GameReviewHome(DataMixin, ListView):
    template_name = 'review_app/index.html'
    context_object_name = 'reviews'
    title_page = 'GameReviews'
    paginate_by = 5

    def get_queryset(self):
        return GameReview.published.all().select_related('cat')


@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'review_app/about.html', {'title': 'About', 'form': form})


class ShowReview(DataMixin, DetailView):
    template_name = 'review_app/review.html'
    slug_url_kwarg = 'review_slug'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['review'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(GameReview.published, slug=self.kwargs[self.slug_url_kwarg])


class GameReviewCategory(ListView):
    template_name = 'review_app/index.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def get_queryset(self):
        return GameReview.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Cat: {get_object_or_404(Category, slug=self.kwargs["cat_slug"])}'
        context['cat_selected'] = Category.pk
        return context


class GameReviewTags(ListView):
    template_name = 'review_app/index.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def get_queryset(self):
        return GameReview.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Tag: {get_object_or_404(TagReview, slug=self.kwargs["tag_slug"])}'
        return context


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddReviewForm
    template_name = 'review_app/addreview.html'
    title_page = 'Add review'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    ''' Придумать функционал для этой функции,
    добавить аналогичную DeletePage для авторов постов'''

    model = GameReview
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'price']
    template_name = 'review_app/addreview.html'
    success_url = reverse_lazy('home')
    title_page = 'Add review'
    permission_required = 'reviews_app.change_gamereview'
