from django.db import models
from config.g_model import TimeStampMixin


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    def get_variant(self):

        return ProductVariant.objects.filter(variant=self.id).order_by('variant_title').values('variant_title').distinct()


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    def get_product_variant(self):
        Pvariant=ProductVariantPrice.objects.filter(product=self.id)

        return Pvariant
    def get_product_variant_filter(price_to,price_from):

        return ProductVariantPrice.objects.filter(price__range=(price_from,price_to))

    def create_product(data):
        new_product=Product.objects.create(title=data['title'],sku=data['sku'],description=data['description'])
        for op in data['product_variant']:
            new_variant=Variant.objects.get(id=op['option']);
            for tag in op['tags']:
                new_product_variant=ProductVariant.objects.create(variant_title=tag,variant=new_variant,product=new_product)
        for p_v_p in data['product_variant_prices']:
            v = p_v_p['title'].split('/')
            print(v[0])
            try:
                product_variant_one=ProductVariant.objects.get(variant_title=v[0],product=new_product)
            except :
                product_variant_one=None
            try:
                product_variant_two = ProductVariant.objects.get(variant_title=v[1], product=new_product)
            except :
                product_variant_two = None
            try:
                product_variant_three = ProductVariant.objects.get(variant_title=v[2], product=new_product)
            except :
                product_variant_three = None
            new_product_variant_price=ProductVariantPrice.objects.create(product_variant_one=product_variant_one,
                                                   product_variant_two=product_variant_two,
                                                   product_variant_three=product_variant_three,price=p_v_p['price'],stock=p_v_p['stock'],product=new_product)
        return True

class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.URLField()


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    stock = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)