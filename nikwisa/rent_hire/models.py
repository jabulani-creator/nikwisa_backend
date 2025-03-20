from django.db import models
from django.utils.text import slugify

class RentHireCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='rent_hire_categories/', blank=True, null=True)
    categories = models.ManyToManyField('categories.Category', related_name='rent_hire_categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(RentHireCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class RentHireSubCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ManyToManyField(RentHireCategory, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(RentHireSubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
