from django.db import models
from member.models import Members

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    label = models.CharField(max_length=100)
    day = models.BigIntegerField()

    def __str__(self):
        return self.title


class Due(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='dues')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Due for {self.member.name} - {self.amount}"