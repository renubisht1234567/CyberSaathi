from django.db import models


class User(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'democollection'
