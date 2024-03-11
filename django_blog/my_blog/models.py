# models.py
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import uuid
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product_list_category', args=[str(self.name)])

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    model_date = models.CharField(max_length=50)
    description = models.TextField(default=None)
    thumbnail = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)   

    def __str__(self): 
        return str(self.name)

class ImageUpload(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

class UserDetailModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    address = models.TextField(default=None)
    phone = models.IntegerField(default=None)
    email = models.EmailField(default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self): 
        return str(self.user)
	
class FavouriteModel(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	qty = models.IntegerField(default=None)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=datetime.now)

