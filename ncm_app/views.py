from django.shortcuts import render
from django.views import View
from django.http import Http404

from .models import Page


class HomePageView(View):
    template_name = 'page_template.html'

    def get(self, request):
        try:
            page = Page.objects.filter(main_page=True)[0]
            blocks = page.block_set.order_by('order')
        except Page.DoesNotExist:
            raise Http404("Страница не найдена")

        return render(request, self.template_name, {'page': page, 'blocks': blocks})


class PageView(View):
    template_name = 'page_template.html'

    def get(self, request, slug):
        try:
            page = Page.objects.get(slug=slug)
            blocks = page.block_set.order_by('order')
        except Page.DoesNotExist:
            raise Http404("Страница не найдена")

        return render(request, self.template_name, {'page': page, 'blocks': blocks})



