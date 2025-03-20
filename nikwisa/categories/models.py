from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    # category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    # image = models.ImageField(upload_to='subcategories/')

    def __str__(self):
        return self.title

# Create your models here.
