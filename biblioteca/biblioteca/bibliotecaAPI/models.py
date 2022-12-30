from django.db import models

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category_name

class Livro(models.Model):
    nome = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    descricao = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10)
    quantidade = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.nome