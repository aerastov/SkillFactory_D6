from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm

class NewsList(ListView):
  model = Post  # указываем модель, объекты которой мы будем выводить
  template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
  context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
  queryset = Post.objects.order_by('-dateCreation') # Сортируем от самой свежей по дате создания
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['list_in_page'] = self.paginate_by
    return context

class NewsItem(DetailView):
  model = Post
  template_name = 'news_item.html'
  context_object_name = 'news_item'


class Search(ListView):
  model = Post
  template_name = 'search.html'
  context_object_name = 'post_search'
  ordering = ['-dateCreation']
  filter_class = PostFilter # Для вывода фильтра не через форму
  paginate_by = 10

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filter = self.filter_class(self.request.GET, queryset=queryset)
    return self.filter.qs.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # Если выводить фильтр только через формы
    context['filter'] = self.filter # Если выводить фильтр не через формы
    context['list_in_page'] = self.paginate_by # Для отображения кол-ва выведенных публикаций на странице
    context['all_posts'] = Post.objects.all() # Для отображения общего кол-ва публикаций на сайте
    return context

class CreatePost(CreateView):
  model = Post
  template_name = 'create_post.html'
  form_class = PostForm

class EditPost(UpdateView):
  template_name = 'edit_post.html'
  form_class = PostForm

  def get_object(self, **kwargs):
    id = self.kwargs.get('pk')
    return Post.objects.get(pk=id)

class DeletePost2(DeleteView):
  model = Post
  template_name = 'delete_post.html'
  context_object_name = 'postdelete'
  queryset = Post.objects.all()
  success_url = '/../../'

class DeletePost(DeleteView):
  template_name = 'delete_post.html'
  queryset = Post.objects.all()
  success_url = '/news/'
