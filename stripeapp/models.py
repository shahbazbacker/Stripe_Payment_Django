from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=0, default=200)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    