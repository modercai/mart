from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal
from django.db.models import Sum
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
    

class VendorBalance(models.Model):
    vendor = models.OneToOneField(User, related_name='vendor_balance', on_delete=models.CASCADE)
    pending_withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def get_available_balance(self):
        """
        Calculate available balance from completed orders minus processed withdrawals
        Ensures accurate tracking of vendor earnings
        """
        # Get all completed and paid orders for this vendor
        completed_orders = Order.objects.filter(
            items__product__user=self.vendor,
            status=Order.DELIVERED,
            is_paid=True
        ).distinct()
        
        # Calculate total earnings from vendor's products
        total_earnings = Decimal('0.00')
        for order in completed_orders:
            vendor_items = order.items.filter(product__user=self.vendor)
            total_earnings += sum(Decimal(str(item.price * item.quantity)) for item in vendor_items)
        
        # Calculate processed withdrawals
        processed_withdrawals = WithdrawalRequest.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        # Calculate pending withdrawals
        pending_withdrawals = WithdrawalRequest.objects.filter(
            vendor=self.vendor,
            status='pending'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        # Available balance calculation
        available_balance = total_earnings - (processed_withdrawals + pending_withdrawals)
        return max(available_balance, Decimal('0.00'))
    
    def get_total_earnings(self):
        """Calculate total earnings from all completed and paid orders"""
        completed_orders = Order.objects.filter(
            items__product__user=self.vendor,
            status=Order.DELIVERED,
            is_paid=True
        ).distinct()
        
        total_earnings = Decimal('0.00')
        for order in completed_orders:
            vendor_items = order.items.filter(product__user=self.vendor)
            total_earnings += sum(Decimal(str(item.price * item.quantity)) for item in vendor_items)
        
        return total_earnings

    def __str__(self):
        return f"{self.vendor.username}'s Balance"

    

class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    vendor = models.ForeignKey(User, related_name='withdrawal_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vendor.username} - {self.amount} ZMW"

    def save(self, *args, **kwargs):
        vendor_balance = VendorBalance.objects.get(vendor=self.vendor)
        
        if self._state.adding:  # If creating new withdrawal request
            vendor_balance.pending_withdrawal += self.amount
        else:  # If updating existing withdrawal request
            original = WithdrawalRequest.objects.get(pk=self.pk)
            if original.status == 'pending' and self.status in ['completed', 'rejected']:
                vendor_balance.pending_withdrawal -= self.amount
                
        vendor_balance.save()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_vendor_balance(sender, instance, created, **kwargs):
    """Create VendorBalance instance when a new user is created"""
    if created:
        VendorBalance.objects.create(vendor=instance)
    
    
    