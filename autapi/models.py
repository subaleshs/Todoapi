from datetime import date
from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.auth.models import User
from datetime import date

class todo(models.Model):
    
    job = models.CharField(max_length=28)
    stat = models.BooleanField(default=False)
    completeBy = models.DateField(default=date.today,null=True)
    usrid = models.ForeignKey(User,related_name='work',on_delete=models.CASCADE)
    

    class Meta:
        ordering = ('stat',)

    def __str__(self):
        return self.job
