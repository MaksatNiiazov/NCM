# Create your views here.
from django.views.generic import DetailView, ListView

from ncm_app.models import Footer, Header
from posts.models import Post





class PostDetailView(DetailView):
    model = Post
    template_name = 'post_templates/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer'] = Footer.objects.filter(is_default=True)[0] or None
        context['header'] = Header.objects.filter(is_default=True)[0] or None
        return context


class PostListView(ListView):
    model = Post
    template_name = 'post_templates/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer'] = Footer.objects.filter(is_default=True)[0] or None
        context['header'] = Header.objects.filter(is_default=True)[0] or None
        return context