from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    
    DRAFT = 'draft'
    WAITING_APPROVAL = 'awaitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'
    
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL,'Awaitng Approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )
    
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/product_images', blank=True, null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=ACTIVE)
    
    def __str__(self): 
        return self.title
    