from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
class SellerKYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    id_document = models.FileField(upload_to='uploads/kyc_documents/id/')
    address_proof = models.FileField(upload_to='uploads/kyc_documents/address/')

    def __str__(self):
        return self.user.username
    
    