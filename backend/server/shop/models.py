from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator


class Category(models.Model):
    
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/')
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name}"


class Variant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=50, unique=True)

    class Meta:
        unique_together = ('product', 'size')
    
    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()} "
    

class Colors(models.Model):
    COLOR_PALETTE = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#F5F5DC", "beige"),
        ("#8B0000", "dark red"),
        ("#4169E1", "royal blue"),
        ("#FFD700", "gold"),
        ("#C0C0C0", "silver"),
        ("#50C878", "emerald green"),
        ("#FF6B6B", "coral pink"),
        ("#4B0082", "indigo"),
        ("#FFA500", "bright orange"),
        ("#A52A2A", "brown"),
        ("#FFC0CB", "pastel pink"),
        ("#808080", "gray"),
        ("#00FFFF", "cyan"),
        ("#E6E6FA", "lavender"),
        ("#36454F", "charcoal"),
        ("#FF00FF", "magenta"),
        ("#FFFF00", "yellow"),
        ("#00FF00", "lime green")
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = ColorField(samples=COLOR_PALETTE,default="#FFFFFF")
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name} - {self.color}"

