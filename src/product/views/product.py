from django.views import generic
from django.views.generic import ListView


from product.models import Variant, Product


class BaseProductView(generic.View):

    model = Product
    template_name = 'product/create.html'
    success_url = '/product/list'


class ProductView(BaseProductView, ListView):
    template_name = 'products/list.html'
    paginate_by = 2

    def get_queryset(self):

        return Product.objects.filter()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.GET.get('page'):
            print("true page")
            context['paginator'].get_page(self.request.GET.get('page'))


        return context

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
