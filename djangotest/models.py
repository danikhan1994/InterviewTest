from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class App(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    Plans = (
        (1, 'Free ($0)'),
        (2, 'Standard ($10)'),
        (3, 'Pro ($25)')
    )
    plan = models.IntegerField(choices=Plans, default=1)
    app = models.ForeignKey(App, on_delete=models.DO_NOTHING)
    subscribed = models.BooleanField()