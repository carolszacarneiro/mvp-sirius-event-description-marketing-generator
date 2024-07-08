from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    banner_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
