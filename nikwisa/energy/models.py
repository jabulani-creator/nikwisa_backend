from django.db import models
from django.utils.text import slugify

from categories.models import Category

class EnergyCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/')
    # category = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='energy_categories') 


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(EnergyCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class EnergySubCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ManyToManyField(EnergyCategory, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(EnergySubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
