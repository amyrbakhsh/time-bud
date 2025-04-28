from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#watch condition-----------------------------------
CONDITIONS = (
    ('N', 'New'),
    ('U', 'Used'),
    ('D', 'Damaged'),
)

#OPTIONAL------------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'pk': self.id})

#Watch Model-------------------------------
class Watch(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(
        max_length=1,
        choices=CONDITIONS,
        default=CONDITIONS[0][0]
    )
    image = models.ImageField(upload_to='watch_images/')
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_watches')
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} - {self.title} ({self.get_condition_display()})"

    def get_absolute_url(self):
        return reverse('watch_detail', kwargs={'pk': self.pk})

 #Bid Model-----------------------------------------
class Bid(models.Model):
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} by {self.bidder.username}"

#Transaction Model------------------------------------
class Transaction(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    final_price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.watch} bought by {self.buyer.username}"
