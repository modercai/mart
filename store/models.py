from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image
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
    thumbnails = models.ImageField(upload_to='uploads/product_images/thumbnails/', blank=True,null=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=ACTIVE)
    
    def __str__(self): 
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnails:
            return self.thumbnails.url
        else:
            if self.image:
                self.thumbnails = self.make_thumbnail(self.image)
                self.save()
                
                return self.thumbnails.url
            else:
                return 'https//via.placeholder.com/240x240.jpg'
    
    def make_thumbnail(self,image,size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/','')
        thumbnail = File(thumb_io,name=name)
        return thumbnail

class Order(models.Model):
    PENDING = 'pending'
    PROCESSED = 'in-transit'
    DELIVERED = 'delivered'
    
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSED, 'in-transit'),
        (DELIVERED, 'Delivered'),
    )
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    merchant_id = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.first_name
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='items',on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    
    