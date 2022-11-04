from django.db.models import Subquery
from django.views import generic
from django.views.generic import ListView

from datetime import datetime, timedelta


from product.models import Variant, Product, ProductVariantPrice, ProductVariant


class BaseProductView(generic.View):

    model = Product
    template_name = 'product/create.html'
    success_url = '/product/list'


class ProductView(BaseProductView, ListView):
    template_name = 'products/list.html'
    paginate_by = 5

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        if self.request.GET.get('title__icontains'):
            p3 = Product.objects.filter(title__icontains=self.request.GET.get('title__icontains'))

            if self.request.GET.get('price_from') or self.request.GET.get('price_to'):
                print("price")
                p3 = Product.objects.filter(title__icontains=self.request.GET.get('title__icontains')).filter(productvariantprice__price__range=(
                self.request.GET.get('price_from'), self.request.GET.get('price_to'))).distinct()
            return p3
        elif self.request.GET.get('price_from') or self.request.GET.get('price_to'):

            p3 = Product.objects.filter(productvariantprice__price__range=(self.request.GET.get('price_from'),self.request.GET.get('price_to'))).distinct()

            return p3
        elif self.request.GET.get('date'):
            print('date')
            print(self.request.GET.get('date'))
            p3 = Product.objects.filter(created_at__date__lte=self.request.GET.get('date'))

        return Product.objects.filter(**filter_string)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.GET.get('page'):
            print("true page")
            context['paginator'].get_page(self.request.GET.get('page'))
        context['variants']=Variant.objects.filter()
        context['pvariants']=ProductVariant.objects.filter().order_by('variant_title')

        return context

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
